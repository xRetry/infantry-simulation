import numpy as np
from matplotlib.colors import LinearSegmentedColormap


def custom_cmap():
    cdict = {'red': [[0.0, 0.2, 0.2],
                     [0.5, 0, 0],
                     [0.6, 0.1, 0.1],
                     [1.0, 0.75, 0.75]],
             'green': [[0.0, 0.2, 0.2],
                       [0.5, 0, 0],
                       [1.0, 0.2, 0.2]],
             'blue': [[0.0, 0.75, 0.75],
                      [0.4, 0.1, 0.1],
                      [0.5, 0, 0],
                      [1.0, 0.2, 0.2]]}
    return LinearSegmentedColormap('testCmap', segmentdata=cdict, N=256)


def values_from_dict(dct:dict, paths:list):
    """
    Returns values form a nested dict according to provided key paths.

    :param dct: Nested dictionary
    :param paths: List of dictionary keys
    :return: Numpy array of dictionary values
    """
    # Check if list of paths is given
    is_single_path = not isinstance(paths[0], list)
    # Wrap path if not
    if is_single_path:
        paths = [paths]
    value_list = []
    # Iterate trough paths
    for path in paths:
        temp = dct
        # Iterate through keys in path
        for key in path:
            temp = temp[key]
        value_list.append(temp)
    # Unwrap result if only one path was given
    if is_single_path:
        value_list = value_list[0]
    return np.array(value_list)


def calc_difference(x:np.ndarray, y1:np.ndarray, y2:np.ndarray) -> (np.ndarray, np.ndarray):
    """
    [UNFINISHED] Calculates x and y values for win margin difference.

    :param x:
    :param y1:
    :param y2:
    :return:
    """
    x = np.ndarray(x)
    diff = y1 - y2
    diff[np.abs(diff) < 1e-3] = 0.
    sign_change = np.where(np.sign(diff[:-1]) != np.sign(diff[1:]))[0] + 1
    added = 0
    for i in range(len(sign_change)):
        if -1e-3 < diff[sign_change[i] - 1] < 1e-3:
            sign_change[i] -= 1
            continue
        if -1e-3 < diff[sign_change[i]] < 1e-3:
            continue
        sign_change[i] += added
        diff = np.insert(diff, sign_change[i], 0)
        x = np.insert(x, sign_change[i], (x[sign_change[i]] + x[sign_change[i] - 1]) / 2)
        added += 1
    idxs1 = diff > 1e-3
    idxs2 = diff < -1e-3
    idxs0 = np.abs(diff) < 1e-3
    idxs1[sign_change] = True
    idxs2[sign_change] = True
    idxs0[sign_change] = False

    w1 = x[idxs1], abs(diff[idxs1])
    w2 = x[idxs2], abs(diff[idxs2])
    draw = x[idxs0], abs(diff[idxs0])


def calc_average(x_keep: (np.ndarray, list, tuple), y: (np.ndarray, list, tuple)) -> (np.ndarray, np.ndarray):
    """
    Returns average for (multivariate) x-y value pairs based on x values to keep.

    :param x_keep: List (or list of lists) of x values group by
    :param y: List of y values
    :return: New x and y values
    """
    # Check if x values are list of lists -> wrap if not
    if not isinstance(x_keep[0], (np.ndarray, list, tuple)):
        x_keep = [x_keep]
    # Group y by x values. Aggregate multiple y values in lists
    d = {}
    for i, k in enumerate(np.dstack(x_keep)[0]):
        k = tuple(k)
        val_old = d.get(k)
        if val_old is None:
            d[k] = [y[i]]
        else:
            d[k].append(y[i])
    # Compute mean value for every aggregate list.
    x, y = [], []
    for k, v in d.items():
        x.append(k)
        y.append(np.mean(v))
    return np.array(x).T, np.array(y)


def ellipse(x_size:float, y_size:float, n_pts:int=100, rot_degrees:float=0) -> (np.ndarray, np.ndarray):
    """
    Returns equally spaced points from given ellipse, centered at 0,0.

    :param x_size: Half of the horizontal width of the ellipse.
    :param y_size: Half of the vertical height of the ellipse.
    :param n_pts: Amount of point to be returned.
    :param rot_degrees: Rotation of the ellipse in degrees.
    :return: x, y coordinates of ellipse points as numpy array.
    """
    t = np.linspace(0, 2 * np.pi, n_pts)
    rot_radians = np.deg2rad(rot_degrees)

    x_tar = x_size * np.cos(rot_radians) * np.cos(t) - y_size * np.sin(rot_radians) * np.sin(t)
    y_tar = x_size * np.sin(rot_radians) * np.cos(t) + y_size * np.cos(rot_radians) * np.sin(t)
    return x_tar, y_tar


if __name__ == '__main__':
    pass
