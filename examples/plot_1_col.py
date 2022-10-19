import b2style
import matplotlib.pyplot as plt

b2fig = b2style.B2Figure(bold_labels=False)
fig, ax = b2fig.create(n_x_subfigures=1, figsize=(15,10))

b2fig.add_descriptions(ax=ax, small_title=True, simulation=True, luminosity=100)

ax.set_xlabel("x-axis in arb. units")
ax.set_ylabel("y-axis in arb. units")
ax.grid(True)
plt.show()