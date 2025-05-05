import matplotlib.patheffects as path_effects
import pandas as pd

def format_date(date_str):
    date = pd.to_datetime(date_str)
    day = date.day
    if 11 <= day <= 13:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    return date.strftime(f'%-d{suffix} %B %Y')

def path_effect_stroke(**kwargs):
    return [path_effects.Stroke(**kwargs), path_effects.Normal()]

def extract_team_info(stats_df):
    home_team = stats_df['team_name'].iloc[0]
    away_team = stats_df['team_name'].iloc[1]
    home_row = stats_df.iloc[0]
    away_row = stats_df.iloc[1]
    home_prefix = home_team[:3].upper()
    away_prefix = away_team[:3].upper()
    save_string = f"{home_prefix}{away_prefix}dash"
    return home_team, away_team, home_row, away_row, save_string

def format_match_details(stats_df):
    stats_df['formatted_date'] = stats_df['match_kick_off'].apply(format_date)
    match_date = format_date(stats_df['match_kick_off'].iloc[0])
    match_comp = str(stats_df['comp_name'].iloc[0])
    match_season = str(stats_df['season_name'].iloc[0])
    home_goals = stats_df.iloc[0]['total_goals']
    away_goals = stats_df.iloc[1]['total_goals']
    match_score = f"{home_goals} - {away_goals}"
    return match_date, match_score, match_comp, match_season

def get_team_colors(home_team, away_team):
    """Determine team colors based on team names."""
    if home_team == 'Arsenal':
        return '#be0a24', '#959595'
    if away_team == 'Arsenal':
        return '#959595', '#be0a24'
    return '#FFFFFF', '#000000'
