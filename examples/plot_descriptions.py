import b2style
import matplotlib.pyplot as plt

b2fig = b2style.B2Figure()
fig, ax = b2fig.create_figure(n_x_subfigures=2)

b2fig.add_descriptions(ax=ax[0], small_title=True, simulation=True)
b2fig.add_descriptions(ax=ax[1], small_title=True, simulation=True)

plt.show()