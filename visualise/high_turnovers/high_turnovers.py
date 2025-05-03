import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import matplotlib.patches as mpatches
from mplsoccer import VerticalPitch

from lib.possession_chains import get_possession_chains


def create(match_events, visualisation_params, team_colors, match_info, team_info):

    df = get_possession_chains(match_events, 5, 3)
    df['period_display_value'] = df['period_display_value'].replace({1: 'FirstHalf', 2: 'SecondHalf', 3: 'FirstPeriodOfExtraTime', 4: 'SecondPeriodOfExtraTime', 
                                     5: 'PenaltyShootout', 14: 'PostGame', 16: 'PreMatch'})

    # final df is ready here
    df = df[df['period_display_value']!='PenaltyShootout']
    df = df.reset_index(drop=True)

    pitch_line_color = visualisation_params['pitch_line_color']
    bg = visualisation_params['bg']
    titlefont = visualisation_params['titlefont']
    bodyfont = visualisation_params['bodyfont']
    away_color = team_colors['away_color']
    
    pitch = VerticalPitch(corner_arcs=True, pitch_color=bg, line_color=pitch_line_color, linewidth=1.5,
                      line_zorder=2, goal_type='box', half=False, pitch_type='uefa', pad_bottom=0.1)
    fig,ax=plt.subplots(figsize=(10,10))
    pitch.draw(ax=ax)

    # High Turnover means any sequence which starts in open play and within 40 metres of the opponent's goal 
    high_turn_over_df = df.copy()
    high_turn_over_df['distance'] = ((high_turn_over_df['uefa_x'] - 105)**2 + (high_turn_over_df['uefa_y'] - 34)**2)**0.5

    # HTO which led to Goal for away team
    goal_count = 0
    # Iterate through the DataFrame
    for i in range(len(high_turn_over_df)):
        if ((high_turn_over_df.loc[i, 'type_display_name'] in ['BallRecovery', 'Interception']) and 
            (high_turn_over_df.loc[i, 'team_name'] == 'Arsenal') and 
            (high_turn_over_df.loc[i, 'distance'] <= 40)):
            
            possession_id = high_turn_over_df.loc[i, 'possession_id']
            
            # Check the following rows within the same possession
            j = i + 1
            while j < len(high_turn_over_df) and high_turn_over_df.loc[j, 'possession_id'] == possession_id and high_turn_over_df.loc[j, 'team_name']=='Arsenal':
                if high_turn_over_df.loc[j, 'type_display_name'] == 'Goal' and high_turn_over_df.loc[j, 'team_name']=='Arsenal':
                    ax.scatter(high_turn_over_df.loc[i, 'uefa_y'],high_turn_over_df.loc[i, 'uefa_x'], s=600, marker='*', color='#a78d58', edgecolor=bg, zorder=4)
                    goal_count += 1
                    break
                j += 1

    # HTO which led to Shot for away team
    shot_count = 0
    # Iterate through the DataFrame
    for i in range(len(high_turn_over_df)):
        if ((high_turn_over_df.loc[i, 'type_display_name'] in ['BallRecovery', 'Interception']) and 
            (high_turn_over_df.loc[i, 'team_name'] == 'Arsenal') and 
            (high_turn_over_df.loc[i, 'distance'] <= 40)):
            
            possession_id = high_turn_over_df.loc[i, 'possession_id']
            
            # Check the following rows within the same possession
            j = i + 1
            while j < len(high_turn_over_df) and high_turn_over_df.loc[j, 'possession_id'] == possession_id and high_turn_over_df.loc[j, 'team_name']=='Arsenal':
                if ('Shot' in high_turn_over_df.loc[j, 'type_display_name']) and (high_turn_over_df.loc[j, 'team_name']=='Arsenal'):
                    ax.scatter(high_turn_over_df.loc[i, 'uefa_y'],high_turn_over_df.loc[i, 'uefa_x'], s=150, color=away_color, edgecolor=bg, zorder=3)
                    shot_count += 1
                    break
                j += 1
    
    #other HTO for away team
    
    ht_count = 0
    p_list = []
    # Iterate through the DataFrame
    for i in range(len(high_turn_over_df)):
        if ((high_turn_over_df.loc[i, 'type_display_name'] in ['BallRecovery', 'Interception']) and 
            (high_turn_over_df.loc[i, 'team_name'] == 'Arsenal') and 
            (high_turn_over_df.loc[i, 'distance'] <= 40)):
            
            # Check the following rows
            j = i + 1
            if ((high_turn_over_df.loc[j, 'team_name']=='Arsenal') and
                (high_turn_over_df.loc[j, 'type_display_name']!='Dispossessed') and (high_turn_over_df.loc[j, 'type_display_name']!='OffsidePass')):
                ax.scatter(high_turn_over_df.loc[i, 'uefa_y'],high_turn_over_df.loc[i, 'uefa_x'], s=100, color='None', edgecolor=away_color, zorder=2)
                ht_count += 1
                p_list.append(high_turn_over_df.loc[i, 'player_name'])

    
    patches = [
        # Arc
        {"type": mpatches.Arc, "args": ((34, 105),), 
         "kwargs": {"height": 2*40, "width": 2*40, "angle": 180, "theta1": 0, "theta2": 180, 
                    "color": pitch_line_color, "ls": (2, (2, 2)), "lw": 1, "alpha": 1, "zorder": 2}},
        
        # Wedge
        {"type": mpatches.Wedge, "args": ((34, 105), 40, 180, 0), 
         "kwargs": {"facecolor": 'w', "edgecolor": 'none', "zorder": 3, "alpha": 0.05}},
        
        # Rectangles
        {"type": mpatches.Rectangle, "args": ((68.15, 80), 10, 26), 
         "kwargs": {"linewidth": 1, "facecolor": bg, "zorder": 5}},
        
        {"type": mpatches.Rectangle, "args": ((-0.19, 80), -10, 26), 
         "kwargs": {"linewidth": 1, "facecolor": bg, "zorder": 5}},
        ]

    # Loop to add patches
    for patch_info in patches:
        patch = patch_info["type"](*patch_info["args"], **patch_info["kwargs"])
        ax.add_patch(patch)


    start_x = 19
    spacing = 15
    labels = ['goal\nending', 'shot\nending', 'high\nturnover']
    
    values = [goal_count, shot_count, ht_count]
    
    for i, label in enumerate(labels):
        x_position = start_x + i * spacing
        y_position = 20
    
        pitch.scatter(y_position, x_position, s=3000, ax=ax, marker='s', color='#e7e7e7', alpha=0.2, zorder=10)
    
        ax.text(x_position, y_position - 12, label, va='center', ha='center', size=18, color='white',zorder=11)
        ax.text(x_position, y_position - 0.1, str(values[i]), va='center', ha='center', size=32, weight='black', color='white',
                   path_effects=[path_effects.withStroke(linewidth=5, foreground='black')],zorder=11)

    rectangle = mpatches.Rectangle((13, 0.13), 42, 25, linewidth=2, facecolor=bg,zorder=3)
    ax.add_patch(rectangle)

    home_team = team_info['home_team']
    away_team = team_info['away_team']

    match_comp = match_info['match_comp']
    match_score = match_info['match_score']
    match_date = match_info['match_date']

    fig.text(0.5, 0.94, "High Turnovers".upper(),
         size=35, c='w', fontfamily=titlefont, ha='center', va='center',
         fontweight='black', zorder=2, style='italic')

    fig.text(0.5, 0.9, match_comp+" • "+home_team+" "+match_score+" "+away_team+" • "+match_date,
            size=14, c='#a78d58', fontfamily=bodyfont, ha='center', va='center')

    fig.text(0.75, 0.06, '@ j o n o l l i n g t o n', size=14, c='#a78d58', ha='right', va='center', weight='bold')

    return fig, ax