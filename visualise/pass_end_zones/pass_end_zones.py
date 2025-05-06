import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
from mplsoccer import Pitch
from matplotlib.colors import LinearSegmentedColormap

def create_pass_end_zone(ax, team_name, cm, match_events, team_info, team_colors, visualisation_params):

    # Extract visualisation parameters and team colors
    bg = visualisation_params['bg']
    line_color = visualisation_params['line_color']
    text_color = visualisation_params['text_color']
    
    home_color = team_colors['home_color']
    away_color = team_colors['away_color']
    
    # Match team names
    home_team = team_info['home_team']
    away_team = team_info['away_team']


    pez_df = match_events[(match_events['team_name'] == team_name) & (match_events['name'] == 'pass') & (match_events['outcome'] == 'complete')]
    pitch = Pitch(pitch_type='statsbomb', line_color=line_color, goal_type='box', goal_alpha=.5, corner_arcs=True, line_zorder=2, pitch_color=bg, linewidth=2)
    pitch.draw(ax=ax)
    ax.set_xlim(-3, 123)
    if team_name == away_team:
        ax.invert_xaxis()
        ax.invert_yaxis()

    cmap = cm
    # binning the data points
    bin_statistic = pitch.bin_statistic(pez_df.end_x, pez_df.end_y, bins=(6, 5), normalize=True)
    pitch.heatmap(bin_statistic, ax=ax, cmap=cmap, edgecolors=None)
    pitch.label_heatmap(bin_statistic, color=text_color, fontsize=20, ax=ax, ha='center', va='center', str_format='{:.0%}', path_effects=[path_effects.Stroke(linewidth=5, foreground=bg), path_effects.Normal()])

    # Headings and other texts
    if team_name == home_team:
        ax.set_title(f"{home_team} Pass End Zone", color=line_color, fontsize=20, fontweight='bold', path_effects=[path_effects.Stroke(linewidth=5, foreground=bg), path_effects.Normal()])
    else:
        ax.set_title(f"{away_team} Pass End Zone", color=line_color, fontsize=20, fontweight='bold', path_effects=[path_effects.Stroke(linewidth=5, foreground=bg), path_effects.Normal()])

    def add_arrow(ax, x_start, y_start, x_end, y_end, color):
        arrow = "Simple, tail_width=0.05, head_width=0.8, head_length=0.8"
        ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                    arrowprops=dict(arrowstyle=arrow, color=color, alpha=1))

    if team_name == home_team:
        ax.text(0, 83, 'ATTACK', color=home_color, fontsize=10, ha='left', va='center', weight='bold')
        add_arrow(ax, 10, 83, 35, 83, home_color)
    else:
        ax.text(0, -3, 'ATTACK', color=away_color, fontsize=10, ha='right', va='center', weight='bold')
        add_arrow(ax, 10, -3, 35, -3, away_color)

def create(match_events, team_info, visualisation_params, team_colors, match_info):

    home_color = team_colors['home_color']
    away_color = team_colors['away_color']

    

    bg = visualisation_params['bg']
    line_color = visualisation_params['line_color']
    text_color = visualisation_params['text_color']

    home_team_colormap = LinearSegmentedColormap.from_list("",  [bg, home_color])
    away_team_colormap = LinearSegmentedColormap.from_list("",  [bg, away_color])

    home_team = team_info['home_team']
    away_team = team_info['away_team']
    
    fig, axs = plt.subplots(1, 2, figsize=(20, 10), facecolor=bg)

    create_pass_end_zone(axs[0], home_team, home_team_colormap, match_events, team_info, team_colors, visualisation_params)
    create_pass_end_zone(axs[1], away_team, away_team_colormap, match_events, team_info, team_colors, visualisation_params)


    # Add title and additional text to the figure
    fig.suptitle("Pass end zones: Where teams are passing", color=text_color, fontsize=30, fontweight='bold', x=0.5, y=0.87, ha='center')
    fig.text(0.5, 0.81, f"{match_info['match_comp']} • {match_info['match_date']} • {home_team} {match_info['match_score']} {away_team}", color=line_color, fontsize=15, ha='center', va='center')

    return fig, axs