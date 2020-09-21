import matplotlib.pyplot as plt
from typing import Union
import numpy as np
from uncertainties import unumpy as unp
from scipy.stats import binned_statistic
import os
import b2style.b2plotstyle
import b2style.b2colors
from b2style.b2colors import B2Colors

class B2Figure:
    def __init__(self):
        #self.pointstyle = {'color': 'navy', 'marker': '.', 'ls': ''}
        self.pointstyle = {'marker': '.', 'ls': ''}
        b2style.b2plotstyle.set_default_plot_params()
        b2style.b2colors.set_default_colors('reset')
        self.colors = B2Colors()

    def color(self,color):
        return self.colors.color[color]

    def create_figure(self, figsize=(5, 5), dpi=200, n_x_subfigures=1, n_y_subfigures=1, **kwargs):
        return plt.subplots(ncols=n_x_subfigures, nrows=n_y_subfigures, figsize=figsize, dpi=dpi, **kwargs)

    def add_descriptions(self, ax: plt.axis,
                                 experiment: Union[str, None] = 'Belle II',
                                 luminosity: Union[str, None] = '',
                                 additional_info: Union[str, None] = None,
                                 small_title: Union[bool, None] = False,
                                 preliminary: Union[bool, None] = True,
                                 title_indent: Union[int, None] = 0
                                 ):

       
        
        if small_title:
            ax.set_title('{}'.format(' '*title_indent)+experiment+'\n{}'.format(' '*title_indent)+'{}'.format('(Preliminary)' if preliminary else ''), loc="left", fontdict={'style': 'normal', 'weight': 'bold'})                
            ax.set_title(luminosity, loc="right")
        else:
            ax.set_title('{}'.format(' '*title_indent)+experiment, loc="left", fontdict={'size': 16, 'style': 'normal', 'weight': 'bold'})                
            ax.set_title('{}'.format('(Preliminary) ' if preliminary else '' ) + luminosity, loc="right")
            
        ax.annotate(
            additional_info, (0.02, 0.98), xytext=(4, -4), xycoords='axes fraction',
            textcoords='offset points',
            fontweight='bold', ha='left', va='top'
        )

    def get_bincenters_of_binedges(self, bin_edges):
        return np.mean(np.vstack([bin_edges[0:-1],bin_edges[1:]]), axis=0)

    def get_range(self,data):
        return (np.nanmin(data),np.nanmax(data))

    def point_plot_hist(self, ax, data, label='', bins=100, range='', color='black',weight=1,density=False):
        color = B2Colors.color[color]
        if not range:
            range = (data.min(), data.max())
        hist, bin_edges = np.histogram(data,bins=bins, range=range, density=density)
        bin_centers = self.get_bincenters_of_binedges(bin_edges)
        y_err = np.sqrt(hist)
        x_err = (bin_centers[1]-bin_centers[0])/2
        ax.errorbar(bin_centers, hist*weight, yerr=y_err*weight, xerr=x_err, label=label, elinewidth=0.5, fmt='o', color=color, markersize='1.4')

    def pull_plot(self, ax, data1, data2, bins, range=None, variable='', color='black', weight=1, is_df=False, stacked=False, density=False):
        color = B2Colors.color[color]
                    
        if stacked:
            if not range:
                range = self.get_range(data1[variable].to_numpy())
            hist1, bin_edges = np.histogram(data1[variable].to_numpy(),bins=bins, range=range, density=density)
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
                            fmt='o', color=color, markersize='1.4', elinewidth=0.5)
            

        else:
            if is_df:
                pass
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
        


    def save(self, fig, filename,target_dir="plots/",file_formats=[".pdf"]):
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        for file_format in file_formats:
            #fig.savefig(os.path.join(target_dir, f'{filename}{file_format}'), bbox_inches="tight")
            #print(f'{filename}{file_format}')
            fig.savefig(f'{target_dir}{filename}{file_format}', bbox_inches="tight")


    def show(self):
        plt.show()

def hist(df,var):
    b2fig = B2Figure()
    fig, ax = b2fig.create_figure()
    b2fig.add_descriptions(ax)
    ax.hist(df[var],bins=50)
