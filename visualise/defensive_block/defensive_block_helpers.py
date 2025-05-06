import matplotlib.pyplot as plt

def plot_defensive_action_lines(ax, average_locs_and_count_df):
    # Plotting the average defensive actions height
    dah = round(average_locs_and_count_df['start_x'].mean(), 2)
    ax.axhline(y=dah, color='w', linestyle='--', alpha=0.75, linewidth=2)
    ax.text(
        68,
        dah + 1,
        f'Avg Def Actions {dah}m',
        color='w',
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold',
        bbox=dict(facecolor='w', edgecolor='none', boxstyle='round,pad=0.3', alpha=0.2)
    )

    # Plotting the average defensive line height
    center_backs_height = average_locs_and_count_df[average_locs_and_count_df['position'] == 'DC']
    def_line_h = round(center_backs_height['x'].median(), 2)
    ax.axhline(y=def_line_h, color='w', linestyle='dotted', alpha=0.5, linewidth=2)
    ax.text(
        68,
        def_line_h + 1,
        f'Avg Def Line Actions: {def_line_h}m',
        color='w',
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold',
        bbox=dict(facecolor='w', edgecolor='none', boxstyle='round,pad=0.3', alpha=0.2)
    )

    # Plotting the average forward line height
    forwards_height = average_locs_and_count_df[average_locs_and_count_df['is_first_eleven'] == True]
    forwards_height = forwards_height.sort_values(by='x', ascending=False).head(2)
    fwd_line_h = round(forwards_height['x'].mean(), 2)
    ax.axhline(y=fwd_line_h, color='w', linestyle='dotted', alpha=0.5, linewidth=2)
    ax.text(
        68,
        fwd_line_h + 1,
        f'Avg Fwd Line Actions {fwd_line_h}m',
        color='w',
        ha='center',
        va='bottom',
        fontsize=10,
        fontweight='bold',
        bbox=dict(facecolor='w', edgecolor='none', boxstyle='round,pad=0.3', alpha=0.2)
    )

    # Getting the compactness value 
    compactness = round((1 - ((fwd_line_h - def_line_h) / 105)) * 100, 2)
    ax.text(68/2, -4.5, f'Compactness: {compactness}%', fontsize=11, color='w', ha='center', va='center')

    import pandas as pd

MAX_MARKER_SIZE = 3500

