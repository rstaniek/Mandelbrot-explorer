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
        i = 0       
        #for i in range(width):
        while i < width:
            #for j in range(height):
            j = 0
            while j < height:
                #mandelbrot actual calculation happening here
                z = r1[i] + 1j*r2[j]
                c = z
                n = 0
                #for n in range(maxiter):
                while n < maxiter:
                    az = abs(z)
                    if az > horizon:
                        n3[i,j] = n - np.divide(np.log(np.log(az)), np.log(2)) + log_horizon
                        break
                    z = z*z + c
                    n = n + 1
                j = j + 1
            i = i + 1
        return (r1,r2,n3)

from matplotlib import pyplot as plt
from matplotlib import colors
import time

class Coordinates():
    xmin_base = -2.0
    xmax_base = 0.5
    ymin_base = -1.25
    ymax_base = 1.25
    DPI = 72

    def __init__(self, xmin, xmax, ymin, ymax, *args, **kwargs):
        self.xmin = xmin
        self.ymin = ymin
        self.xmax = xmax
        self.ymax = ymax
        self.dim_w = 0
        self.dim_h = 0
        return super().__init__(*args, **kwargs)

    def __str__(self):
        return 'Coordinates:\n\txmin:\t{}\n\txmax:\t{}\n\tymin:\t{}\n\tymax:\t{}'.format(self.xmin, self.xmax, self.ymin, self.ymax)

    @classmethod
    def from_values(cls, offset_x=0, offset_y=0, zoom_level=1):
        xmin = np.divide(Coordinates.xmin_base, zoom_level) + offset_x
        xmax = np.divide(Coordinates.xmax_base, zoom_level) + offset_x
        ymin = np.divide(Coordinates.ymin_base, zoom_level) + offset_y
        ymax = np.divide(Coordinates.ymax_base, zoom_level) + offset_y
        return cls(xmin, xmax, ymin, ymax)


    def set_img_dim(self, w, h):
        self.dim_h = h
        self.dim_w = w

    def recalculate_coordinates(self, center_x, center_y, zoom):
        center_x = np.rint(center_x)
        center_y = np.rint(center_y)
        ### for now zoom in doesn't really work yet
        # self.xmin = np.divide(self.xmin, zoom)
        # self.xmax = np.divide(self.xmax, zoom)
        # self.ymin = np.divide(self.ymin, zoom)
        # self.ymax = np.divide(self.ymax, zoom)
        offset_x = np.divide(np.multiply((self.dim_w * Coordinates.DPI / 2) - center_x, self.xmax - self.xmin), self.dim_w * Coordinates.DPI)
        offset_y = np.divide(np.multiply((self.dim_h * Coordinates.DPI / 2) - center_y, self.ymax - self.ymin), self.dim_h * Coordinates.DPI)
        self.xmin = self.xmin - offset_x
        self.xmax = self.xmax - offset_x
        self.ymin = self.ymin - offset_y
        self.ymax = self.ymax - offset_y

class Mandelbrot():
        
    def __init__(self, *args, **kwargs):
        self.image_counter = 1
        self.fig = None
        self.ax = None
        self.coord = None
        self.maxiter = None
        self.cmap = None
        self.gamma = None
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

    def _on_mouse_click(self, event):
        x= event.xdata
        y= event.ydata
        if x is not None and y is not None:
            self.coord.recalculate_coordinates(x, y, 1)
            print('\n\nCalculating new region with the following values:\n{}\nw:\t{}\nh:\t{}\niter:\t{}\ncmap:\t{}\ngamma:\t{}'.format(self.coord, self.coord.dim_w, self.coord.dim_h, self.maxiter, self.cmap, self.gamma))
            self.close_all_figs()
            self.mandelbrot_coord(self.coord, self.coord.dim_w, self.coord.dim_h, self.maxiter, self.cmap, self.gamma)
            self.showfig()

    def mandelbrot_img(self, xmin,xmax,ymin,ymax,width=10,height=10, maxiter=2048,cmap='jet',gamma=0.3, showborder=False):
        dpi = Coordinates.DPI
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
            plt.axis('off')
        
        norm = colors.PowerNorm(gamma)
        ax.imshow(z.T,cmap=cmap,origin='lower',norm=norm)  
        
        fig.canvas.mpl_connect('button_press_event', self._on_mouse_click)

        self.fig = fig
        self.ax = ax
        #self.save_image(fig, showborder)

    def mandelbrot_coord(self, coordinates, width=10, height=10, maxiter=2048, cmap='magma', gamma=0.3, showborder=True):
        self.coord = coordinates
        self.coord.set_img_dim(width, height)
        self.maxiter = maxiter
        self.cmap = cmap
        self.gamma = gamma
        self.mandelbrot_img(coordinates.xmin, coordinates.xmax, coordinates.ymin, coordinates.ymax, width, height, maxiter, cmap, gamma, showborder)
