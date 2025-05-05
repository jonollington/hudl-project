import numpy as np

def plot_goal_post_away(ax, shots_df, pitch2, line_color, away_color):
    
    away_team_id = shots_df['away_team_id'].iloc[1]
    away_team_name = shots_df[shots_df['team_id'] == away_team_id]['name'].iloc[0]
    away_shot_df = shots_df[(shots_df['team_id'] == away_team_id) & (shots_df['own_goal'] == False)].copy()
    

    pitch2.draw(ax=ax)
    line_width = 6

    # Filter the DataFrame for goals
    goals_df = away_shot_df[away_shot_df['type_display_name'] == 'Goal'].copy()

    # Filter the DataFrame for non-goals (shots)
    shots_df = away_shot_df[(away_shot_df['type_display_name'] != 'Goal') & (away_shot_df['blocked_shot'] != True) & (away_shot_df['type_display_name'] != 'MissedShots')].copy()

    # Old and new ranges for scaling (you might want to adjust these ranges)
    old_min_y, old_max_y = 44.5, 55.5
    new_min_y, new_max_y = 0, 100
    old_min_z, old_max_z = 0, 41
    new_min_z, new_max_z = 20, 80

    # Apply the transformation for goals
    goals_df['goal_mouth_y_scaled'] = ((goals_df['goal_mouth_y'] - old_min_y) / (old_max_y - old_min_y)) * (new_max_y - new_min_y) + new_min_y
    goals_df['goal_mouth_z_scaled'] = ((goals_df['goal_mouth_z'] - old_min_z) / (old_max_z - old_min_z)) * (new_max_z - new_min_z) + new_min_z

    # Apply the transformation for shots
    shots_df['goal_mouth_y_scaled'] = ((shots_df['goal_mouth_y'] - old_min_y) / (old_max_y - old_min_y)) * (new_max_y - new_min_y) + new_min_y
    shots_df['goal_mouth_z_scaled'] = ((shots_df['goal_mouth_z'] - old_min_z) / (old_max_z - old_min_z)) * (new_max_z - new_min_z) + new_min_z

    # Define x and y data for goals and shots
    x_goals = goals_df['goal_mouth_y_scaled']
    y_goals = goals_df['goal_mouth_z_scaled']
    x_shots = shots_df['goal_mouth_y_scaled']
    y_shots = shots_df['goal_mouth_z_scaled']

    # Plot goals on the pitch
    pitch2.scatter(x_goals, y_goals, marker='football', zorder=4, s=350, ax=ax)

    # Plot shots on the pitch
    pitch2.scatter(x_shots, y_shots, marker='o', color=away_color, ec='w',zorder=3, s=350, ax=ax, alpha=0.8)

    # Left Vertical Line
    ax.plot([0.5, 0.5], [20, 80], color=line_color, linewidth=line_width)  # Left vertical line
    # Top Horizontal Line
    ax.plot([0.5, 99.9], [80, 80], color=line_color, linewidth=line_width)  # Top horizontal line
    # Right Vertical Line
    ax.plot([99.9, 99.9], [20, 80], color=line_color, linewidth=line_width)  # Right vertical line
    # plotting the home net
    y_values = np.linspace(20, 80, num=8)

    for y in y_values:
        ax.plot([0.5, 99.9], [y, y], color=line_color, linewidth=2, alpha=0.2)

    x_values = np.linspace(0, 100, num=12)
    for x in x_values:
        ax.plot([x, x], [20, 80], color=line_color, linewidth=2, alpha=0.2)

    shots_count = len(
    away_shot_df[
        (away_shot_df['type_display_name'] == 'Goal') |
        (away_shot_df['type_display_name'] == 'SavedShot') &
        (away_shot_df['blocked_shot'] != True)
    ])
    
    # Define the bounding box properties
    away_shots_bbox = dict(boxstyle="round,pad=0.3", facecolor=away_color)

    # Place the text without a bounding box
    ax.text(100, 90, f"{away_team_name} shots on target", color='silver', fontsize=20, ha='left')

    # Place the number with a bounding box right after the text
    ax.text(0, 90, f"{shots_count}", color='w', fontsize=20, ha='right', weight='bold', bbox=away_shots_bbox)
    
    ax.set_xlim(101, -1)
    ax.set_ylim(0, 101)