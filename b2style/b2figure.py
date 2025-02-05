from enum import auto
import matplotlib as mpl
import matplotlib.pyplot as plt
from typing import Union
import numpy as np
from uncertainties import unumpy as unp
from scipy.stats import binned_statistic
import os
from b2style.b2plotstyle import *
import b2style.b2colors
from b2style.b2colors import B2Colors
from b2style.b2description import B2Description
from collections import OrderedDict
from pathlib import Path
import datetime
import types
import logging

import matplotlib

_log = logging.getLogger(name=__name__)

class B2Figure:
    def __init__(self, bold_labels=True, dpi=90, output_dir='plots/', plot_state=None, experiment=None,
                 luminosity=None, auto_description=True, description=None, color_theme='phd'):
        #self.pointstyle = {'color': 'navy', 'marker': '.', 'ls': ''}
        self.pointstyle = {'marker': '.', 'ls': ''}
        self.plot_state = plot_state
        self.experiment = experiment
        self.luminosity = luminosity
        self.simulation = None
        self.preliminary = None

        self.fig_labels = []

        #matplotlib.rc('text', usetex=True)
        matplotlib.rc('text.latex', preamble=r"\usepackage{amsmath}")
        set_default_plot_params(bold_labels=bold_labels)
        b2style.b2colors.set_default_colors(color_theme)
        self.colors = B2Colors()
        self.dpi = dpi

        if description is None:
            self.description_args = {}
        else:
            for key, value in description.items():
                if key in self.__dict__:
                    self.__dict__[key] = value
                else:
                    _log.warning(f"description atribute {key} not found... skip")
            self.description_args = description
        self.auto_description = auto_description
        self.save_fig = False
        self.output_dir = output_dir

        self.xlabel_pos = OrderedDict([('x', 1), ('ha', 'right')])
        self.ylabel_pos = OrderedDict([('y', 1), ('ha', 'right')])

        self.errorbar_args = {"fmt": 'o',
                                      "elinewidth": 0.5,
                                      "markersize": 1.4}


    def color(self,color):
        #print("get color", color)
        return self.colors.color[color]

    def create(self, **kwargs):
        return self.create_figure(**kwargs)

    def create_figure(self, figsize=None, dpi=90, n_x_subfigures=None, n_y_subfigures=None, left=70, top=40, right=15, bottom=40, **kwargs):
        if n_x_subfigures:
            kwargs["ncols"] = n_x_subfigures
        if n_y_subfigures:
            kwargs["nrows"] = n_y_subfigures
        if "nrows" not in kwargs: kwargs["nrows"] = 1
        if "ncols" not in kwargs: kwargs["ncols"] = 1
        if not figsize:
             figsize = (6*kwargs["ncols"], 5*kwargs["nrows"])

        # first trim the figure, otherwise the description is displaced
        self.fig, self.ax = plt.subplots(figsize=figsize, dpi=dpi, **kwargs)
        self.trim(fig=self.fig, left=left, right=right, top=top, bottom=bottom)

        if self.auto_description:
            if "plot_state" not in self.description_args:
                self.description_args.update({"plot_state": self.plot_state})
            if "luminosity" not in self.description_args:
                self.description_args.update({"luminosity": self.luminosity})
            if type(self.ax) == type(plt.gca()):
                # we have just a single subplot
                        self.add_descriptions(self.ax, **self.description_args)
                        self.shift_offset_text_position(self.ax)
            elif kwargs["ncols"] > 1 and kwargs["nrows"] == 1:
                for i in range(kwargs["ncols"]):
                    self.add_descriptions(self.ax[i], **self.description_args)
                    self.shift_offset_text_position(self.ax[i])

            elif kwargs["ncols"] == 1 and kwargs["nrows"] > 1:
                for j in range(kwargs["nrows"]):
                    self.add_descriptions(self.ax[j], **self.description_args)
                    self.shift_offset_text_position(self.ax[j])
            else:
                print(self.ax.shape)
                for i in range(kwargs["ncols"]):
                    for j in range(kwargs["nrows"]):
                        self.add_descriptions(self.ax[j][i], **self.description_args)
                        self.shift_offset_text_position(self.ax[j][i])

        #print(self.fig.transFigure.transform(self.fig_labels[0].get_position()))

        return self.fig, self.ax

    def create_pull_plot(self, data=[[]], mc=[[]], ncols=1, **kwargs):
        gridspec_kw={'height_ratios': [2, 1]}
        kwargs["ncols"] = ncols
        kwargs["nrows"] = 2
        kwargs["gridspec_kw"] = gridspec_kw
        if not "dpi" in kwargs:
            kwargs["dpi"] = self.dpi
        fig, ax = plt.subplots(**kwargs)

        if self.auto_description:
            if kwargs["ncols"] == 1:
                self.add_descriptions(ax[0], **self.description_args)
            else:
                pass
        return fig, ax

    def plot_errorbar(self, ax, x, data, mc, data_yerr=None, mc_yerr=None, poisson_err=True, **kwargs):
        for arg in self.errorbar_args:
            if not arg in kwargs:
                kwargs[arg] = self.errorbar_args[arg]

        if poisson_err:
            if data_yerr or mc_yerr:
                raise ValueError("data_yerr or mc_yerr given together with poission_err!")
            data_yerr = np.sqrt(data)
            mc_yerr = np.sqrt(mc)
        ax.errorbar(x, data, yerr=data_yerr, **kwargs)
        ax.errorbar(x, mc, yerr=mc_yerr, **kwargs)

    def plot_pull(ax, x, data, mc, ):
        pass


    def tight_pull_spacing(self):
        self.subplots_adjust(hspace=0.05)

    def subplots_adjust(self,**kwargs):
        plt.subplots_adjust(**kwargs)

    def add_head_room(self, ax, data_list, head_room_frac=1.1, y_lower_lim=0):
        max_list = []
        for data in data_list:
            max_list.append(np.max(data))
        max_bin_entries = np.max(max_list)
        ax.set_ylim((y_lower_lim, max_bin_entries*head_room_frac))

    def add_descriptions(self, ax: plt.axis,
                                 experiment: Union[str, None] = 'Belle II',
                                 luminosity: Union[str, int, float, None] = None,
                                 additional_info: Union[str, None] = None,
                                 small_title: Union[bool, None] = False,
                                 preliminary: Union[bool, None] = False,
                                 simulation: Union[bool, None] = False,
                                 plot_state: Union[str, None] = None,
                                 title_indent: Union[int, None] = 0,
                                 exp_nr: Union[int, None] = None,
                                 proc_nr: Union[int, None] = None,
                                 buck_nr: Union[int, None] = None,
                                 description: Union[B2Description, None] = None,
                                 y_offset: Union[int] = 17,
                                 extra_luminosity: Union[str, int, float, None] = None
                                 ):

        # generate luminosity text
        if luminosity is None:
            luminosity = ""
        if isinstance(luminosity, int) or isinstance(luminosity, float):
           luminosity = r"$\int \mathcal{L} \,\mathrm{d}t=" + "{:.0f}".format(np.round(luminosity,0))  +"\,\mathrm{fb}^{-1}$"

        # add some additional dataset meta data
        if exp_nr:
            luminosity += f"\nExp. {exp_nr}"
            if proc_nr:
                 luminosity += f", Proc {proc_nr}"
            if buck_nr:
                 luminosity += f", Buck. {buck_nr}"

        #print("plot_state", plot_state)
        if not plot_state:
            plot_state = ""
            if simulation:
                plot_state = "(Simulation)"
            elif preliminary:
                plot_state = "(Preliminary)"
        #print(f"plot_state: {plot_state}")
        #print(f"luminosity: {luminosity}")

        if small_title or plot_state or preliminary or simulation:
            if plot_state or preliminary or simulation:
                y=1
                y_offset_points = y_offset  # Absolute distance from the subplot in points
                y_plot_state_distance = -14
            else:
                y = 1
                y_offset_points = 0  # Absolute distance from the subplot in points

            # Get the bounding box of the axes in figure coordinates
            renderer = self.fig.canvas.get_renderer()
            bbox = ax.get_window_extent(renderer)

            # Convert the y_offset from points to pixels
            y_offset_pixels = y_offset_points

            # Calculate the y position for the title in pixels
            absolute_y_pixels = bbox.ymax + y_offset_pixels
            absolute_y_plot_state_pixels = absolute_y_pixels + y_plot_state_distance

            # Convert the y position from pixels to figure coordinates
            absolute_y_fig = absolute_y_pixels / self.fig.bbox.height
            absolute_y_plot_state_fig = absolute_y_plot_state_pixels / self.fig.bbox.height

            # Set the title with the calculated y position
            self.fig_labels.append(self.fig.text(bbox.x0 / self.fig.bbox.width, absolute_y_fig,
                    ' ' * title_indent + experiment, ha='left', va='bottom',
                    fontdict={'style': 'normal', 'weight': 'bold', 'size': 16}))

            # Add the plot_state text (e.g., Preliminary or Simulation tag)
            self.fig_labels.append(self.fig.text(bbox.x0 / self.fig.bbox.width, absolute_y_plot_state_fig, '{}'.format(' ' * title_indent) +
                    plot_state, ha='left', va='bottom',
                    fontdict={'style': 'normal', 'weight': 'normal', 'size': 11}))

            if extra_luminosity is not None:
                # Add extra text in lumi style at the same y level es the plot _state with loc right
                self.fig_labels.append(self.fig.text(bbox.xmax / self.fig.bbox.width, absolute_y_plot_state_fig,
                    f"{extra_luminosity}", ha='right', va='bottom',
                    fontdict={'style': 'normal', 'weight': 'normal', 'size': 11}))


            ax.set_title(luminosity, loc="right")
        else:
            ax.set_title('{}'.format(' '*title_indent)+experiment, loc="left", fontdict={'size': 16, 'style': 'normal', 'weight': 'bold'})
            ax.set_title(plot_state + luminosity, loc="right")

        self.add_additional_info(ax=ax, additional_info=additional_info)

        if description:
            description.add(ax)


    def add_additional_info(self, ax, additional_info="", fontweight='bold', ha='left', va='top', x=0.02, y=0.98):
        """Aadd additional info in info in the plotting area."""
        ax.annotate(
            additional_info, (x, y), xytext=(4, -4), xycoords='axes fraction',
            textcoords='offset points',
            fontweight=fontweight, ha=ha, va=va)


    def get_bincenters_of_binedges(self, bin_edges):
        return np.mean(np.vstack([bin_edges[0:-1],bin_edges[1:]]), axis=0)

    def get_range(self,data):
        return (np.nanmin(data),np.nanmax(data))

    def add_bin_width(self, bin_edges, units=''):
        return r"/$" + str(np.round((bin_edges[1]-bin_edges[0]),3)) + r"\;$" + units


    def calculate_stacked_err_df(self,stacked_data,bin_edges,variable):
        # stacked_data conteins a list of data frames, the column variable is stacked, here we want to calc the unvertainty for this
        stacked_err = np.sum(np.array([binned_statistic(data_i[variable].to_numpy(),
                                          data_i['__weight__'].to_numpy()**2,
                                          statistic="sum",
                                          bins=bin_edges)[0] for data_i in stacked_data]),
               axis=0)
        return np.sqrt(stacked_err)

    def calculate_stacked_err_list(self,stacked_data,weights,bin_edges):
        # stacked_data conteins a list of data frames, the column variable is stacked, here we want to calc the uncertainty for this
        stacked_err = np.sum(np.array([binned_statistic(data_i,
                                          weight_i**2,
                                          statistic="sum",
                                          bins=bin_edges)[0] for data_i,weight_i in zip(stacked_data,weights)]),
               axis=0)
        return np.sqrt(stacked_err)

    def point_plot_hist(self, ax, data, label='', bins=100, range='', color='black',weight=1,density=False):
        color = B2Colors.color[color]
        if not range:
            range = (data.min(), data.max())
        hist, bin_edges = np.histogram(data,bins=bins, range=range, density=density)
        bin_centers = self.get_bincenters_of_binedges(bin_edges)
        y_err = np.sqrt(hist)
        x_err = (bin_centers[1]-bin_centers[0])/2
        ax.errorbar(bin_centers, hist*weight, yerr=y_err*weight, xerr=x_err, label=label, elinewidth=0.5, fmt='o', color=color, markersize='1.4')

    def pull_plot(self, ax, data1, data2, bins=None, range=None, bin_edges=[], variable='', color='black', weight=1, is_df=False, stacked=False, density=False, is_hist=False):
        color = B2Colors.color[color]

        if stacked:
            # data1: df with colum variable containing data
            # data2: a list of df each with column variable
            if not range:
                range = self.get_range(data1[variable].to_numpy())

            # data
            hist1, bin_edges = np.histogram(data1[variable].to_numpy(),bins=bins, range=range, density=density)
            # MC
            hist2 = np.sum(np.array([binned_statistic(data2_i[variable].to_numpy(), data2_i['__weight__'].to_numpy(), statistic="sum", bins=bin_edges)[0] for data2_i in data2]), axis=0)
            err_hist2 = np.sum(np.array([binned_statistic(data2_i[variable].to_numpy(), data2_i['__weight__'].to_numpy()**2, statistic="sum", bins=bin_edges)[0] for data2_i in data2]), axis=0)
            uhist1 = unp.uarray(hist1,np.sqrt(hist1))
            uhist2 = unp.uarray(hist2,np.sqrt(err_hist2))

                # find entries which are problematic because of zero devision
            avoid_zero_div = (hist1 > 0) #& (np.abs(hist1 - hist2) > 0)
            uhist1=uhist1[avoid_zero_div]
            uhist2=uhist2[avoid_zero_div]

            bin_centers = self.get_bincenters_of_binedges(bin_edges)[avoid_zero_div]
            pull = (uhist1-uhist2)/uhist1
            ax.axhline(y=0, color='grey', alpha=0.8)
            ax.errorbar(bin_centers, unp.nominal_values(pull), yerr=unp.std_devs(pull),
                            **self.errorbar_args)

        else:
            if is_df:
                pass
            else:
                if is_hist:
                    hist1 = data1
                    hist2 = data2
                else:
                    if not range:
                        range = self.get_range(data1)
                    hist1, bin_edges = np.histogram(data1,bins=bins, range=range)
                    hist2, bin_edges = np.histogram(data2,bins=bins, range=range,weights=weight if isinstance(weight, list) else np.full(data2.size,weight))


                uhist1 = unp.uarray(hist1,np.sqrt(hist1))
                uhist2 = unp.uarray(hist2,np.sqrt(hist2))

                # find entries which are problematic because of zero devision
                avoid_zero_div = (hist1 > 0) #& (np.abs(hist1 - hist2) > 0)
                uhist1=uhist1[avoid_zero_div]
                uhist2=uhist2[avoid_zero_div]

                bin_centers = self.get_bincenters_of_binedges(bin_edges)[avoid_zero_div]
                pull = (uhist1-uhist2)/uhist1
                ax.axhline(y=0, color='grey', alpha=0.8)
                ax.errorbar(bin_centers, unp.nominal_values(pull), yerr=unp.std_devs(pull),
                                fmt='o', color=color, markersize='1.4', elinewidth=0.5)


        ax.set_ylim((-1,1))
        self.tight_pull_spacing()

    def shift_offset_text_position_old(self, ax):
        def upper_left_offset(self, bboxes, bboxes2):
            upper = self.axes.bbox.ymax
            self.offsetText.set(va="bottom", ha="right")
            self.offsetText.set_position(
                    (-0.01, 0.5 ))#upper-0.3))
        ax._update_offset_text_position = types.MethodType(upper_left_offset, ax.yaxis)
        ax._update_offset_text_position(0,0)

    def shift_offset_text_position_pull_old(self, ax):
        def upper_left_offset(self, bboxes, bboxes2):
            top = self.axes.bbox.ymax
            right = self.axes.bbox.xmax
            self.offsetText.set(va="bottom", ha="right")
            self.offsetText.set_position(
                    (0.15, top*0.9 ))#upper-0.3))
        ax.yaxis._update_offset_text_position = types.MethodType(upper_left_offset, ax.yaxis)
        ax.yaxis._update_offset_text_position(0.1,-0.1)

    def shift_offset_text_position(self, ax):
        #self.fig.tight_layout()
        offset = ax.yaxis.get_offset_text().get_text()
        print(offset)
        if len(offset) > 0:
            ax.yaxis.offsetText.set_visible(False)
            #ax.text(-0.2, 0.9, offset, transform=ax.transAxes,
            #   horizontalalignment="left",
            #   verticalalignment="bottom")


    def trim(self, fig, left=50, top=50, right=10, bottom=50):
        # Convert pixel values to relative figure units
        left_margin_px = left  # pixels
        right_margin_px = right  # pixels
        top_margin_px = top  # pixels
        bottom_margin_px = bottom  # pixels

        # Convert pixels to relative figure units
        left_margin = left_margin_px / fig.get_figwidth() / fig.dpi
        right_margin = right_margin_px / fig.get_figwidth() / fig.dpi
        top_margin = top_margin_px / fig.get_figheight() / fig.dpi
        bottom_margin = bottom_margin_px / fig.get_figheight() / fig.dpi

        # Adjust the subplots
        fig.subplots_adjust(left=left_margin, right=1-right_margin,
                            top=1-top_margin, bottom=bottom_margin)


    def add_date(self, s=""):
        now = datetime.datetime.now()
        if s:
            s = f"{s}_"
        return f"{s}{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}"


    def save(self, fig, filename, target_dir=None, file_formats=[".pdf"], add_date=False, **kwargs):
        if not target_dir:
            target_dir = self.output_dir

        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        if add_date:
            filename = self.add_date(filename)

        for file_format in file_formats:
            #fig.savefig(os.path.join(target_dir, f'{filename}{file_format}'), bbox_inches="tight")
            path = Path(target_dir)/Path(filename+file_format)
            print(str(path))
            fig.savefig(path, bbox_inches="tight", **kwargs)


    def show(self):
        plt.show()

def hist(df, var, hist_args={"bins": 50}):
    b2fig = B2Figure()
    fig, ax = b2fig.create_figure()
    b2fig.add_descriptions(ax)
    ax.hist(df[var], **hist_args)
