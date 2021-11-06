from julia import JuliaSet, OutputConfig, Seed
import numpy as np
import matplotlib.animation as animation

def sample_1():
    cfg = OutputConfig(-2, -2, 4, 4, 200, 50)
    seed = Seed.asAnimated(0.7885, 360, (lambda f: np.linspace(0, 2*np.pi, f)))

    j = JuliaSet(cfg, seed)
    anim = j.get_animated()

    Writer = animation.writers['ffmpeg']
    writer = Writer(fps=30, metadata=dict(artist='Raymond'), bitrate=3600)
    anim.save('julia_set_sample1.mp4', writer=writer)

def main():
    sample_1()

if __name__ == "__main__":
    main()