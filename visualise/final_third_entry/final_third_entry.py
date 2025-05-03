import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image
import matplotlib.patheffects as path_effects
from mplsoccer import VerticalPitch, arrowhead_marker

from .final_third_helpers import analyse_final_third_entries, plot_stats


def create(match_events_df, team_info, visualisation_params, match_info):
    bg = visualisation_params['bg']
    line_color = visualisation_params['line_color']
    pitch_line_color = visualisation_params['pitch_line_color']
    pass_color = visualisation_params['pass_color']
    carry_color = visualisation_params['carry_color']
    text_color = visualisation_params['text_color']
    titlefont = visualisation_params['titlefont']

    match_comp = match_info['match_comp']
    match_date = match_info['match_date']
    match_score = match_info['match_score']

    home_team = team_info['home_team']
    away_team = team_info['away_team']

    # Filter passes and carries for final third entries
    df_pass = match_events_df[(match_events_df['team_name'] == 'Arsenal') & 
                         (match_events_df['type_display_name'] == 'Pass') & 
                         (match_events_df['x'] < 70) & 
                         (match_events_df['end_x'] >= 70) & 
                         (match_events_df['outcome_type_display_name'] == 'Successful') & 
                         (~match_events_df['qualifiers'].fillna('').str.contains('Freekick', na=False))]

    df_carry = match_events_df[(match_events_df['team_name'] == 'Arsenal') & 
                         (match_events_df['type_display_name'] == 'Carry') & 
                         (match_events_df['x'] < 70) & 
                         (match_events_df['end_x'] >= 70) & 
                         (match_events_df['outcome_type_display_name'] == 'Successful') & 
                         (~match_events_df['qualifiers'].fillna('').str.contains('Freekick', na=False))]
    
    pitch = VerticalPitch(corner_arcs=True, pitch_color=bg, line_color=pitch_line_color, linewidth=1.5,
                      line_zorder=2, goal_type='box', half=False, pitch_type='uefa', pad_bottom=0.1)

    fig, ax = pitch.draw(figsize=(10, 7.727))
    ax.set_xlim(-0.5, 105.5)

    pitch.draw(ax=ax)
    # ax.set_xlim(-0.5, 105.5)
    ax.set_ylim(-5, 110)

    ax.vlines(22.67, ymin=0, ymax=70, colors=line_color, linestyle='dashed', alpha=0.55)
    ax.vlines(45.33, ymin=0, ymax=70, colors=line_color, linestyle='dashed', alpha=0.55)
    ax.hlines(70, xmin=0, xmax=68, colors=line_color, linestyle='dashed', alpha=0.55)

    pass_count = len(df_pass) + len(df_carry)

    # Plot passes and carries
    pitch.lines(df_pass.x, df_pass.y, df_pass.end_x, df_pass.end_y, comet=True, 
                color=pass_color, ax=ax, transparent=True, lw=5, alpha_start=0, alpha_end=0.3, zorder=3)
    pitch.scatter(df_pass.end_x, df_pass.end_y, s=50, edgecolor=pass_color, linewidth=2,
                  color=bg, zorder=4, ax=ax, alpha=0.7)

    # #Add player names to the start of the passes
    # for _, row in df_pass.iterrows():
    #     ax.text(row['y'], row['x'], row['player_name'], fontsize=10, color=home_color, 
    #             ha='center', va='center', zorder=5, alpha=0.9)  # Adjust text placement

    angle, distance = pitch.calculate_angle_and_distance(df_carry['x'], df_carry['y'],
    df_carry['end_x'], df_carry['end_y'], standardized=False, degrees=True)
    
    # Draw lines and scatter arrows
    pitch.lines(df_carry['x'], df_carry['y'], df_carry['end_x'], df_carry['end_y'], comet=True,
                transparent=True, lw=5, alpha_start=0, alpha_end=0.5, color=carry_color, ax=ax, zorder=3)
    pitch.scatter([df_carry['end_x']], [df_carry['end_y']], rotation_degrees=angle, color=carry_color,
                  alpha=0.8, s=100, ax=ax, marker=arrowhead_marker, zorder=4)

    # #Add player names to the start of the arrow
    # for _, row in df_carry.iterrows():
    #     ax.text(row['y'], row['x'], row['player_name'], fontsize=10, color=home_color, 
    #             ha='center', va='center', zorder=5, alpha=0.9)  # Adjust position as needed

    ax.text(70, 105, '<------------ final third ------------>', 
        color=text_color, ha='center', va='top', rotation=90, fontsize=12)

    # calculating the counts
    left_entry = len(df_pass[df_pass['y']>=45.33]) + len(df_carry[df_carry['y']>=45.33])
    mid_entry = len(df_pass[(df_pass['y']>=22.67) & (df_pass['y']<45.33)]) + len(df_carry[(df_carry['y']>=22.67) & (df_carry['y']<45.33)])
    right_entry = len(df_pass[(df_pass['y']>=0) & (df_pass['y']<22.67)]) + len(df_carry[(df_carry['y']>=0) & (df_carry['y']<22.67)])
    left_percentage = round((left_entry/pass_count)*100)
    mid_percentage = round((mid_entry/pass_count)*100)
    right_percentage = round((right_entry/pass_count)*100)

    # showing the texts in the pitch
    bbox_props = dict(boxstyle="round,pad=0.2", edgecolor="w", facecolor='w', alpha=0.2)
    
    ax.text(11.5, 11.335, f'{right_entry}\n({right_percentage}%)', color='w', fontsize=24, weight='bold',
            va='center', ha='center', bbox=bbox_props, path_effects=[path_effects.withStroke(linewidth=2, foreground=bg)])
    ax.text(34, 11.335, f'{mid_entry}\n({mid_percentage}%)', color='w', fontsize=24, weight='bold',
            va='center', ha='center', bbox=bbox_props, path_effects=[path_effects.withStroke(linewidth=2, foreground=bg)])
    ax.text(56.5, 11.335, f'{left_entry}\n({left_percentage}%)', color='w', fontsize=24, weight='bold',
            va='center', ha='center', bbox=bbox_props, path_effects=[path_effects.withStroke(linewidth=2, foreground=bg)])
    
    # Set title for the shot map
    ax.set_title("final third entries".upper(), size=30, weight='black', family=titlefont,
                y=1.05, ha='center', va='center', style='italic', c='w')
    ax.text(0.5, 1.02, match_comp+' • '+match_date+' • '+home_team+' '+match_score+' '+away_team, size=12, ha='center', va='center', c=text_color,transform=ax.transAxes)

    # Create an additional axis for defensive stats
    ax1 = fig.add_axes((0.72, 0.06, 0.38, 0.815))
    ax1.axis('off')

    # Plot stats
    grouped_carry, grouped_pass = analyse_final_third_entries(df_pass, df_carry)
    plot_stats(ax1, df_pass, df_carry, grouped_carry, grouped_pass, visualisation_params)

    # Set figure background color
    fig.patch.set_facecolor(bg)
    ax.set_facecolor(bg)

    fig.text(1.09, 0.03, '@ j o n o l l i n g t o n',
            ha='right', fontsize=15, color=text_color)

    ax2 = fig.add_axes([1,0.91,0.1,0.1]) # badge
    ax2.axis("off")
    img = Image.open('../logo/colour/cannonSilver.png')
    ax2.imshow(img)

    return fig, ax

    