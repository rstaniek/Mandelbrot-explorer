from numba import jit
import numpy as np

class MandelbrotJIT():

    @staticmethod
    @jit(parallel=True, nopython=True)
    def mandelbrot_set(xmin,xmax,ymin,ymax,width,height,maxiter):
        horizon = 2.0 ** 40
        log_horizon = np.log(np.log(horizon))/np.log(2)
        r1 = np.linspace(xmin, xmax, width)
        r2 = np.linspace(ymin, ymax, height)
        n3 = np.empty((width,height))
        for i in range(width):
            for j in range(height):
                #mandelbrot actual calculation happening here
                z = r1[i] + 1j*r2[j]
                c = z
                for n in range(maxiter):
                    az = abs(z)
                    if az > horizon:
                        n3[i,j] = n - np.divide(np.log(np.log(az)), np.log(2)) + log_horizon
                        break
                    z = z*z + c
        return (r1,r2,n3)

from matplotlib import pyplot as plt
from matplotlib import colors
import time

class Coordinates():
    xmin_base = -2.0
    xmax_base = 0.5
    ymin_base = -1.25
    ymax_base = 1.25

    def __init__(self, xmin, xmax, ymin, ymax, *args, **kwargs):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        return super().__init__(*args, **kwargs)

    @classmethod
    def from_values(cls, offset_x=0, offset_y=0, zoom_level=1):
        xmin = np.divide(Coordinates.xmin_base, zoom_level) + offset_x
        xmax = np.divide(Coordinates.xmax_base, zoom_level) + offset_x
        ymin = np.divide(Coordinates.ymin_base, zoom_level) + offset_y
        ymax = np.divide(Coordinates.ymax_base, zoom_level) + offset_y
        return cls(xmin, xmax, ymin, ymax)

class Mandelbrot():
        
    def __init__(self, *args, **kwargs):
        self.image_counter = 1
        self.fig = None
        self.ax = None
        return super().__init__(*args, **kwargs)
    
    def save_image(self, fig, showborder=False):
        filename = "images/mandelbrodt_%d.png" % self.image_counter
        self.image_counter += 1
        if showborder:
            fig.savefig(filename)
        else:
            fig.savefig(filename, bbox_inches='tight', pad_inches = 0)

    def save_visualization(self):
        filename = "images\mandelbrodt_%s.png" % time.strftime("%d-%m-%Y")
        self.ax.set_axis_off()
        self.ax.xaxis.set_major_locator(plt.NullLocator())
        self.ax.yaxis.set_major_locator(plt.NullLocator())
        self.ax.set_frame_on(False)
        self.fig.savefig(filename, bbox_inches='tight', pad_inches = 0)
        return filename

    def showfig(self):
        self.fig.show()

    def close_all_figs(self):
        plt.close('all')

    def mandelbrot_img(self, xmin,xmax,ymin,ymax,width=10,height=10, maxiter=2048,cmap='jet',gamma=0.3, showborder=False):
        dpi = 72
        img_width = dpi * width
        img_height = dpi * height
        x,y,z = MandelbrotJIT.mandelbrot_set(xmin,xmax,ymin,ymax,img_width,img_height,maxiter)
        
        fig, ax = plt.subplots(figsize=(width, height),dpi=72)
        ticks = np.arange(0,img_width,3*dpi)
        x_ticks = xmin + (xmax-xmin)*ticks/img_width
        plt.xticks(ticks, x_ticks)
        y_ticks = ymin + (ymax-ymin)*ticks/img_width
        plt.yticks(ticks, y_ticks)
        if not showborder:
            ax.set_axis_off()
            ax.xaxis.set_major_locator(plt.NullLocator())
            ax.yaxis.set_major_locator(plt.NullLocator())
            ax.set_frame_on(False)
        
        norm = colors.PowerNorm(gamma)
        ax.imshow(z.T,cmap=cmap,origin='lower',norm=norm)  
        
        self.fig = fig
        self.ax = ax
        #self.save_image(fig, showborder)

    def mandelbrot_coord(self, coordinates, width=10, height=10, maxiter=2048, cmap='magma', gamma=0.3, showborder=True):
        self.mandelbrot_img(coordinates.xmin, coordinates.xmax, coordinates.ymin, coordinates.ymax, width, height, maxiter, cmap, gamma, showborder)
