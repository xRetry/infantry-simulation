import numpy as np
from plotting import utils, figures


def time_to_kill(engagement_result:dict):

    # Define path structure to values in engagement result
    x_path = [
        ['player_1', 'solution', 'time_to_kill'],
        ['player_2', 'solution', 'time_to_kill'],
    ]
    y_path = [
        ['player_1', 'solution', 'kill_probability'],
        ['player_2', 'solution', 'kill_probability']
    ]
    y_bar_path = ['solution', 'win_rates']

    # Get values from path
    x_plot = utils.values_from_dict(engagement_result, x_path)
    y_plot = utils.values_from_dict(engagement_result, y_path)
    y_bar = utils.values_from_dict(engagement_result, y_bar_path)
    # Plot figure
    figures.plot(
        x=x_plot,
        y=y_plot,
        x_label='Time to Kill [s]',
        y_label='Probability',
        y_bar=np.array([y_bar[0][1], y_bar[0][2], y_bar[0][0]]),  # reordering
        labels_bar=['Player 1', 'Player 2', 'Draw']
    )


if __name__ == '__main__':
    pass
