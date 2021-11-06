from julia import JuliaSet, OutputConfig
import matplotlib.pyplot as plt
import numpy as np

def sample_og():
    cfg = OutputConfig(-2, -2, 4, 4, 500, 50, True, 14, 14)

    # we represent c as c = r*cos(a) + i*r*sin(a) = r*e^{i*a}
    r = 0.7885
    a = 2 * np.pi / 4.
    cx, cy = r * np.cos(a), r * np.sin(a)

    j = JuliaSet(cfg)
    ax = j.get_static(cx, cy)
    plt.show()

def sample_1():
    cfg = OutputConfig(-1, -0.5, 1, 1, 2000, 200, True, 14, 14)

    # we represent c as c = r*cos(a) + i*r*sin(a) = r*e^{i*a}
    r = 0.7885
    a = 2 * np.pi / 2.3
    cx, cy = r * np.cos(a), r * np.sin(a)

    j = JuliaSet(cfg)
    ax = j.get_static(cx, cy)
    plt.show()

def main():
    sample_og()

if __name__ == "__main__":
    main()