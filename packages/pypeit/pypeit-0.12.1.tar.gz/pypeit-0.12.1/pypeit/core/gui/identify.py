import os
import copy
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.cm import ScalarMappable
import matplotlib.transforms as mtransforms
from matplotlib.widgets import Button, Slider

from IPython import embed

from pypeit.par import pypeitpar
from pypeit.core.wavecal import fitting, waveio, wvutils
from pypeit import utils, msgs
from astropy.io import ascii as ascii_io
from astropy.table import Table

operations = dict({'cursor': "Select lines (LMB click)\n" +
                    "         Select regions (LMB drag = add, RMB drag = remove)\n" +
                    "         Navigate (LMB drag = pan, RMB drag = zoom)",
                   'p' : "Toggle pan/zoom with the cursor",
                   'q' : "Close Identify window and continue PypeIt reduction",
                   'a' : "Automatically identify lines using current solution",
                   'c' : "Clear automatically identified lines",
                   'd' : "Delete all line identifications (start from scratch)",
                   'f' : "Fit the wavelength solution",
                   'l' : "Load saved line IDs from file",
                   'r' : "Refit a line",
                   's' : "Save current line IDs to a file",
                   'w' : "Toggle wavelength/pixels on the x-axis of the main panel",
                   'z' : "Delete a single line identification",
                   '+/-' : "Raise/Lower the order of the fitting polynomial"
                   })


