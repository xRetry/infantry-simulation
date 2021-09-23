import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib.colors as mcolors
from matplotlib.lines import Line2D

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


def recoil_samples(x: np.ndarray, y: np.ndarray, distances, tar_offset, acc, weapon_name, compensate):

    tar_color = 'lime'
    tar_size = [0.0950435176, 0.0950435176]
    tar_x, tar_y = utils.ellipse(tar_size[0], tar_size[1])
    cmap = plt.get_cmap("plasma")
    comp_state = 'perfect compensation' if compensate else 'no compensation'
    title = '{} Recoil Pattern ({})'.format(weapon_name, comp_state)
    target_name = '{} Hitbox'.format('Head')
    sub_titles = ['Side View', 'Top View']
    xy = [x, y]

    # FIGURE

    plt.style.use('dark_background')
    fig = plt.figure(tight_layout=True, figsize=(11, 7))
    fig.suptitle(title)
    gs = gridspec.GridSpec(3, len(distances))
    ax0 = None
    for i in range(len(distances)):
        if i == 0:
            ax0 = fig.add_subplot(gs[0, i])
            ax = ax0
        else:
            ax = fig.add_subplot(gs[0, i], sharey=ax0)

        plots.recoil_pattern(
            ax=ax,
            x=x * distances[i],
            y=y * distances[i],
            target_x=tar_x + tar_offset[i, 0],
            target_y=tar_y + tar_offset[i, 1],
            target_color=tar_color,
            title='{} m'.format(round(distances[i])),
            cmap=cmap
        )

    circle_marker = Line2D(range(1), range(1), color="k", marker='o', markerfacecolor="k", markeredgecolor=tar_color)
    ax0.legend([circle_marker], [target_name], loc='upper center', bbox_to_anchor=(0.5, -0.05))

    ax = None
    for i in range(2):
        sign = -1 if i == 1 else 1
        ax = fig.add_subplot(gs[i+1, :])
        ax.set_title(sub_titles[1-i])
        plots.recoil_cone(
            ax=ax,
            vals=sign * xy[1-i],
            distances=distances,
            target_y=sign * tar_offset[:, 1-i],
            target_size=tar_size[1-i],
            target_color=tar_color,
            bar_color=cmap,
        )
    ax.set_xlabel('Range [m]')

    plt.show()


def recoil(x, y, x_comp, y_comp, x_centers, y_centers, tar_size, weapon_name=None):
    title = '{} - Recoil Pattern'.format(weapon_name)
    cmap = plt.get_cmap("plasma")
    tar_dis = np.array([5, 10, 20])

    tar_x, tar_y = utils.ellipse(tar_size[0], tar_size[1])

    plt.style.use('dark_background')
    fig = plt.figure(figsize=(13, 10), tight_layout=True)
    fig.suptitle(title)
    gs = gridspec.GridSpec(4, 6)

    ax0 = fig.add_subplot(gs[1, 0])
    plots.recoil_pattern(
        ax0,
        x,
        y,
        n=-1,
        target_x=tar_x,
        target_y=tar_y,
        target_distance=tar_dis
    )
    plots.recoil_centers(ax0, x_centers, y_centers)

    ax1 = fig.add_subplot(gs[3, 0])
    plots.recoil_pattern(ax1, x_comp, y_comp, n=-1, target_x=tar_x, target_y=tar_y, target_distance=tar_dis)

    ax = fig.add_subplot(gs[0, 0], sharey=ax0, sharex=ax0)
    plots.recoil_pattern(ax, x, y, cmap=cmap)
    ax.set_title('No Compensation:')

    ax = fig.add_subplot(gs[2, 0], sharey=ax1, sharex=ax1)
    plots.recoil_pattern(ax, x_comp, y_comp, cmap=cmap)
    ax.set_title('Perfect Compensation:')

    for i in range(2):
        for j in range(5):
            ax = fig.add_subplot(gs[i, j+1], sharey=ax0, sharex=ax0)
            plots.recoil_pattern(ax, x, y, n=i*5+j)

    for i in range(2):
        for j in range(5):
            ax = fig.add_subplot(gs[i+2, j+1], sharey=ax1, sharex=ax1)
            plots.recoil_pattern(ax, x_comp, y_comp, n=i*5+j)

    plt.show()


if __name__ == '__main__':
    pass
