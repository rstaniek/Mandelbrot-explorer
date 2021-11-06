import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from numba import jit

plt.rcParams['animation.ffmpeg_path'] = 'ffmpeg'

class JuliaJIT():
    @staticmethod
    @jit(parallel=True, nopython=True)
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
    def __init__(self, xmin, ymin, w: int, h: int, density: int, threshold: int, show_axes = True, ww = 10, wh = 10) -> None:
        self.xmin = xmin
        self.ymin = ymin

        self.x_offset = w
        self.y_offset = h

        self.density = density #pixles per unit
        self.threshold = threshold #maximum number of iterations

        self.show_axes = show_axes
        self.window_width = ww
        self.window_height = wh

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

def run_static(cfg: OutputConfig, cx, cy) -> None:
    X = np.empty((len(cfg.real), len(cfg.imaginary)))  # the initial array-like image

    for i in range(len(cfg.real)):
        for j in range(len(cfg.imaginary)):
            X[i, j] = JuliaJIT.julia_q(cfg.real[i], cfg.imaginary[j], cx, cy, cfg.threshold)

    fig = plt.figure(figsize=(cfg.window_width, cfg.window_height))

    ax = plt.axes()

    if not cfg.show_axes:
        ax.set_axis_off()
        ax.xaxis.set_major_locator(plt.NullLocator())
        ax.yaxis.set_major_locator(plt.NullLocator())
        ax.set_frame_on(False)
        plt.axis('off')

    ax.imshow(X.T, interpolation="hanning", cmap='magma')
    plt.show()

def static_sample():
    cfg = OutputConfig(-2, -2, 4, 4, 800, 50, False, 12, 12)

    # we represent c as c = r*cos(a) + i*r*sin(a) = r*e^{i*a}
    r = 0.7885
    a = 2 * np.pi / 4.
    cx, cy = r * np.cos(a), r * np.sin(a)

    run_static(cfg, cx, cy)

def animate(frame:int, ax: plt.Axes, cfg: OutputConfig, seed: Seed) -> list:
    ax.clear()
    ax.set_axis_off()
    ax.xaxis.set_major_locator(plt.NullLocator())
    ax.yaxis.set_major_locator(plt.NullLocator())
    ax.set_frame_on(False)
    plt.axis('off')

    X = np.empty((len(cfg.real), len(cfg.imaginary)))  # the initial array-like image
    cx, cy = seed.r * np.cos(seed.a[frame]), seed.r * np.sin(seed.a[frame])

    for i in range(len(cfg.real)):
        for j in range(len(cfg.imaginary)):
            X[i, j] = JuliaJIT.julia_q(cfg.real[i], cfg.imaginary[j], cx, cy, cfg.threshold)
    img = ax.imshow(X.T, interpolation='hamming', cmap='viridis')
    print("Frame {0} out of {1} rendered.".format(frame, seed.frames))
    return [img]


def run_animated(cfg: OutputConfig, seed: Seed) -> animation.FuncAnimation:
    fig = plt.figure(figsize=(cfg.window_width, cfg.window_height))
    ax = plt.axes()

    anim = animation.FuncAnimation(fig, (lambda _Frame, ax=ax, cfg=cfg, seed=seed: animate(_Frame, ax, cfg, seed)), frames=seed.frames, interval=50, blit=True)
    return anim

def animation_sample():
    cfg = OutputConfig(-2, -2, 4, 4, 200, 50)
    seed = Seed.asAnimated(0.7885, 360, (lambda f: np.linspace(0, 2*np.pi, f)))
    anim = run_animated(cfg, seed)

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30, metadata=dict(artist='Raymond'), bitrate=3600)
    anim.save('julia_set.mp4', writer=writer)

def main():
    static_sample()

if __name__ == "__main__":
    main()