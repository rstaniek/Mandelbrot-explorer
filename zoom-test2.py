import matplotlib.pyplot as plt

#
# Some toy data
x_seq = [x / 100.0 for x in range(1, 100)]
y_seq = [x**2 for x in x_seq]

#
# Scatter plot
fig, ax = plt.subplots(1, 1)
ax.scatter(x_seq, y_seq)

#
# Declare and register callbacks
def on_xlims_change(axes):
    print("updated xlims: " + str(ax.get_xlim()))

def on_ylims_change(axes):
    print("updated ylims: " + str(ax.get_ylim()))

ax.callbacks.connect('xlim_changed', on_xlims_change)
ax.callbacks.connect('ylim_changed', on_ylims_change)

#
# Show
plt.show()