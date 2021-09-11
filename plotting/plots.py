import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.legend_handler import HandlerTuple
from plotting import utils
import constants
from scipy.interpolate import griddata


def table(ax, plotType, player1=None, player2=None, sampled_vars=()):
    pl1 = player1
    pl2 = player2
    col_labels = ['Player 1', 'Player 2']
    keys = ['Class', 'Overshield', 'Weapon', 'Ammunition', 'Attachment', 'Suit Slot',
            'Implants', 'Healing Effects', 'Frame Rate', 'Latency']

    units = {'Accuracy': ' %', 'Headshot Ratio': ' %', 'Latency': ' s', 'Range': ' m', 'Fire Rate': '', 'Health': ''}
    sample_vars = {'acc': 'Accuracy', 'hsr': 'Headshot Ratio', 'fire rate': 'Fire Rate', 'health missing': 'Health',
                   'health remaining': 'Health'}
    cells = []
    row_labels = []
    grp_length = []
    is_unique = []
    for j, k in enumerate(keys):
        unit = units.get(k)
        if unit is None: unit = ''
        val1 = pl1.get_desc(k)
        val2 = pl2.get_desc(k)
        inter = np.intersect1d(val1, val2)
        comp1 = val1[np.isin(val1, inter) == False]
        comp2 = val2[np.isin(val2, inter) == False]
        n_added = 0
        # add values that occur in both
        for i in inter:
            if i == '': continue
            n_added += 1
            cells.append([i + unit, i + unit])
            is_unique.append(False)
        max_length = max([len(comp1), len(comp2)])
        # pad shorter array
        c1 = np.repeat([''], max_length - len(comp1))
        c1 = np.concatenate([comp1, c1])
        c2 = np.repeat([''], max_length - len(comp2))
        c2 = np.concatenate([comp2, c2])
        # add values that occur in one
        for i in range(max_length):
            n_added += 1
            cells.append([c1[i] + unit, c2[i] + unit])
            is_unique.append(True)
        # add group key length
        grp_length.append(n_added)
        # add row labels

        for i in range(n_added):
            if i == 0:
                row_labels.append(k)
            else:
                row_labels.append('')

    appendix = ''  # ' - Decrease'
    is_sampled = []
    # add range, acc and hsr
    sampled_vars = np.array(sampled_vars)
    for k in ['Range', 'Accuracy', 'Headshot Ratio']:
        val1 = pl1.get_desc(k)[0] + units[k]
        val2 = pl2.get_desc(k)[0] + units[k]
        if ('acc' in sampled_vars and k == 'Accuracy') or ('hsr' in sampled_vars and k == 'Headshot Ratio'):
            val2 = val2 + appendix
            is_sampled.append(len(cells))
        cells.append([val1, val2])
        grp_length.append(1)
        is_unique.append(val1 != val2)
        row_labels.append(k)
    del_vars = np.array(['acc', 'hsr'])
    sampled_vars = sampled_vars[np.isin(sampled_vars, del_vars) == False]

    # add sample variables
    for var in sampled_vars:
        key = sample_vars[var]
        desc1 = player1.get_desc(key)[0] + units[key]
        desc2 = player2.get_desc(key)[0] + units[key]
        is_sampled.append(len(cells))
        cells.append([desc1, desc2 + appendix])
        grp_length.append(1)
        is_unique.append(True)
        row_labels.append(key)

    # create background coloring
    colMap = []
    colMap2 = []
    c = 0
    for i, grp in enumerate(grp_length):
        for row in range(grp):
            g = 0.15 if (c % 2) == 0 else 0.1
            colMap.append([(g, g, g), (g, g, g)])
            colMap2.append((0, 0, 0))
        if grp > 0: c += 1

    tbl = ax.table(cellText=cells,
                   cellLoc='left',
                   cellColours=colMap,
                   rowLabels=row_labels,
                   rowLoc='right',
                   rowColours=colMap2,
                   colLabels=col_labels,
                   colLoc='left',
                   colColours=[(0, 0, 0), (0, 0, 0)],
                   fontSize=15,
                   loc='center')

    grey = (0.4, 0.4, 0.4)
    for i in range(len(row_labels)):
        tbl[i + 1, -1].set_text_props(fontweight=600)
        tbl[i + 1, 0].set_text_props(color=grey)
        tbl[i + 1, 1].set_text_props(color=grey)

    for i in range(2):
        tbl[0, i].set_text_props(fontweight=600, color=constants.CLS[i])

    for j in range(2):
        for i, uni in enumerate(is_unique):
            if uni:
                tbl[i + 1, j].set_text_props(color=(1, 1, 1))

    for i, s in enumerate(is_sampled):
        tbl[s + 1, 1].set_text_props(color=constants.SAMPLE_COLORS[i])

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(7)
    # ax.set_title('Simulation Parameters')

    ax.axis('off')


