def plot_shots(shots_df, pitch, ax, home_color, away_color):
    """
    Splits the shots data by team and plots it on the pitch.
    
    Parameters:
    - shots_df: DataFrame containing all shots data.
    - pitch: An instance of the Pitch class from mplsoccer.
    - ax: The axes on which to plot the data.
    - home_color: The color to use for the home team's shots.
    - away_color: The color to use for the away team's shots.
    """
    home_team_id = shots_df['home_team_id'].iloc[0]
    away_team_id = shots_df['away_team_id'].iloc[0]
    
    home_shot_df = shots_df[(shots_df['team_id'] == home_team_id)].copy()
    home_shot_df = home_shot_df[(home_shot_df['team_id'] == home_team_id) & (home_shot_df['own_goal'] == False)]
    home_goal_df = shots_df[(shots_df['team_id'] == home_team_id) & (shots_df['type_display_name'] == 'Goal') & (shots_df['own_goal'] == False)]
    home_own_goal_df = shots_df[(shots_df['team_id'] == home_team_id) & (shots_df['own_goal'] == True)]
    
    away_shot_df = shots_df[(shots_df['team_id'] == away_team_id)].copy()
    away_shot_df = shots_df[(shots_df['team_id'] == away_team_id) & (shots_df['own_goal'] == False)]
    away_goal_df = shots_df[(shots_df['team_id'] == away_team_id) & (shots_df['type_display_name'] == 'Goal') & (shots_df['own_goal'] == False)]
    away_own_goal_df = shots_df[(shots_df['team_id'] == away_team_id) & (shots_df['own_goal'] == True)]

    # Plot home team data
    pitch.scatter(100 - home_shot_df.x, 100 - home_shot_df.y, ax=ax, color=home_color, ec='w', alpha=0.7, s=200)
    pitch.scatter(100 - home_goal_df.x, 100 - home_goal_df.y, marker='football', c='w', ax=ax, alpha=0.9, s=250)
    pitch.scatter(100 - home_own_goal_df.x, 100 - home_own_goal_df.y, marker='football', c='w', ec='red', lw=1.1, ax=ax, alpha=0.9, s=250)

    # Plot away team data
    pitch.scatter(away_shot_df.x, away_shot_df.y, ax=ax, color=away_color, ec='w', alpha=0.7, s=200)
    pitch.scatter(away_goal_df.x, away_goal_df.y, marker='football', c='w', ax=ax, alpha=0.9, s=250)
    pitch.scatter(away_own_goal_df.x, away_own_goal_df.y, marker='football', c='w', ec='red', lw=1.1, ax=ax, alpha=0.9, s=250)

    home_shots_count = len(
    home_shot_df[
        (home_shot_df['type_display_name'] == 'Goal') |
        (home_shot_df['type_display_name'] == 'SavedShot') |
        (home_shot_df['type_display_name'] == 'ShotOnPost') |
        (home_shot_df['type_display_name'] == 'MissedShots')
        ])

    away_shots_count = len(
    away_shot_df[
        (away_shot_df['type_display_name'] == 'Goal') |
        (away_shot_df['type_display_name'] == 'SavedShot') |
        (away_shot_df['type_display_name'] == 'ShotOnPost') |
        (away_shot_df['type_display_name'] == 'MissedShots')
        ])

    ax.text(50, 107, 'Total shots (incl. blocked)', size=20, c='silver', ha='center', va='center')
    home_shots_bbox = dict(boxstyle='round,pad=0.2', facecolor=home_color, alpha=0.9)
    away_shots_bbox = dict(boxstyle='round,pad=0.2', facecolor=away_color, alpha=0.9)
    ax.text(0, 107, str(home_shots_count), size=22, c='w', weight='bold', ha='left', va='center', bbox=home_shots_bbox)
    ax.text(100, 107, str(away_shots_count), size=22, c='w', weight='bold',ha='right', va='center', bbox=away_shots_bbox)