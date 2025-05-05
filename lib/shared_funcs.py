import os
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import Standardizer

def extract_team_info(df, save_suffix):
    home_team = df['match_home_team_name'].dropna().iloc[0]
    away_team = df['match_away_team_name'].dropna().iloc[0]
    home_prefix = home_team[:3].upper()
    away_prefix = away_team[:3].upper()
    save_string = f"{home_prefix}{away_prefix}{save_suffix}"

    team_info = {
        "home_team": home_team,
        "away_team": away_team,
        "home_prefix": home_prefix,
        "away_prefix": away_prefix,
        "save_string": save_string,
    }

    return team_info

def format_date(date_str):
    date = pd.to_datetime(date_str)
    day = date.day
    suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th') if not (11 <= day <= 13) else 'th'
    return date.strftime(f'%-d{suffix} %B %Y')

def format_match_info(df, team_info):
    home_prefix = team_info['home_prefix']
    away_prefix = team_info['away_prefix']
    df['formatted_date'] = df['match_date'].apply(format_date)
    match_date = format_date(df['match_date'].iloc[0])
    match_comp = str(df['competition_name'].iloc[0])
    match_season = str(df['season_name'].iloc[0])
    home_goals = int(df[(df['outcome'] == 'goal') & (df['team_name'] == df['match_home_team_name'])].shape[0])
    away_goals = int(df[(df['outcome'] == 'goal') & (df['team_name'] == df['match_away_team_name'])].shape[0])
    match_score = f"{home_goals} - {away_goals}"
    comp_prefix = match_comp[:3].upper()
    folder_name = f"{home_prefix}{away_prefix}{comp_prefix}"

    match_info = {
        "match_date": match_date,
        "match_comp": match_comp,
        "match_season": match_season,
        "match_score": match_score,
        "comp_prefix": comp_prefix,
        "folder_name": folder_name
    }
    
    return match_info


def save_plot(fig, match_info, team_info, visualisation_params):
    # Extract background color from visualisation_params
    bg = visualisation_params['bg']
    folder_name = match_info['folder_name']
    save_string = team_info['save_string']
    
    # Create the output directory if it doesn't exist
    output_dir = f"./output/{folder_name}"
    os.makedirs(output_dir, exist_ok=True)

    # Save the plot with the specified background color
    fig.savefig(f"{output_dir}/{save_string}.jpeg", bbox_inches='tight', facecolor=bg)

    print(f"Plot saved to {output_dir}/{save_string}.jpeg")


def preprocess_data(df, pitch_length=105, pitch_width=68):
    statsbomb_to_uefa = Standardizer(pitch_from='statsbomb', pitch_to='uefa', length_to=pitch_length, width_to=pitch_width)
    df.start_x, df.start_y = statsbomb_to_uefa.transform(df.start_x, df.start_y)
    df.end_x, df.end_y = statsbomb_to_uefa.transform(df.end_x, df.end_y)
    return df




# def get_team_data(df, team_info, return_range=False):
#     df['qualifiers'] = df['qualifiers'].astype(str)

#     if return_range:
#         start_min = df.expanded_minute.min()
#         end_min = df.expanded_minute.max()
#         return start_min, end_min
    
#     # Use team_info dictionary to access home and away teams
#     home_team = team_info['home_team']
#     away_team = team_info['away_team']

#     # Filter the DataFrame for the specified team
#     team_data = df[(df['name'].isin([home_team, away_team])) & 
#                     (df['is_touch'] == True) & 
#                     (~df['qualifiers'].str.contains('CornerTaken|Freekick|ThrowIn'))]

#     return team_data

# def preprocess_xg_data(df):
#     shot_df = df.copy()
#     shot_df = shot_df[(shot_df['type_display_name'] == 'MissedShots') | (shot_df['type_display_name'] == 'ShotOnPost') | (shot_df['type_display_name'] == 'SavedShot') | (shot_df['type_display_name'] == 'Goal')]
#     shot_df = shot_df[['expanded_minute','second','period_display_value','player_name','event_type','team_name','home_team','away_team','expected_goals','home_cumulative_xg','away_cumulative_xg','home_cumulative_score','away_cumulative_score']]
#     shot_df['max_xg'] = np.maximum(shot_df['home_cumulative_xg'], shot_df['away_cumulative_xg'])
#     shot_df['time'] = shot_df['expanded_minute'] + shot_df['second'] / 60
#     highest_value = shot_df['max_xg'].max()
#     return shot_df, highest_value

# def preprocess_pass_data(pass_df):
#     pass_df = cumulative_match_mins(pass_df)
#     pass_df = insert_ball_carries(pass_df, min_carry_length=3, max_carry_length=60, min_carry_duration=1, max_carry_duration=10)
#     pass_df['index'] = range(1, len(pass_df) + 1)
#     pass_df = pass_df[['index'] + [col for col in pass_df.columns if col != 'index']]
#     return pass_df

