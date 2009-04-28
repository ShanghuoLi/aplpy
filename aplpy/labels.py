import matplotlib.pyplot as mpl
import math
import angle_util as au
import wcs_util
import numpy as np
import string
import math_util

class Labels(object):
    
    def _initialize_labels(self):
        
        self._ax2.yaxis.set_label_position('right')
        self._ax2.xaxis.set_label_position('top')
        
        system,equinox,units = wcs_util.system(self._wcs)
        
        # Set default label format
        if system == 'celestial':
            self._ax1.xaxis.apl_label_form = "hh:mm:ss."
            self._ax1.yaxis.apl_label_form = "sdd:mm:ss."
        else:
            self._ax1.xaxis.apl_label_form = "ddd.dddd"
            self._ax1.yaxis.apl_label_form = "dd.dddd"
        
        if system == 'celestial':
            if equinox == 'b1950':
                self._ax1.set_xlabel('RA (B1950)')
                self._ax1.set_ylabel('Dec (B1950)')
            else:
                self._ax1.set_xlabel('RA (J2000)')
                self._ax1.set_ylabel('Dec (J2000)')
        elif system == 'galactic':
            self._ax1.set_xlabel('Galactic Longitude')
            self._ax1.set_ylabel('Galactic Latitude')
        else:
            self._ax1.set_xlabel('Ecliptic Longitude')
            self._ax1.set_ylabel('Ecliptic Latitude')
        
        # Set major tick formatters
        fx1 = WCSFormatter(wcs=self._wcs,axist='x')
        fy1 = WCSFormatter(wcs=self._wcs,axist='y')
        self._ax1.xaxis.set_major_formatter(fx1)
        self._ax1.yaxis.set_major_formatter(fy1)
        
        fx2 = mpl.NullFormatter()
        fy2 = mpl.NullFormatter()
        self._ax2.xaxis.set_major_formatter(fx2)
        self._ax2.yaxis.set_major_formatter(fy2)
    
    def set_xlabels_format(self,format,refresh=True):
        '''
        Set the format of the x-axis tick labels
        
        Required Arguments:
        
            *format*: [ string ]
                The format for the tick labels. This can be:

                    * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
                    * ``hh`` or ``dd`` - hours (or degrees)
                    * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
                    * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
                    * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied. 
                    
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.                                         
        '''
        
        self._ax1.xaxis.apl_label_form = format
        if refresh: self.refresh()
    
    def set_ylabels_format(self,format,refresh=True):
        '''
        Set the format of the x-axis tick labels
        
        Required Arguments:
        
            *format*: [ string ]
                The format for the tick labels. This can be:

                    * ``ddd.ddddd`` - decimal degrees, where the number of decimal places can be varied
                    * ``hh`` or ``dd`` - hours (or degrees)
                    * ``hh:mm`` or ``dd:mm`` - hours and minutes (or degrees and arcminutes)
                    * ``hh:mm:ss`` or ``dd:mm:ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds)
                    * ``hh:mm:ss.ss`` or ``dd:mm:ss.ss`` - hours, minutes, and seconds (or degrees, arcminutes, and arcseconds), where the number of decimal places can be varied.  
            
        Optional Keyword Arguments:

            *refresh*: [ True | False ]
                Whether to refresh the display straight after setting the parameter.
                For non-interactive uses, this can be set to False.            
        '''
        
        self._ax1.yaxis.apl_label_form = format
        if refresh: self.refresh()
    
    def set_axis_labels(self,refresh=True,family='serif',fontsize='12',fontstyle='normal'):
        """
        family                [ 'serif' | 'sans-serif' | 'cursive' | 'fantasy' | 'monospace' ]
          size or fontsize    [ size in points | relative size eg 'smaller', 'x-large' ]
          style or fontstyle    [ 'normal' | 'italic' | 'oblique']
        """
        self._ax1.set_xlabel('(R.A. J2000)',family=family,fontsize=fontsize,fontstyle=fontstyle)
        self._ax1.set_ylabel('(Dec. J2000)',family=family,fontsize=fontsize,fontstyle=fontstyle)
        
        if refresh: self.refresh()

class WCSFormatter(mpl.Formatter):
    
    def __init__(self, wcs=False,axist='x'):
        self._wcs = wcs
        self.axist = axist
    
    def __call__(self,x,pos=None):
        'Return the format for tick val x at position pos; pos=None indicated unspecified'
        
        hours = 'h' in self.axis.apl_label_form
        
        if hours:
            sep = ('h','m','s')
        else:
            sep = ('d','m','s')
        
        ymin, ymax = self.axis.get_axes().yaxis.get_view_interval()
        xmin, xmax = self.axis.get_axes().xaxis.get_view_interval()
            
        ipos = math_util.minloc(np.abs(self.axis.apl_tick_positions_pix-x))
        
        c = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[ipos]

        if hours:
            c = c.tohours()
        
        c = c.tostringlist(format=self.axis.apl_label_form,sep=sep)
        
        if ipos <> len(self.axis.apl_tick_positions_pix)-1:
            cnext = self.axis.apl_tick_spacing * self.axis.apl_tick_positions_world[ipos+1]
            if hours:
                cnext = cnext.tohours()
            cnext = cnext.tostringlist(format=self.axis.apl_label_form,sep=sep)
            for iter in range(len(c)):
                if cnext[0] == c[0]:
                    c.pop(0)
                    cnext.pop(0)
                else:
                    break
            
        return string.join(c,"")
