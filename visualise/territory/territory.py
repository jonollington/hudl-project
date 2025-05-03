import matplotlib.pyplot as plt
from highlight_text import ax_text, fig_text
from matplotlib.colors import LinearSegmentedColormap
from mplsoccer import Pitch

from .territory_helpers import create_heatmap, plot_texts, add_pitch_lines

def create(df1, df2, team_info, team_colors, visualisation_params, match_info):
    
    # Extract visualization parameters from the dictionary
    bg = visualisation_params['bg']
    line_color = visualisation_params['line_color']

    match_comp = match_info['match_comp']
    match_date = match_info['match_date']
    match_score = match_info['match_score']

    home_team = team_info['home_team']
    away_team = team_info['away_team']

    home_color = team_colors['home_color']
    away_color = team_colors['away_color']

    cmap = LinearSegmentedColormap.from_list("",  [away_color, 'gray', home_color], N=20)

    fig, ax = plt.subplots(figsize=(10, 10), facecolor=bg)

    pitch = Pitch(pitch_type='uefa',  goal_type='box', corner_arcs=True, pitch_color=bg, line_color=line_color, linewidth=2, line_zorder=6)
    pitch.draw(ax=ax)
    ax.set_ylim(-5, 68.5)
    ax.set_xlim(-3, 108)

    bin_statistic1 = pitch.bin_statistic(df1.x, df1.y, bins=(6, 5), statistic='count', normalize=False)
    bin_statistic2 = pitch.bin_statistic(df2.x, df2.y, bins=(6, 5), statistic='count', normalize=False)

    create_heatmap(ax, bin_statistic1, bin_statistic2, cmap, pitch)
    plot_texts(ax, home_team, away_team, home_color, away_color, line_color, match_comp, match_date, match_score, bg)
    add_pitch_lines(ax, bg)

    return fig, ax