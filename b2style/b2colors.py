import matplotlib.pyplot as plt
from cycler import cycler


class B2Colors(object):
    color = {}

class DefaultColors(object):
    default_colors_dict = {
        'green': 'green',
        'blue': 'blue',
        'maygreen': 'maygreen',
        'yellow': 'yellow',
        'orange': 'orange',
        'brown': 'brown',
        'red': 'red',
        'purple': 'purple',
        'cyan': 'cyan',
        'black': 'black',
        'light_grey': 'light_grey',
        'grey': 'grey',
        'dark_grey': 'dark_grey'
        }

    default_colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']


class KITColors(object):
    """
    Provides the KIT colors.
    """
    green = '#009682'
    blue = '#4664aa'
    maygreen = '#8cb63c'
    yellow = '#fce500'
    orange = '#df9b1b'
    brown = '#a7822e'
    red = '#a22223'
    purple = '#a3107c'
    cyan = '#23a1e0'
    black = '#000000'
    light_grey = '#bdbdbd'
    grey = '#797979'
    dark_grey = '#4e4e4e'

    default_colors_dict = {
        'green': green,
        'blue': blue,
        'maygreen': maygreen,
        'yellow': yellow,
        'orange': orange,
        'brown': brown,
        'red': red,
        'purple': purple,
        'cyan': cyan,
        'black': black,
        'light_grey': light_grey,
        'grey': grey,
        'dark_grey': dark_grey
        }

    default_colors = [
        blue,
        orange,
        maygreen,
        red,
        purple,
        brown,
        yellow,
        dark_grey,
        cyan,
        green,
    ]


def set_default_colors(color_set='kit'):
    if color_set == 'kit':
        color_cycler = cycler("color", KITColors.default_colors)
        B2Colors.color = KITColors.default_colors_dict
    if color_set == 'reset':
        color_cycler = cycler("color", DefaultColors.default_colors)
        B2Colors.color = DefaultColors.default_colors_dict
    plt.rc('axes', prop_cycle=color_cycler)