def bar(ax, labels:list, y:np.ndarray, y_label:str or None, title=None, horizontal=False, colors=None):
    if colors is None:
        colors = constants.PLAYER_COLORS

    # plot bars
    if horizontal:
        # plot bars
        ax.barh(
            y=labels,
            width=y,
            edgecolor=colors,
            color=(0, 0, 0),
            linewidth=2
        )

        gridAxis = 'x'
        ax.set_yticklabels(labels, rotation=0)
        ax.set_xlabel(y_label)

    else:
        ax.bar(
            x=labels,
            height=y,
            edgecolor=colors,
            color=(0, 0, 0),
            linewidth=2
        )

        gridAxis = 'y'
        ax.set_xticklabels(labels, rotation=0)
        ax.set_ylabel(y_label)

    # set up axis
    ax.grid(True, color=(0.2, 0.2, 0.2), axis=gridAxis)
    ax.set_axisbelow(True)
    ax.set_title(title)


def surface(ax: plt.Subplot, x1, x2, y, y_limits=None, x1_label=None, x2_label=None, y_label=None, title=None, colorbar=False, interpolate=True):
    # define value ranges
    x1_min = min(x1)
    x1_max = max(x1)
    x2_min = min(x2)
    x2_max = max(x2)

    norm = None
    cmap = plt.get_cmap('inferno')
    if y_limits is not None:
        norm = mcolors.TwoSlopeNorm(vmin=y_limits[0], vcenter=sum(y_limits) / 2, vmax=y_limits[1])
        cmap = utils.custom_cmap()

    if interpolate:
        grid_x, grid_y = np.meshgrid(np.linspace(x1_min, x1_max, 100), np.linspace(x2_min, x2_max, 100))
        xy = np.array([x1, x2]).T
        interpol = griddata(xy, y, (grid_y, grid_x), method='cubic')

        # plot maps
        img = ax.imshow(
            interpol.T,
            cmap=cmap,
            norm=norm,
            extent=[x1_min, x1_max, x2_min, x2_max],
            origin='lower'
        )
        #x, y = np.meshgrid(
        #    x,
        #    y)
        #con = ax.contour(
        #    x, y,
        #    z,
        #    cmap='seismic',
        #    norm=norm,
        #    linestyles='-',
        #    levels=np.linspace(-1, 1, 21),
        #    alpha=0.5,
        #)

         # add colorbar
        if colorbar:
            cbar = plt.colorbar(img, ax=ax, ticks=np.linspace(-1, 1, 9))
            #cbar.add_lines(con)
            #cbar.ax.set_yticklabels(['100', '75', '50', '25', '0', '25', '50', '75', '100'])
            cbar.ax.set_ylabel(y_label, rotation=-270)

    plt.scatter(x1, x2, c=y, cmap=cmap, norm=norm)

    # configure axis
    ax.set_xlabel(x1_label)
    ax.set_ylabel(x2_label)
    ax.set_title(title)
    ax.grid(True, color=(0.2, 0.2, 0.2))


def plot(ax:plt.Subplot, x:np.ndarray, y:np.ndarray, c=None, x_label:str=None, y_label:str=None, norm_limits=None):
    if len(x.shape) == 1:
        x = x[:, None].T
    if len(y.shape) == 1:
        y = y[:, None].T

    cmap, norm = None, None

    if c is None:
        c = constants.PLAYER_COLORS
    if norm_limits is not None:
        cmap = plt.get_cmap('bwr')
        norm = mcolors.TwoSlopeNorm(vmin=norm_limits[0], vcenter=0, vmax=norm_limits[1])

    for i in range(len(y)):
        ax.plot(x[i], y[i], c='w', alpha=0.3)
        ax.scatter(x[i], y[i], c=c[i], cmap=cmap, zorder=3, norm=norm)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.grid(True, color=(0.1, 0.1, 0.1))


if __name__ == '__main__':
    pass
