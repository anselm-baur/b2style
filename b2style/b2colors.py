import matplotlib.pyplot as plt
import matplotlib as mpl
from cycler import cycler
import numpy as np
from matplotlib.colors import LinearSegmentedColormap
import copy

class B2Colors(object):
    color = {}
    cm = {}

    def __init__(self):
        #print(f"available colors: {self.color}")
        #print(f"available color maps: {self.cm}")
        pass

    def __getitem__(self, item):
        return self.color[item]

    def plot_cycle(self):
        visualize_color_cycle_patches_column()

    def trans(self, color, alpha):
        return trancparent_color_equivalent(color, alpha)

    def create_cm(colors, name="my_color_map"):
        custom_cmap = LinearSegmentedColormap.from_list(name, colors)
        return custom_cmap


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

    colors_dict = {
        "dark_green": '#5ca904',
        "green": '#95c75b',
        "light_green": '#bddc9a',

        "dark_blue": "#1e488f",
        "blue": '#617eb0',
        "light_blue": "#99accc",

        "dark_red": "#9a2b1b",
        "red": "#b6665a",
        "light_red": "#d2a199",

        "dark_yellow": "#f5bf03",
        "yellow": "#f8d24e",
        "light_yellow": "#fadf81",

        "dark_orange": "#e17701",
        "orange": "#ea9f4d",
        "light_orange": "#f1c18c",

        "dark_pink": "#a00498",
        "pink": "#c668c1",
        "light_pink": "#dda7da",

        "dark_grey": "#666666",
        "grey": '#a5a5a5',
        "light_grey": "#cccccc",

        "black": '#000000',
        "white": '#ffffff',
    }


    default_colors = [
        colors_dict["dark_blue"],
        colors_dict["dark_orange"],
        colors_dict["dark_green"],
        colors_dict["dark_red"],
        colors_dict["dark_pink"],
        colors_dict["dark_yellow"],

        colors_dict["blue"],
        colors_dict["orange"],
        colors_dict["green"],
        colors_dict["red"],
        colors_dict["pink"],
        colors_dict["yellow"],

        colors_dict["light_blue"],
        colors_dict["light_orange"],
        colors_dict["light_green"],
        colors_dict["light_red"],
        colors_dict["light_pink"],
        colors_dict["light_yellow"],
    ]

    default_colors_dict = colors_dict



class PhDColors_old(object):
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
        B2Colors.color = copy.deepcopy(PhDColors.colors_dict)
        B2Colors.cm["blue_green_orange"] = B2Colors.create_cm([PhDColors.default_colors_dict["dark_blue"], PhDColors.default_colors_dict["dark_green"], PhDColors.default_colors_dict["dark_orange"]], name="blue_green_orange")
        B2Colors.cm["blue_green_yellow"] = B2Colors.create_cm([PhDColors.default_colors_dict["dark_blue"], PhDColors.default_colors_dict["dark_green"], PhDColors.default_colors_dict["dark_yellow"]], name="blue_green_yellow")
        B2Colors.cm["blue_green"] = B2Colors.create_cm([PhDColors.default_colors_dict["dark_blue"], PhDColors.default_colors_dict["dark_green"]], name="blue_green")
        B2Colors.cm["blue_yellow"] = B2Colors.create_cm([PhDColors.default_colors_dict["dark_blue"], PhDColors.default_colors_dict["dark_yellow"]], name="blue_yellow")
        B2Colors.cm["blue"] = B2Colors.create_cm([PhDColors.default_colors_dict["dark_blue"], PhDColors.default_colors_dict["light_blue"]], name="blue")
        B2Colors.cm["default"] = B2Colors.cm["blue_green_orange"]
        color_names = PhDColors.default_colors_dict
    elif color_set == 'kit':
        color_cycler = cycler("color", KITColors.default_colors)
        B2Colors.color = KITColors.default_colors_dict
        color_names = KITColors.default_colors_dict
    elif color_set == 'reset':
        color_cycler = cycler("color", DefaultColors.default_colors)
        B2Colors.color = DefaultColors.default_colors_dict
        color_names = DefaultColors.default_colors_dict
    #print(f"set color cycler to {color_set}")
    plt.rc('axes', prop_cycle=color_cycler)



