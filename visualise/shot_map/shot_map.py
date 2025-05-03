import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import Normalize

from .shot_map_helpers import (
    calculate_metrics,
    setup_pitch,
    plot_events,
    add_metrics_boxes,
    add_metric_labels,
    plot_top_players
)

def create(team_shot_events, team_info, team_colors, visualisation_params, match_info):
    bg = visualisation_params["bg"]
    bodyfont = visualisation_params["bodyfont"]
    text_color = visualisation_params["text_color"]
    line_color = visualisation_params["pitch_line_color"]
    # folder_path = visualisation_params["folder_path"]

    home_team = team_info["home_team"]
    away_team = team_info["away_team"]
    home_prefix = team_info["home_prefix"]
    away_prefix = team_info["away_prefix"]
    save_string = team_info["save_string"]

    # # If format_match_details is your own function, make sure it's imported correctly
    # match_date, match_score, match_comp, match_season = match_info

    labels, values, start_x, spacing = calculate_metrics(team_shot_events)

    pitch, fig, ax = setup_pitch(bg, text_color)

    plot_events(ax, team_shot_events, pitch, bg)
    add_metrics_boxes(ax, pitch, values, start_x, spacing, text_color, bg)

    rectangle = patches.Rectangle((20, 60.1), 40, 10, linewidth=2, facecolor=bg, zorder=2)
    ax.add_patch(rectangle)

    ax1 = fig.add_axes((0.93, 0.06, 0.5, 0.815))
    add_metric_labels(ax1, text_color, line_color)

    # Player positions
    positiondict = {'line': [[0.9, .65], [1.04, .65], [1.18, .65], [1.32, .65], [1.46, .65]]}
    positiondict1 = {'line1': [[0.9, .452], [1.07, .452], [1.24, .452]]}
    positiondict2 = {'line2': [[0.9, .264], [1.07, .264], [1.24, .264]]}

    # plot_top_players(team_shot_events, team_shot_events, positiondict, 'line', 'total_goals', folder_path, line_color, text_color, bodyfont, ascending=True)
    # plot_top_players(team_shot_events, team_shot_events, positiondict1, 'line1', 'total_shots', folder_path, line_color, text_color, bodyfont)
    # plot_top_players(team_shot_events, team_shot_events, positiondict2, 'line2', 'total_xg', folder_path, line_color, text_color, bodyfont)

    fig.set_facecolor(bg)

    return fig, ax