def analyse_defensive_actions(average_locs_and_count_df, defensive_actions_df, team_name='Arsenal'):
    
    # Calculate marker size based on the count
    average_locs_and_count_df['marker_size'] = (average_locs_and_count_df['count'] / average_locs_and_count_df['count'].max()) * MAX_MARKER_SIZE

    # Filter the DataFrame for the specified team
    average_locs_and_count_df = average_locs_and_count_df[average_locs_and_count_df['team_name'] == team_name]

    # Create a DataFrame for defensive actions of the specified team
    defensive_actions_team_df = defensive_actions_df[defensive_actions_df["team_name"] == team_name]

    # Group defensive actions by player and action type
    defensive_actions_team_df_groupby = defensive_actions_team_df.groupby(['player_name', 'type_display_name', 'outcome_type_display_name']).size().reset_index(name='count')

    # Filter true tackles based on specific conditions
    true_tackles_interceptions = defensive_actions_team_df_groupby[
        ((defensive_actions_team_df_groupby['type_display_name'] == 'Tackle') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Successful')) |
        ((defensive_actions_team_df_groupby['type_display_name'] == 'Challenge') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Unsuccessful')) |
        ((defensive_actions_team_df_groupby['type_display_name'] == 'Foul') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Unsuccessful')) |
        ((defensive_actions_team_df_groupby['type_display_name'] == 'Interception') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Successful')) |
        ((defensive_actions_team_df_groupby['type_display_name'] == 'BlockedPass') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Successful'))
    ]

    # Group the true tackles by player name
    grouped_true_tackles_interceptions = true_tackles_interceptions.groupby(['player_name']).sum('count').reset_index()
    grouped_true_tackles_interceptions = grouped_true_tackles_interceptions.sort_values(by='count', ascending=False).head(3).reset_index(drop=True)


    # Filter aerial duels based on specific conditions
    aerial_duels = defensive_actions_team_df_groupby[
        ((defensive_actions_team_df_groupby['type_display_name'] == 'Aerial') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Successful'))
    ]

    # Group aerial duels by player name
    grouped_aerial_duels = aerial_duels.groupby(['player_name']).sum('count').reset_index()
    grouped_aerial_duels = grouped_aerial_duels.sort_values(by='count', ascending=False).head(3).reset_index(drop=True)

    # Filter recoveries based on specific conditions
    recoveries = defensive_actions_team_df_groupby[
        ((defensive_actions_team_df_groupby['type_display_name'] == 'BallRecovery') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Successful'))
    ]

    # Group recoveries by player name
    grouped_recoveries = recoveries.groupby(['player_name']).sum('count').reset_index()
    grouped_recoveries = grouped_recoveries.sort_values(by='count', ascending=False).head(3).reset_index(drop=True)

    # Filter recoveries based on specific conditions
    clearances = defensive_actions_team_df_groupby[
        ((defensive_actions_team_df_groupby['type_display_name'] == 'Clearance') & (defensive_actions_team_df_groupby['outcome_type_display_name'] == 'Successful'))
    ]

    # Group recoveries by player name
    grouped_clearances = clearances.groupby(['player_name']).sum('count').reset_index()
    grouped_clearances = grouped_clearances.sort_values(by='count', ascending=False).head(3).reset_index(drop=True)

    return average_locs_and_count_df, grouped_true_tackles_interceptions, grouped_aerial_duels, grouped_clearances, grouped_recoveries

def get_defensive_action_df(df, team_names):
    df['index'] = range(1, len(df) + 1)
    df = df[['index'] + [col for col in df.columns if col != 'index']]
    df['qualifiers'] = df['qualifiers'].astype(str)
    
    # Define the defensive action types
    defensive_actions = [
        'BallRecovery', 'BlockedPass', 'Challenge', 'Clearance', 
        'Error', 'Foul', 'Interception', 'Tackle'
    ]
    
    # Create a boolean mask for defensive actions
    mask = (
        (df['type_display_name'] == 'Aerial') & (df['qualifiers'].str.contains('Defensive')) |
        df['type_display_name'].isin(defensive_actions)
    )
    
    # Filter the DataFrame using the mask
    df_defensive_actions = df.loc[mask, [
        "index", "x", "y", "team_name", "player_id", "player_name", "shirt_no", 
        "type_display_name", "outcome_type_display_name",
        "position", "is_first_eleven"
    ]]

    return df_defensive_actions

def get_da_count_df(defensive_actions_df, df):
    # Check if necessary columns exist in the defensive actions DataFrame
    required_columns_da = ['player_id', 'x', 'y']
    if not all(col in defensive_actions_df.columns for col in required_columns_da):
        raise ValueError(f"defensive_actions_df must contain columns: {required_columns_da}")

    # Aggregate defensive actions
    average_locs_and_count_df = (defensive_actions_df
                                  .groupby('player_id')
                                  .agg({'x': 'median', 'y': ['median', 'count']}))
    
    average_locs_and_count_df.columns = ['x', 'y', 'count']
    average_locs_and_count_df = average_locs_and_count_df.reset_index()

    # Drop duplicates in df for 'player_id'
    df_unique = df[['player_id', 'player_name', 'shirt_no', 'position', 'is_first_eleven', 'team_name']].drop_duplicates(subset='player_id')

    # Merge with average locations and count DataFrame
    average_locs_and_count_df = average_locs_and_count_df.merge(df_unique, on='player_id', how='left')

    # Set player_id as index
    average_locs_and_count_df = average_locs_and_count_df.set_index('player_id')

    return average_locs_and_count_df

import matplotlib.pyplot as plt
from matplotlib import patheffects
from lib.player_plot import player_plot

def plot_defensive_stats(ax1, grouped_true_tackles_interceptions, grouped_aerial_duels, grouped_clearances, grouped_recoveries, folder_path, line_color, text_color, bodyfont, bg):
    # Define positions and labels

    vertical_shift = 0.9
    vertical_shift1 = 0.05
    positions = {
        "TRUE TACKLES + TRUE INTERCEPTIONS": (0.7, 0.65+vertical_shift1),
        "DEFENSIVE AERIAL DUELS WON": (0.7, 0.46+vertical_shift1),
        "CLEARANCES": (0.7, 0.27+vertical_shift1),
        "RECOVERIES": (0.7, 0.084+vertical_shift1)
    }
    y_lines = [11.5+vertical_shift, 8.5+vertical_shift, 5.5+vertical_shift, 2.5+vertical_shift]
    y_dots = [9.3+vertical_shift, 6.3+vertical_shift, 3.3+vertical_shift, 0.3+vertical_shift]
    text_y_positions = [11.8+vertical_shift, 8.8+vertical_shift, 5.8+vertical_shift, 2.8+vertical_shift]
    
    ax1.axis('off')
    ax1.set_ylim(0, 13)
    ax1.set_xlim(0, 3)

    # Adding labels
    for label, y in zip(positions.keys(), text_y_positions):
        ax1.text(x=0.1, y=y, s=label, size=15, va='center', ha='left', color='w')

    # Adding horizontal lines
    for y in y_lines:
        ax1.plot([0, 3], [y, y], lw='1.5', color='w')

    # Adding dotted lines
    for y in y_dots:
        ax1.plot([0, 3], [y, y], lw='0.5', color=line_color, linestyle='dotted')

    # Define a helper function for plotting players
    def plot_players(grouped_data, position_key):
        for i in range(min(len(grouped_data), 3)):  # Max 3 players per category
            pos = positions[position_key]
            spacing = 0.12  # Adjust this value for more or less space
            player_ax = plt.axes([pos[0] + i * spacing, pos[1], 0.1, 0.15])
            # player_ax = plt.axes([pos[0] + i * 0.17, pos[1], 0.1, 0.15])
            
            full_name = grouped_data.iloc[i]['player_name']
            
            # Use 'Gabriel' for Gabriel Magalhães, otherwise use the surname
            if 'Gabriel' in full_name:
                display_name = 'Gabriel'
            else:
                display_name = full_name.split()[-1]  # Get the surname

            player_plot(player_ax, display_name, folder_path, line_color, text_color, bodyfont, bg)
            count_to_display = str(grouped_data.iloc[i]['count'])
            player_ax.text(5.1, 2.4, count_to_display, size=22, va='center', ha='center',
                        color=text_color, weight='black',
                        path_effects=[patheffects.withStroke(linewidth=6, foreground=bg)])
            player_ax.axis('off')


    # Plotting tackles and interceptions
    plot_players(grouped_true_tackles_interceptions, "TRUE TACKLES + TRUE INTERCEPTIONS")
    plot_players(grouped_aerial_duels, "DEFENSIVE AERIAL DUELS WON")
    plot_players(grouped_clearances, "CLEARANCES")
    plot_players(grouped_recoveries, "RECOVERIES")



