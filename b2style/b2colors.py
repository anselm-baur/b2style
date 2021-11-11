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

class PhDColors(object):
    """
    Provides PhD colors.
    """
    green = '#73d216'
    dark_green = '#4e9a06'
    blue = '#3465a4'
    yellow = '#edd400'
    orange = '#f57900'
    brown = '#c17d11'
    red = '#cc0000'
    purple = '#75507b'
    black = '#000000'
    light_grey = '#babdb6'
    grey = '#555753'

    default_colors_dict = {
        'green': green,
        'dark_green': dark_green,
        'blue': blue,
        'yellow': yellow,
        'orange': orange,
        'brown': brown,
        'red': red,
        'purple': purple,
        'black': black,
        'light_grey': light_grey,
        'grey': grey,
        }

    default_colors = [
        blue,
        orange,
        dark_green,
        red,
        purple,
        brown,
        yellow,
        grey,
        light_grey,
        green,
        black
    ]



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


def set_default_colors(color_set='phd'):
    if color_set == 'phd':
        color_cycler = cycler("color", PhDColors.default_colors)
        B2Colors.color = PhDColors.default_colors_dict
    if color_set == 'kit':
        color_cycler = cycler("color", KITColors.default_colors)
        B2Colors.color = KITColors.default_colors_dict
    if color_set == 'reset':
        color_cycler = cycler("color", DefaultColors.default_colors)
        B2Colors.color = DefaultColors.default_colors_dict
    plt.rc('axes', prop_cycle=color_cycler)
