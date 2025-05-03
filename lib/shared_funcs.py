import os
import pandas as pd
import matplotlib.pyplot as plt

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
    df['formatted_date'] = df['kick_off_at'].apply(format_date)
    match_date = format_date(df['kick_off_at'].iloc[0])
    match_comp = str(df['competition_name'].iloc[0])
    match_season = str(df['season'].iloc[0])
    if 'home_goals' in df.columns and 'away_goals' in df.columns:
        home_goals = int(df['home_goals'].sum())
        away_goals = int(df['away_goals'].sum())
    elif 'home_cumulative_score' in df.columns and 'away_cumulative_score' in df.columns:
        home_goals = int(df['home_cumulative_score'].max())
        away_goals = int(df['away_cumulative_score'].max())
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
