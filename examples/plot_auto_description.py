import b2style
import matplotlib.pyplot as plt

description = {"simulation": True, "luminosity": 100}
b2fig = b2style.B2Figure(auto_description=True, description=description)

fig, ax = b2fig.create(n_x_subfigures=1, figsize=(15,10))

ax.set_xlabel("x-axis in arb. units")
ax.set_ylabel("y-axis in arb. units")
ax.grid(True)
plt.show()