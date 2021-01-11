import matplotlib.pyplot as plt

def set_default_plot_params():
    """
    Sets default parameters in the matplotlibrc.
    :return: None
    """
    xtick = {
        'top': True,
        'minor.visible': True,
        'direction': 'in',
        'labelsize': 10
    }

    ytick = {
        'right': True,
        'minor.visible': True,
        'direction': 'in',
        'labelsize': 10
    }

    axes = {
        'labelsize': 12,
        #"prop_cycle": tango_color_cycler,
        'formatter.limits': (-4, 4),
        'formatter.use_mathtext': True,
        'titlesize': 'large',
        'labelpad': 4.0,
    }
    lines = {
        'lw': 1.5
    }
    legend = {
        'frameon': False
    }
    errorbar = {
        'capsize': 0
    }

    plt.rc('lines', **lines)
    plt.rc('axes', **axes)
    plt.rc('xtick', **xtick)
    plt.rc('ytick', **ytick)
    plt.rc('legend', **legend)
    plt.rc('errorbar', **errorbar)