class Identify(object):
    """
    GUI to interactively identify arc lines. The GUI can be run within
    PypeIt during data reduction, or as a standalone script outside of
    PypeIt. To initialise the GUI, call the initialise() function in this
    file.
    """

    def __init__(self, canvas, axes, spec, specres, detns, line_lists, par, lflag_color, slit=0):
        """Controls for the Identify task in PypeIt.

        The main goal of this routine is to interactively identify arc lines
        to be used for wavelength calibration.

        Args:
            canvas (Matploltib figure canvas): The canvas on which all axes are contained
            axes (dict): Dictionary of four Matplotlib axes instances (Main spectrum panel, two for residuals, one for information)
            spec (Line2D): Matplotlib Line2D instance which contains plotting information of the plotted arc spectrum
            specres (dict): Three element list of Matplotlib Line2D/path instances, used for residuals plotting
            detns (ndarray): Detections from the arc spectrum
            line_lists (Table): Contains information about the line list to be used for wavelength calibration
            par (WavelengthSolutionPar): Calibration parameters
            lflag_color (list): List of colors used for plotting
            slit (int): The slit to be used for wavelength calibration
        """
        # Store the axes
        self.axes = axes
        # Initialise the spectrum properties
        self.spec = spec
        self.specres = specres   # Residual information
        self.specdata = spec.get_ydata()
        self.specx = np.arange(self.specdata.size)
        self.plotx = self.specx.copy()
        # Detections, linelist, line IDs, and fitting params
        self._slit = slit
        self._detns = detns
        self._detnsy = self.get_ann_ypos()  # Get the y locations of the annotations
        self._line_lists = line_lists
        self._lines = np.sort(line_lists['wave'].data)  # Remove mask (if any) and then sort
        self._lineids = np.zeros(self._detns.size, dtype=np.float)
        self._lineflg = np.zeros(self._detns.size, dtype=np.int)  # Flags: 0=no ID, 1=user ID, 2=auto ID, 3=flag reject
        self._lflag_color = lflag_color
        self.par = par
        # Fitting properties
        self._fitdict = dict(polyorder=1,
                             scale=self.specdata.size-1,
                             coeff=None,
                             fitc=None,
                             res_stats=[]
                             )
        # Initialise the residuals colormap
        residcmap = LinearSegmentedColormap.from_list("my_list", ['grey', 'blue', 'orange', 'red'], N=4)
        self.residmap = ScalarMappable(norm=Normalize(vmin=0, vmax=3), cmap=residcmap)
        # Initialise the annotations
        self.annlines = []
        self.anntexts = []

        # Unset some of the matplotlib keymaps
        matplotlib.pyplot.rcParams['keymap.fullscreen'] = ''        # toggling fullscreen (Default: f, ctrl+f)
        matplotlib.pyplot.rcParams['keymap.home'] = ''              # home or reset mnemonic (Default: h, r, home)
        matplotlib.pyplot.rcParams['keymap.back'] = ''              # forward / backward keys to enable (Default: left, c, backspace)
        matplotlib.pyplot.rcParams['keymap.forward'] = ''           # left handed quick navigation (Default: right, v)
        #matplotlib.pyplot.rcParams['keymap.pan'] = ''              # pan mnemonic (Default: p)
        matplotlib.pyplot.rcParams['keymap.zoom'] = ''              # zoom mnemonic (Default: o)
        matplotlib.pyplot.rcParams['keymap.save'] = ''              # saving current figure (Default: s)
        matplotlib.pyplot.rcParams['keymap.quit'] = ''              # close the current figure (Default: ctrl+w, cmd+w)
        matplotlib.pyplot.rcParams['keymap.grid'] = ''              # switching on/off a grid in current axes (Default: g)
        matplotlib.pyplot.rcParams['keymap.yscale'] = ''            # toggle scaling of y-axes ('log'/'linear') (Default: l)
        matplotlib.pyplot.rcParams['keymap.xscale'] = ''            # toggle scaling of x-axes ('log'/'linear') (Default: L, k)
        matplotlib.pyplot.rcParams['keymap.all_axes'] = ''          # enable all axes (Default: a)

        # Initialise the main canvas tools
        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('key_press_event', self.key_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        self.canvas = canvas
        self.background = self.canvas.copy_from_bbox(self.axes['main'].bbox)

        # Setup slider for the linelist
        self._slideval = 0  # Default starting point for the linelist slider
        self.linelist_init()

        # Interaction variables
        self._detns_idx = -1
        self._fitr = None  # Matplotlib shaded fit region (for refitting lines)
        self._fitregions = np.zeros(self.specdata.size, dtype=np.int)  # Mask of the pixels to be included in a fit
        self._addsub = 0   # Adding a region (1) or removing (0)
        self._respreq = [False, None]  # Does the user need to provide a response before any other operation will be permitted? Once the user responds, the second element of this array provides the action to be performed.
        self._qconf = False  # Confirm quit message
        self._changes = False
        self._wavepix = 1   # Show wavelength (0) or pixels (1) on the x-axis of the main panel

        # Draw the spectrum
        self.replot()

    def print_help(self):
        """Print the keys and descriptions that can be used for Identification
        """
        keys = operations.keys()
        print("===============================================================")
        print(" Colored lines in main panels:")
        print("   gray   : wavelength has not been assigned to this detection")
        print("   red    : currently selected line")
        print("   blue   : user has assigned wavelength to this detection")
        print("   yellow : detection has been automatically assigned")
        print(" Colored symbols in residual panels:")
        print("   gray   : wavelength has not been assigned to this detection")
        print("   blue   : user has assigned wavelength to this detection")
        print("   yellow : detection has been automatically assigned")
        print("   red    : automatically assigned wavelength was rejected")
        print("---------------------------------------------------------------")
        print("       IDENTIFY OPERATIONS")
        for key in keys:
            print("{0:6s} : {1:s}".format(key, operations[key]))
        print("---------------------------------------------------------------")

    def replot(self):
        """Redraw the entire canvas
        """
        # First set the xdata to be shown
        self.canvas.restore_region(self.background)
        self.toggle_wavepix()
        self.draw_residuals()
        self.draw_lines()
        self.canvas.draw()

    def linelist_update(self, val):
        """For a given detection, set the linelist value to be the best guess based on the wavelength solution

        When a user selects a detection, reset the current value of the linelist
        to reflect the best candidate wavelength for that detection (given the current
        wavelength solution)

        Args:
            val (int): The index corresponding to the closest match
        """
        val = int(val)
        self._slidell.label.set_text("{0:.4f}".format(self._lines[val]))
        self._slideval = val

    def linelist_select(self, event):
        """Assign a wavelength to a detection

        Note, only the LMB works.

        Args:
            event (Event): A matplotlib event instance
        """
        if event.button == 1:
            self.update_line_id()
            self._detns_idx = -1
            # Try to perform a fit
            self.fitsol_fit()
            # Now replot everything
            self.replot()

    def linelist_init(self):
        """Initialise the linelist Slider (used to assign a line to a detection)
        """
        axcolor = 'lightgoldenrodyellow'
        # Slider
        self.axl = plt.axes([0.15, 0.87, 0.7, 0.04], facecolor=axcolor)
        self._slidell = Slider(self.axl, "{0:.4f}".format(self._lines[self._slideval]), self._slideval,
                               self._lines.size-1, valinit=0, valstep=1)
        self._slidell.valtext.set_visible(False)
        self._slidell.on_changed(self.linelist_update)
        # Select button
        selax = plt.axes([0.86, 0.87, 0.1, 0.04])
        self._select = Button(selax, 'Assign Line', color=axcolor, hovercolor='y')
        self._select.on_clicked(self.linelist_select)

    def toggle_wavepix(self, toggled=False):
        if toggled:
            self._wavepix = 1 - self._wavepix
        self.plotx = self.specx.copy()  # Plot pixels on the x-axis
        if self._wavepix == 0:
            # Check that a wavelength solution exists
            if self._fitdict['coeff'] is None:
                self.update_infobox(message="Unable to show wavelength until a guess at the solution is available",
                                    yesno=False)
            else:
                self.plotx = self._fitdict['wave_soln'].copy()
        # Update the x-axis data and axis range
        self.spec.set_xdata(self.plotx)
        if toggled:
            self.axes['main'].set_xlim([self.plotx.min(), self.plotx.max()])

    def draw_lines(self):
        """Draw the lines and annotate with their IDs
        """
        for i in self.annlines: i.remove()
        for i in self.anntexts: i.remove()
        self.annlines = []
        self.anntexts = []
        # Decide if pixels or wavelength is being plotted
        plotx = self._detns
        if self._wavepix == 0 and self._fitdict['fitc'] is not None:
            # Plot wavelength
            pixel_fit = self._detns
            xnorm = self._fitdict['xnorm']

            # Calculate the estimated wavelength of the detections
            plotx = utils.func_val(self._fitdict['fitc'],
                                   pixel_fit / xnorm,
                                   self._fitdict["function"],
                                   minx=self._fitdict['fmin'],
                                   maxx=self._fitdict['fmax'])
        # Plot the lines
        xmn, xmx = self.axes['main'].get_xlim()
        w = np.where((plotx > xmn) & (plotx < xmx))[0]
        for i in range(w.size):
            if self._lineflg[w[i]] in [0, 3]:
                if w[i] == self._detns_idx:
                    self.annlines.append(self.axes['main'].axvline(plotx[w[i]], color='r'))
                else:
                    self.annlines.append(self.axes['main'].axvline(plotx[w[i]], color='grey', alpha=0.5))
                continue
            else:
                if w[i] == self._detns_idx:
                    self.annlines.append(self.axes['main'].axvline(plotx[w[i]], color='r'))
                else:
                    self.annlines.append(self.axes['main'].axvline(plotx[w[i]],
                                                                   color=self._lflag_color[self._lineflg[w[i]]]))
                txt = "{0:.2f}".format(self._lineids[w[i]])
                self.anntexts.append(
                    self.axes['main'].annotate(txt, (plotx[w[i]], self._detnsy[w[i]]), rotation=90.0,
                                     color='b', ha='right', va='bottom'))

    def draw_residuals(self):
        """Update the subplots that show the residuals
        """
        if self._fitdict["coeff"] is None:
            nid = np.where((self._lineflg == 1) | (self._lineflg == 2))[0].size
            msg = "Cannot plot residuals until more lines have been identified\n" +\
                  "Polynomial order = {0:d}, Number of line IDs = {1:d}".format(self._fitdict["polyorder"], nid)
            self.update_infobox(message=msg, yesno=False)
        else:
            # Remove the annotated residual statistics
            for i in self._fitdict["res_stats"]:
                i.remove()
            self._fitdict["res_stats"] = []

            # Extract the fitting info
            wave_soln = self._fitdict['wave_soln']
            pixel_fit = self._detns
            wave_fit = self._lineids
            xnorm = self._fitdict['xnorm']
            ymin, ymax = np.min(wave_soln[wave_soln != 0.0]) * .95, np.max(wave_soln) * 1.05

            # Calculate some stats
            wave_soln_fit = utils.func_val(self._fitdict['fitc'],
                                           pixel_fit / xnorm,
                                           self._fitdict["function"],
                                           minx=self._fitdict['fmin'],
                                           maxx=self._fitdict['fmax'])
            dwv_pix = np.median(np.abs(wave_soln - np.roll(wave_soln, 1)))
            resvals = (wave_fit - wave_soln_fit) / dwv_pix

            # Pixel vs wavelength
            self.specres['pixels'].set_offsets(np.c_[pixel_fit, wave_fit])
            self.specres['model'].set_ydata(wave_soln)
            self.axes['fit'].set_ylim((ymin, ymax))
            self.specres['pixels'].set_color(self.residmap.to_rgba(self._lineflg))

            # Pixel residuals
            self.specres['resid'].set_offsets(np.c_[pixel_fit, resvals])
            self.axes['resid'].set_ylim((-1.0, 1.0))
            self.specres['resid'].set_color(self.residmap.to_rgba(self._lineflg))

            # Write some statistics on the plot
            disptxt = r'$\Delta\lambda$={:.3f}$\AA$ (per pix)'.format(dwv_pix)
            rmstxt = 'RMS={:.3f} (pixels)'.format(self._fitdict['rms'])
            self._fitdict["res_stats"].append(self.axes['fit'].text(0.1 * self.specdata.size,
                                                                    ymin + 0.90 * (ymax - ymin),
                                                                    disptxt, size='small'))
            self._fitdict["res_stats"].append(self.axes['fit'].text(0.1 * self.specdata.size,
                                                                    ymin + 0.80 * (ymax - ymin),
                                                                    rmstxt, size='small'))

    def draw_callback(self, event):
        """Draw the lines and annotate with their IDs

        Args:
            event (Event): A matplotlib event instance
        """
        # Get the background
        self.background = self.canvas.copy_from_bbox(self.axes['main'].bbox)
        # Set the axis transform
        trans = mtransforms.blended_transform_factory(self.axes['main'].transData, self.axes['main'].transAxes)
        self.draw_fitregions(trans)
        self.axes['main'].draw_artist(self.spec)
        self.draw_lines()

    def draw_fitregions(self, trans):
        """Refresh the fit regions

        Args:
            trans (AxisTransform): A matplotlib axis transform from data to axes coordinates
        """
        if self._fitr is not None:
            self._fitr.remove()
        # Find all regions
        regwhr = np.copy(self._fitregions == 1)
        # Fudge to get the leftmost pixel shaded in too
        regwhr[np.where((self._fitregions[:-1] == 0) & (self._fitregions[1:] == 1))] = True
        self._fitr = self.axes['main'].fill_between(self.plotx, 0, 1, where=regwhr, facecolor='green',
                                          alpha=0.5, transform=trans)

    def get_ann_ypos(self, scale=1.02):
        """Calculate the y locations of the annotated IDs

        Args:
            scale (float): Scale the location relative to the maximum value of the spectrum

        Returns:
            ypos (ndarray): y locations of the annotations
        """
        ypos = np.zeros(self._detns.size)
        for xx in range(self._detns.size):
            wmin = np.argmin(np.abs(self.specx-self._detns[xx]))
            ypos[xx] = scale * np.max(self.specdata[wmin-1:wmin+2])
        return ypos

    def get_detns(self):
        """Get the index of the detection closest to the cursor
        """
        return np.argmin(np.abs(self._detns-self.specx[self._end]))

    def get_ind_under_point(self, event):
        """Get the index of the line closest to the cursor

        Args:
            event (Event): Matplotlib event instance containing information about the event

        Returns:
            ind (int): Index of the spectrum where the event occurred
        """
        ind = np.argmin(np.abs(self.plotx - event.xdata))
        return ind

    def get_axisID(self, event):
        """Get the ID of the axis where an event has occurred

        Args:
            event (Event): Matplotlib event instance containing information about the event

        Returns:
            axisID (int, None): Axis where the event has occurred
        """
        if event.inaxes == self.axes['main']:
            return 0
        elif event.inaxes == self.axes['resid']:
            return 1
        elif event.inaxes == self.axes['fit']:
            return 2
        elif event.inaxes == self.axes['info']:
            return 3
        return None

    def get_results(self):
        """Perform the final wavelength calibration

        Using the line IDs perform the final fit according
        to the wavelength calibration parameters set by the
        user. This routine must be called after the user has
        manually identified all lines.

        Returns:
            wvcalib (dict): Dict of wavelength calibration solutions
        """
        wvcalib = {}
        # Check that a result exists:
        if self._fitdict['coeff'] is None:
            wvcalib[str(self._slit)] = None
        else:
            # Perform an initial fit to the user IDs
            self.fitsol_fit()
            # Now perform a detailed fit
            gd_det = np.where((self._lineflg == 1) | (self._lineflg == 2))[0]
            bdisp = self.fitsol_deriv(self.specdata.size/2) # Angstroms/pixel at the centre of the spectrum
            try:
                final_fit = fitting.iterative_fitting(self.specdata, self._detns, gd_det,
                                                      self._lineids[gd_det], self._line_lists, bdisp,
                                                      verbose=False, n_first=self.par['n_first'],
                                                      match_toler=self.par['match_toler'],
                                                      func=self.par['func'],
                                                      n_final=self.par['n_final'],
                                                      sigrej_first=self.par['sigrej_first'],
                                                      sigrej_final=self.par['sigrej_final'])
            except TypeError:
                wvcalib[str(self._slit)] = None
            else:
                wvcalib[str(self._slit)] = copy.deepcopy(final_fit)
        return wvcalib

    def button_press_callback(self, event):
        """What to do when the mouse button is pressed

        Args:
            event (Event): Matplotlib event instance containing information about the event
        """
        if event.inaxes is None:
            return
        if self.canvas.toolbar.mode != "":
            return
        if event.button == 1:
            self._addsub = 1
        elif event.button == 3:
            self._addsub = 0
        axisID = self.get_axisID(event)
        self._start = self.get_ind_under_point(event)

    def button_release_callback(self, event):
        """What to do when the mouse button is released

        Args:
            event (Event): Matplotlib event instance containing information about the event

        Returns:
            None
        """
        if event.inaxes is None:
            return
        if event.inaxes == self.axes['info']:
            if (event.xdata > 0.8) and (event.xdata < 0.9):
                answer = "y"
            elif event.xdata >= 0.9:
                answer = "n"
            else:
                return
            self.operations(answer, -1)
            self.update_infobox(default=True)
            return
        elif self._respreq[0]:
            # The user is trying to do something before they have responded to a question
            return
        if self.canvas.toolbar.mode != "":
            return
        # Draw an actor
        axisID = self.get_axisID(event)
        if axisID is not None:
            if axisID <= 2:
                self._end = self.get_ind_under_point(event)
                if self._end == self._start:
                    # The mouse button was pressed (not dragged)
                    self._detns_idx = self.get_detns()
                    if self._fitdict['coeff'] is not None:
                        # Find closest line
                        waveest = self.fitsol_value(idx=self._detns_idx)
                        widx = np.argmin(np.abs(waveest-self._lines))
                        self.linelist_update(widx)
                        self._slidell.set_val(self._slideval)
                elif self._end != self._start:
                    # The mouse button was dragged
                    if axisID == 0:
                        if self._start > self._end:
                            tmp = self._start
                            self._start = self._end
                            self._end = tmp
                        self.update_regions()
        # Now plot
        trans = mtransforms.blended_transform_factory(self.axes['main'].transData, self.axes['main'].transAxes)
        self.canvas.restore_region(self.background)
        self.draw_fitregions(trans)
        # Now replot everything
        self.replot()

    def key_press_callback(self, event):
        """What to do when a key is pressed

        Args:
            event (Event): Matplotlib event instance containing information about the event

        Returns:
            None
        """
        # Check that the event is in an axis...
        if not event.inaxes:
            return
        # ... but not the information box!
        if event.inaxes == self.axes['info']:
            return
        axisID = self.get_axisID(event)
        self.operations(event.key, axisID)

    def operations(self, key, axisID):
        """Canvas operations

        Args:
            key (str): Which key has been pressed
            axisID (int): The index of the axis where the key has been pressed (see get_axisID)
        """
        # Check if the user really wants to quit
        if key == 'q' and self._qconf:
            if self._changes:
                self.update_infobox(message="WARNING: There are unsaved changes!!\nPress q again to exit", yesno=False)
                self._qconf = True
            else:
                msgs.bug("Need to change this to kill and return the results to PypeIt")
                plt.close()
        elif self._qconf:
            self.update_infobox(default=True)
            self._qconf = False

        # Manage responses from questions posed to the user.
        if self._respreq[0]:
            if key != "y" and key != "n":
                return
            else:
                # Switch off the required response
                self._respreq[0] = False
                # Deal with the response
                if self._respreq[1] == "write":
                    # First remove the old file, and save the new one
                    msgs.work("Not implemented yet!")
                    self.write()
                else:
                    return
            # Reset the info box
            self.update_infobox(default=True)
            return

        if key == '?':
            self.print_help()
        elif key == 'a':
            if self._fitdict['coeff'] is not None:
                self.auto_id()
            else:
                msgs.info("You must identify a few lines first")
        elif key == 'c':
            wclr = np.where((self._lineflg == 2) | (self._lineflg == 3))
            self._lineflg[wclr] = 0
            self.replot()
        elif key == 'd':
            self._lineflg *= 0
            self._lineids *= 0.0
            self._fitdict['coeff'] = None
            self.replot()
        elif key == 'f':
            self.fitsol_fit()
            self.replot()
        elif key == 'l':
            self.load_IDs()
        elif key == 'q':
            if self._changes:
                self.update_infobox(message="WARNING: There are unsaved changes!!\nPress q again to exit", yesno=False)
                self._qconf = True
            else:
                plt.close()
        elif key == 'r':
            if self._detns_idx == -1:
                msgs.info("You must select a line first")
            elif self._fitr is None:
                msgs.info("You must select a fitting region first")
            else:
                msgs.work("Feature not yet implemented")
        elif key == 's':
            self.save_IDs()
        elif key == 'w':
            self.toggle_wavepix(toggled=True)
            self.replot()
        elif key == 'z':
            self.delete_line_id()
        elif key == '+':
            if self._fitdict["polyorder"] < 10:
                self._fitdict["polyorder"] += 1
                self.update_infobox(message="Polynomial order = {0:d}".format(self._fitdict["polyorder"]), yesno=False)
                self.fitsol_fit()
                self.replot()
            else:
                self.update_infobox(message="Polynomial order must be <= 10", yesno=False)
        elif key == '-':
            if self._fitdict["polyorder"] > 1:
                self._fitdict["polyorder"] -= 1
                self.update_infobox(message="Polynomial order = {0:d}".format(self._fitdict["polyorder"]), yesno=False)
                self.fitsol_fit()
                self.replot()
            else:
                self.update_infobox(message="Polynomial order must be >= 1", yesno=False)
        self.canvas.draw()

    def auto_id(self):
        """Automatically assign lines based on a few lines identified by the user

        Using the current line IDs and approximate wavelength solution,
        automatically assign a wavelength to all line detections.
        """

        # If the IDs are within an acceptable tolerance, flag them as such
        wave_est = utils.func_val(self._fitdict['fitc'],
                                  self._detns / self._fitdict['xnorm'],
                                  self._fitdict["function"],
                                  minx=self._fitdict['fmin'],
                                  maxx=self._fitdict['fmax'])
        for wav in range(wave_est.size):
            if self._lineflg[wav] == 1:
                # User has manually identified this line already
                continue
            pixdiff = np.abs(wave_est[wav]-self._lines)
            amin = np.argmin(pixdiff)
            pxtst = pixdiff[amin]/self._fitdict['cen_disp']
            self._lineids[wav] = self._lines[amin]
            if pxtst < 0.1:
                # Acceptable
                self._lineflg[wav] = 2
            else:
                # Unacceptable
                self._lineflg[wav] = 3
        # Now that we've automatically identified lines, update the canvas
        self.replot()

    def delete_line_id(self):
        """Remove an incorrect line ID
        """
        rmid = self.get_detns()
        self._lineids[rmid] = 0.0
        self._lineflg[rmid] = 0

    def fitsol_value(self, xfit=None, idx=None):
        """Calculate the wavelength at a pixel

        Args:
            xfit (ndarray, float): Pixel values that the user wishes to evaluate the wavelength
            idx (int): Index of the arc line detections that the user wishes to evaluate the wavelength

        Returns:
            disp (ndarray, float, None): The wavelength (Angstroms) of the requested pixels
        """
        if xfit is None:
            xfit = self._detns
        if self._fitdict['coeff'] is not None:
            if idx is None:
                return np.polyval(self._fitdict["coeff"], xfit / self._fitdict["scale"])
            else:
                return np.polyval(self._fitdict["coeff"], xfit[idx] / self._fitdict["scale"])
        else:
            msgs.bug("Cannot predict wavelength value - no fit has been performed")
            return None

    def fitsol_deriv(self, xfit=None, idx=None):
        """Calculate the dispersion as a function of wavelength

        Args:
            xfit (ndarray, float): Pixel values that the user wishes to evaluate the wavelength
            idx (int): Index of the arc line detections that the user wishes to evaluate the wavelength

        Returns:
            disp (ndarray, float, None): The dispersion (Angstroms/pixel) as a function of wavelength
        """
        if xfit is None:
            xfit = self._detns
        if self._fitdict['coeff'] is not None:
            cder = np.polyder(self._fitdict["coeff"])
            if idx is None:
                return np.polyval(cder, xfit / self._fitdict["scale"]) / self._fitdict["scale"]
            else:
                return np.polyval(cder, xfit[idx] / self._fitdict["scale"]) / self._fitdict["scale"]
        else:
            msgs.bug("Cannot predict wavelength value - no fit has been performed")
            return None

    def fitsol_fit(self):
        """Perform a fit to the line identifications
        """
        # Calculate the dispersion
        # disp = (ids[-1] - ids[0]) / (tcent[idx_str[-1]] - tcent[idx_str[0]])
        # final_fit = fitting.iterative_fitting(censpec, tcent, idx_str, ids,
        #                                       llist, disp, verbose=False,
        #                                       n_first=2, n_final=self._fitdict["polyorder"])
        ord = self._fitdict["polyorder"]
        gd_det = np.where((self._lineflg == 1) | (self._lineflg == 2))  # Use the user IDs or acceptable auto IDs only!
        # Check if there are enough points to perform a fit
        if gd_det[0].size < ord+1:
            msg = "Polynomial order must be >= number of line IDs\n" +\
                  "Polynomial order = {0:d}, Number of line IDs = {1:d}".format(ord, gd_det[0].size)
            self.update_infobox(message=msg, yesno=False)
        else:
            # Start by performing a basic fit
            xpix = self._detns[gd_det] / self._fitdict["scale"]
            ylam = self._lineids[gd_det]
            self._fitdict["coeff"] = np.polyfit(xpix, ylam, ord)
            bdisp = self.fitsol_deriv(self.specdata.size / 2)  # Angstroms/pixel at the centre of the spectrum
            # Then try a detailed fit
            try:
                final_fit = fitting.iterative_fitting(self.specdata, self._detns, gd_det[0],
                                                      self._lineids[gd_det[0]], self._line_lists, bdisp,
                                                      verbose=False, n_first=min(2, self._fitdict["polyorder"]),
                                                      match_toler=self.par['match_toler'],
                                                      func=self.par['func'],
                                                      n_final=self._fitdict["polyorder"],
                                                      sigrej_first=self.par['sigrej_first'],
                                                      sigrej_final=self.par['sigrej_final'])
                # Update the fitdict
                for key in final_fit:
                    self._fitdict[key] = final_fit[key]

            except TypeError:
                # Just stick use the basic fit
                self._fitdict["fitc"] = None

    def update_infobox(self, message="Press '?' to list the available options",
                       yesno=True, default=False):
        """Send a new message to the information window at the top of the canvas

        Args:
            message (str): Message to be displayed
        """
        self.axes['info'].clear()
        if default:
            self.axes['info'].text(0.5, 0.5, "Press '?' to list the available options", transform=self.axes['info'].transAxes,
                          horizontalalignment='center', verticalalignment='center')
            self.canvas.draw()
            return
        # Display the message
        self.axes['info'].text(0.5, 0.5, message, transform=self.axes['info'].transAxes,
                      horizontalalignment='center', verticalalignment='center')
        if yesno:
            self.axes['info'].fill_between([0.8, 0.9], 0, 1, facecolor='green', alpha=0.5, transform=self.axes['info'].transAxes)
            self.axes['info'].fill_between([0.9, 1.0], 0, 1, facecolor='red', alpha=0.5, transform=self.axes['info'].transAxes)
            self.axes['info'].text(0.85, 0.5, "YES", transform=self.axes['info'].transAxes,
                          horizontalalignment='center', verticalalignment='center')
            self.axes['info'].text(0.95, 0.5, "NO", transform=self.axes['info'].transAxes,
                          horizontalalignment='center', verticalalignment='center')
        self.axes['info'].set_xlim((0, 1))
        self.axes['info'].set_ylim((0, 1))
        self.canvas.draw()

    def update_line_id(self):
        """Find the nearest wavelength in the linelist
        """
        if self._detns_idx != -1:
            self._lineids[self._detns_idx] = self._lines[self._slideval]
            self._lineflg[self._detns_idx] = 1

    def update_regions(self):
        """Update the regions used to fit Gaussian
        """
        self._fitregions[self._start:self._end] = self._addsub

    def load_IDs(self, fname='waveid.ascii'):
        """Load line IDs
        """
        if os.path.exists(fname):
            data = ascii_io.read(fname, format='fixed_width')
            self._detns = data['pixel']
            self._lineids = data['wavelength']
            self._lineflg = data['flag']
            msgs.info("Loaded line IDs:" + msgs.newline() + fname)
            self.update_infobox(message="Loaded line IDs: {0:s}".format(fname), yesno=False)
        else:
            self.update_infobox(message="Could not find line IDs: {0:s}".format(fname), yesno=False)

    def save_IDs(self, fname='waveid.ascii'):
        """Save the current IDs
        """
        meta = dict(comments=["flags:",
                              "   0 = wavelength has not been assigned to this detection",
                              "   1 = user has assigned wavelength to this detection",
                              "   2 = detection has been automatically assigned",
                              "   3 = automatically assigned wavelength was rejected"])
        data = Table({'pixel' : self._detns,
                      'wavelength' : self._lineids,
                      'flag' : self._lineflg},
                     names=['pixel', 'wavelength', 'flag'],
                     meta=meta)
        ascii_io.write(data, fname, format='fixed_width')
        msgs.info("Line IDs saved as:" + msgs.newline() + fname)
        self.update_infobox(message="Line IDs saved as: {0:s}".format(fname), yesno=False)


def initialise(arccen, slit=0, par=None):
    """Initialise the 'Identify' window for real-time wavelength calibration

        Args:
            arccen (ndarray): Arc spectrum
        slit (int): The slit to be used for wavelength calibration

        Returns:
            ident (Identify): Returns an instance of the Identify class, which contains the results of the fit

        Todo:
            * Implement multislit functionality
    """

    # Double check that a WavelengthSolutionPar was input
    par = pypeitpar.WavelengthSolutionPar() if par is None else par

    # Extract the lines that are detected in arccen
    tdetns, _, _, icut, _ = wvutils.arc_lines_from_spec(arccen[:, slit].copy(), sigdetect=par['sigdetect'],
                                                        nonlinear_counts=par['nonlinear_counts'])
    detns = tdetns[icut]

    # Load line lists
    if 'ThAr' in par['lamps']:
        line_lists_all = waveio.load_line_lists(par['lamps'])
        line_lists = line_lists_all[np.where(line_lists_all['ion'] != 'UNKNWN')]
    else:
        line_lists = waveio.load_line_lists(par['lamps'])

    # Create a Line2D instance for the arc spectrum
    spec = Line2D(np.arange(arccen.size), arccen,
                  linewidth=1, linestyle='solid', color='k',
                  drawstyle='steps', animated=True)

    # Add the main figure axis
    fig, ax = plt.subplots(figsize=(16, 9), facecolor="white")
    plt.subplots_adjust(bottom=0.05, top=0.85, left=0.05, right=0.65)
    ax.add_line(spec)
    ax.set_ylim((0.0, 1.1*spec.get_ydata().max()))

    # Add two residual fitting axes
    axfit = fig.add_axes([0.7, .5, .28, 0.35])
    axres = fig.add_axes([0.7, .1, .28, 0.35])
    # Residuals
    lflag_color = ['grey', 'blue', 'yellow', 'red']
    residcmap = LinearSegmentedColormap.from_list("my_list", lflag_color, N=len(lflag_color))
    resres = axres.scatter(detns, np.zeros(detns.size), marker='x',
                            c=np.zeros(detns.size), cmap=residcmap, norm=Normalize(vmin=0.0, vmax=3.0))
    axres.axhspan(-0.1, 0.1, alpha=0.5, color='grey')  # Residuals of 0.1 pixels
    axres.axhline(0.0, color='r', linestyle='-')  # Zero level
    axres.set_xlim((0, arccen.size - 1))
    axres.set_ylim((-0.3, 0.3))
    axres.set_xlabel('Pixel')
    axres.set_ylabel('Residuals (Pix)')

    # pixel vs wavelength
    respts = axfit.scatter(detns, np.zeros(detns.size), marker='x',
                            c=np.zeros(detns.size), cmap=residcmap, norm=Normalize(vmin=0.0, vmax=3.0))
    resfit = Line2D(np.arange(arccen.size), np.zeros(arccen.size), linewidth=1, linestyle='-', color='r')
    axfit.add_line(resfit)
    axfit.set_xlim((0, arccen.size - 1))
    axfit.set_ylim((-0.3, 0.3))  # This will get updated as lines are identified
    axfit.set_xlabel('Pixel')
    axfit.set_ylabel('Wavelength')

    # Add an information GUI axis
    axinfo = fig.add_axes([0.15, .92, .7, 0.07])
    axinfo.get_xaxis().set_visible(False)
    axinfo.get_yaxis().set_visible(False)
    axinfo.text(0.5, 0.5, "Press '?' to list the available options", transform=axinfo.transAxes,
             horizontalalignment='center', verticalalignment='center')
    axinfo.set_xlim((0, 1))
    axinfo.set_ylim((0, 1))
    specres = dict(pixels=respts, model=resfit, resid=resres)

    axes = dict(main=ax, fit=axfit, resid=axres, info=axinfo)
    # Initialise the identify window and display to screen
    fig.canvas.set_window_title('PypeIt - Identify')
    ident = Identify(fig.canvas, axes, spec, specres, detns, line_lists, par, lflag_color, slit=slit)
    plt.show()

    # Now return the results
    return ident

