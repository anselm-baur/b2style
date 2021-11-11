class B2Description:
    def __init__(self, ax_labels={"x": "", "y": ""}, additional=""):
        self.ax_labels = ax_labels
        self.additional = additional


    def set_axes_labels(self, ax):
        ax.set_xlabel(self.ax_labels["x"])
        ax.set_ylabel(self.ax_labels["y"])

    def add(self, ax):
        self.set_axes_labels(ax)
        ax.legend()

        ax.annotate(
            self.additional, (0.02, 0.98), xytext=(4, -4), xycoords='axes fraction',
            textcoords='offset points',
            fontweight='bold', ha='left', va='top')