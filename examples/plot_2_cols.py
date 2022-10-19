import b2style
import matplotlib.pyplot as plt

b2fig = b2style.B2Figure(bold_labels=False)
fig, ax = b2fig.create(n_x_subfigures=2)

b2fig.add_descriptions(ax=ax[0], small_title=True, simulation=True, luminosity=100)
b2fig.add_descriptions(ax=ax[1], small_title=True, simulation=True)

ax = ax[0]
ax.set_xlabel("x-axis in arb. units")
ax.set_ylabel("y-axis in arb. units")
plt.show()