from numba.core.typing import templates
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import jit
from numba import cuda
#from memoize import Memoize

import warnings
warnings.filterwarnings('ignore')

plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg'

@jit(None, {}, target='cuda')
def julia_set(real, imaginary, width, height, cx, cy, threshold, X):
    i = 0
    while i < width:
        j = 0
        while j < height:
            t = 0
            z = real[i] + 1j*imaginary[j]
            c = cx + 1j*cy
            while t < threshold:
                z = z * z + c

                # az = z
                # tmp = z >> 31
                # az ^= tmp
                # az += tmp & 1
                az = abs(z)

                if az > 4.:
                    X[i, j] = t
                    break
                t = t + 1
            X[i, j] = threshold - 1
            j = j + 1
        i = i + 1

class JuliaJIT():
    @staticmethod
    @cuda.jit
    def julia_set(real, imaginary, width, height, cx, cy, threshold, X):
        i = 0
        while i < width:
            j = 0
            while j < height:
                t = 0
                z = real[i] + 1j*imaginary[j]
                c = cx + 1j*cy
                while t < threshold:
                    z = z * z + c

                    # az = z
                    # tmp = z >> 31
                    # az ^= tmp
                    # az += tmp & 1
                    az = abs(z)

                    if az > 4.:
                        X[i, j] = t
                        break
                    t = t + 1
                X[i, j] = threshold - 1
                j = j + 1
            i = i + 1

    @staticmethod
    #@Memoize
    def julia_q(zx, zy, cx, cy, threshold) -> int:
        z = zx + 1j*zy
        c = cx + 1j*cy
        i = 0

        while(i < threshold):
            z = z * z + c
            az = abs(z)
            if az > 4.:
                return i
            i = i + 1
        return threshold - 1

class OutputConfig():
    def __init__(self, xmin, ymin, w: float, h: float, density: int, threshold: int, show_axes = True, ww = 10, wh = 10, color = 'magma') -> None:
        self.xmin = xmin
        self.ymin = ymin

        self.x_offset = w
        self.y_offset = h

        self.density = density #pixles per unit
        self.threshold = threshold #maximum number of iterations

        self.show_axes = show_axes
        self.window_width = ww
        self.window_height = wh
        self.color = color

        self.real = np.linspace(self.xmin, self.xmin + self.x_offset, self.x_offset * self.density)
        self.imaginary = np.linspace(self.ymin, self.ymin + self.y_offset, self.y_offset * self.density)

class Seed():
    def __init__(self, r, a = None, frames = None) -> None:
        self.r = r
        self.a = a
        self.frames = frames

    @classmethod
    def asStatic(cls, r, a):
        return cls(r, a)

    @classmethod
    def asAnimated(cls, r, frames, a_fn):
        a = a_fn(frames)
        return cls(r, a, frames)

class JuliaSet():
    def __init__(self, cfg: OutputConfig, seed: Seed = None) -> None:
        self.cfg = cfg
        self.seed = seed

    def get_static(self, cx, cy) -> plt.Axes:
        X = np.empty((len(self.cfg.real), len(self.cfg.imaginary)))  # the initial array-like image
        width = len(self.cfg.real)
        height = len(self.cfg.imaginary)

        # for i in range(len(self.cfg.real)):
        #     for j in range(len(self.cfg.imaginary)):
        #         X[i, j] = JuliaJIT.julia_q(self.cfg.real[i], self.cfg.imaginary[j], cx, cy, self.cfg.threshold)

        real = np.asarray(self.cfg.real)
        imaginary = np.asarray(self.cfg.imaginary)
        JuliaJIT.julia_set(real, imaginary, width, height, cx, cy, self.cfg.threshold, X)

        plt.figure(figsize=(self.cfg.window_width, self.cfg.window_height))

        ax = plt.axes()

        if not self.cfg.show_axes:
            ax.set_axis_off()
            ax.xaxis.set_major_locator(plt.NullLocator())
            ax.yaxis.set_major_locator(plt.NullLocator())
            ax.set_frame_on(False)
            plt.axis('off')

        ax.imshow(X.T, interpolation="hanning", cmap=self.cfg.color)
        return ax

    def __animate(self, frame:int, ax: plt.Axes) -> list:
        ax.clear()
        ax.set_axis_off()
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        ax.set_frame_on(False)
        plt.axis('off')

        X = np.empty((len(self.cfg.real), len(self.cfg.imaginary)))  # the initial array-like image
        cx, cy = self.seed.r * np.cos(self.seed.a[frame]), self.seed.r * np.sin(self.seed.a[frame])

        for i in range(len(self.cfg.real)):
            for j in range(len(self.cfg.imaginary)):
                X[i, j] = JuliaJIT.julia_q(self.cfg.real[i], self.cfg.imaginary[j], cx, cy, self.cfg.threshold)
        img = ax.imshow(X.T, interpolation='hanning', cmap=self.cfg.color)
        print("Frame {0} out of {1} rendered.".format(frame, self.seed.frames))
        return [img]

    def get_animated(self, initseed: Seed = None) -> animation.FuncAnimation:
        if initseed is not None:
            self.seed = initseed
        fig = plt.figure(figsize=(self.cfg.window_width, self.cfg.window_height))
        ax = plt.axes()

        anim = animation.FuncAnimation(fig, (lambda _Frame, ax=ax, cfg=self.cfg, s=self.seed: JuliaSet.__animate(_Frame, ax, cfg, s)), frames=self.seed.frames, interval=50, blit=True)
        return anim
