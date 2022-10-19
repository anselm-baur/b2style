import b2style
import matplotlib.pyplot as plt
import numpy as np

data = np.random.normal(size=10000)
mc = np.random.normal(size=10000)

hist_args = {"bins": 100,
             "range": [-10,10]}
data_hist = np.histogram(data, **hist_args)
mc_hist = np.histogram(mc, **hist_args)

description_args = {"simulation": True,
                    "small_title": True}
b2fig = b2style.B2Figure(auto_description=True, description=description_args)

fig, ax = b2fig.create_pull_plot(sharex=True)
x = b2fig.get_bincenters_of_binedges(data_hist[1])
b2fig.plot_errorbar(ax[0], x, data_hist[0], mc_hist[0])
b2fig.pull_plot(ax[1], data_hist[0], mc_hist[0], bin_edges=data_hist[1], is_hist=True)
#ax[0].errorbar(b2fig.get_bincenters_of_binedges(mc_hist[1]), mc_hist[0])

ax[1].set_xlabel("x label")
ax[0].set_ylabel("events")
ax[1].set_ylabel(r"$\frac{\mathrm{\mathbf{data}}-\mathrm{\mathbf{mc}}}{\mathrm{\mathbf{data}}}$")

#ax[1].sharex(ax[0])
#ax[0].get_xaxis().set_visible(False)


b2fig.save(fig, "pull_plot", add_date=False)
#plt.show()