def visualize_color_cycle():
    # Get the current color cycle from rcParams
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Create some data
    x = np.linspace(0, 10, 100)

    # Plot lines using each color in the color cycle
    plt.figure(figsize=(10, 6))
    for i, color in enumerate(color_cycle):
        plt.plot(x, np.sin(x + i), color=color, label=f'Color {i+1}: {color}')

    # Add title and legend
    plt.title('Visualization of Current Color Cycle')
    plt.legend(loc='upper right')

    # Show the plot
    plt.show()


def visualize_color_cycle_patches():
    import matplotlib.patches as patches

    # Get the current color cycle from rcParams
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(10, 2))

    # Add color patches to the plot
    for i, color in enumerate(color_cycle):
        # Create a rectangle for each color
        rect = patches.Rectangle((i, 0), 1, 1, facecolor=color)
        ax.add_patch(rect)

        # Add a label below each rectangle
        ax.text(i + 0.5, -0.1, f'Color {i+1}\n{color}', ha='center', va='top', fontsize=10)

    # Set the limits and remove ticks
    ax.set_xlim(0, len(color_cycle))
    ax.set_ylim(-0.2, 1)
    ax.set_xticks([])
    ax.set_yticks([])

    # Add a title
    plt.title('Visualization of Current Color Cycle')


def visualize_color_cycle_patches_column():
    import matplotlib.patches as patches
    # Get the current color cycle from rcParams
    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']

    # Create a figure and axis
    fig, ax = plt.subplots(figsize=(6, len(color_cycle) * 0.6))

    # Add color patches to the plot
    for i, color in enumerate(color_cycle):
        # Create a rectangle for each color
        rect = patches.Rectangle((0, len(color_cycle) - i - 1), 1, 1, facecolor=color)
        ax.add_patch(rect)

        # Add a label next to each rectangle
        ax.text(1.1, len(color_cycle) - i - 0.5, f'Color {i+1}: {color}', ha='left', va='center', fontsize=10)

    # Set the limits and remove ticks
    ax.set_xlim(0, 2)
    ax.set_ylim(0, len(color_cycle))
    ax.set_xticks([])
    ax.set_yticks([])

    # Add a title
    plt.title('Visualization of Current Color Cycle', pad=20)

def trancparent_color_equivalent(color, alpha):
    def _calc(Y):
        if Y[0:2] != "0x":
            Y = "0x" + Y
        #print(alpha, Y)
        return f"{int(255 - alpha*(255-int(Y, 16))):02x}"

    if color[0] == "#":
        color = color[1:]
    trans_color = "#"

    for i in range(3):
        trans_color += _calc(color[i*2: (i+1)*2])
    #print(trans_color)
    return trans_color


## Inkscape color palette

import re

def hex_to_rgb(hex_str):
    """Convert a hex color string to an RGB tuple."""
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

def parse_input(input_str):
    """Parse the input string to extract color sets and their colors."""
    color_sets = {}
    lines = input_str.strip().split('\n')
    current_set = None

    for line in lines:
        if line.startswith('Color Set'):
            current_set = line.strip()
            color_sets[current_set] = []
        elif re.match(r'^#[0-9a-fA-F]{6}$', line):
            color_sets[current_set].append(line.strip())

    return color_sets

def create_gpl_file(palette_name, color_sets, output_filename):
    """Create a .gpl file from the provided color sets."""
    with open(output_filename, 'w') as file:
        file.write("GIMP Palette\n")
        file.write(f"Name: {palette_name}\n")
        file.write("Columns: 4\n")
        file.write("#\n")

        for set_name, colors in color_sets.items():
            file.write(f"# {set_name}\n")
            for color in colors:
                rgb = hex_to_rgb(color)
                file.write(f"{rgb[0]:3} {rgb[1]:3} {rgb[2]:3}   {set_name} - {color}\n")
            file.write("#\n")



