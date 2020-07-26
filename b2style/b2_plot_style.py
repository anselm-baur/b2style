import matplotlib.pyplot as plt
from typing import Union
import os

class B2Figure:
    def __init__(self):
        #self.pointstyle = {'color': 'navy', 'marker': '.', 'ls': ''}
        self.pointstyle = {'marker': '.', 'ls': ''}

    def create_figure(self, figsize=(5, 5), dpi=200, n_x_subfigures=1, n_y_subfigures=1):
        return plt.subplots(n_x_subfigures, n_y_subfigures, figsize=figsize, dpi=dpi)

    def add_descriptions(self, ax: plt.axis,
                                 experiment: Union[str, None] = 'Belle II',
                                 luminosity: Union[str, None] = None,
                                 additional_info: Union[str, None] = None,
                                 ):
        ax.set_title(experiment, loc="left", fontdict={'size': 16, 'style': 'normal', 'weight': 'bold'})
        ax.set_title(luminosity, loc="right")
        ax.annotate(
            additional_info, (0.02, 0.98), xytext=(4, -4), xycoords='axes fraction',
            textcoords='offset points',
            fontweight='bold', ha='left', va='top'
        )

    def save(self, fig, filename,target_dir="plots/",file_formats=[".pdf"]):
        if not os.path.isdir(target_dir):
            os.makedirs(target_dir)

        for file_format in file_formats:
            fig.savefig(os.path.join(target_dir, f'{filename}{file_format}'), bbox_inches="tight")


    def show(self):
        plt.show()