import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from plotting import plots, utils


def plot(x:np.ndarray, y:np.ndarray, x_label:str=None, y_label:str=None, y_bar:np.ndarray=None, labels_bar=None, y_label_bar:str=None):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 5.3))
    gs = fig.add_gridspec(2, 2, width_ratios=[3, 1])
    # x-y plot
    plots.plot(fig.add_subplot(gs[0, 0]), x=x, y=y, x_label=x_label, y_label=y_label)
    # Add bar plot if values are provided
    if y_bar is not None:
        plots.bar(
            ax=fig.add_subplot(gs[:, 1]),
            labels=labels_bar,
            y=y_bar,
            y_label=y_label_bar,
            horizontal=False,
        )

    plt.tight_layout()
    plt.show()


def surface(x:np.ndarray, y:np.ndarray, z:np.ndarray, x_label:str=None, y_label:str=None, z_label:str=None):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(10, 5.2))
    gs = fig.add_gridspec(ncols=2, nrows=2, figure=fig, width_ratios=[2, 1], left=0.00)

    plots.surface(ax=fig.add_subplot(gs[:, 0]), x1=x, x2=y, y=z, x1_label=x_label, x2_label=y_label, title=z_label,
                  interpolate=True)


    plots.bar(
        ax=fig.add_subplot(gs[0, 1]),
    )

    plots.table(
        ax=fig.add_subplot(gs[1, 1]),
    )

    fig.suptitle("Engagement Simulation", fontsize=16)

    plt.show()


def volume(x1:np.ndarray, x2:np.ndarray, x3:np.ndarray, y:np.ndarray, x1_label:str=None, x2_label:str=None, x3_label:str=None, y_label:str=None, title:str=None):
    plt.style.use('dark_background')
    fig = plt.figure(figsize=(11, 4))
    gs = fig.add_gridspec(ncols=2, nrows=1, figure=fig, width_ratios=[4, 2])
    fig.suptitle(title, fontsize=16)

    x3_plot, y_plot = utils.calc_average(x3, y)
    plots.plot(
        ax=fig.add_subplot(gs[0, 0]),
        x=x3_plot[0],
        y=y_plot,
        x_label=x3_label,
        y_label=None
    )

    x_surf, y_surf = utils.calc_average([x1, x2], y)
    plots.surface(
        ax=fig.add_subplot(gs[0, 1]),
        x1=x_surf[0],
        x2=x_surf[1],
        y=y_surf,
        x1_label=x1_label,
        x2_label=x2_label,
        y_label=y_label,
        title=None,
        interpolate=False,
        colorbar=True
    )

    fig.tight_layout()
    plt.show()


if __name__ == '__main__':
    acc = np.array([0, 0, 2, 2, 3, 4])
    hsr = np.array([2, 2, 3, 4, 4, 5])
    r = np.array([10, 10, 10, 20, 20, 30])
    y = np.random.randn(6)
    #plots.utils.calc_average(x_keep=(acc, hsr), x_avg=(r,), y=y)
    volume(acc, hsr, r, y)
    pass
