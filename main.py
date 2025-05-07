import matplotlib.pyplot as plt  # Ensure plt is imported in main.py

from fetch.shot_events import get_shot_events
from fetch.match_events import get_match_data
from fetch.match_events import get_match_data

from lib.shared_viz_funcs import get_team_colors, setup_visualisation_params
from lib.shared_funcs import extract_team_info, format_match_info, save_plot, preprocess_data

from visualise.shot_map.shot_map import create as create_shot_map
from visualise.territory.territory import create as create_territory
from visualise.pass_end_zones.pass_end_zones import create as create_pass_end_zones
from visualise.chance_creation_zones.chance_creation_zones import create as create_chance_creation_zones


# Fetch data
shot_events = get_shot_events(1358854)
pass_events = get_match_data(1358854)
match_events = get_match_data(1358854)


##############################################################

# Prepare team info and visualisation parameters for each plot

##############################################################

## Shot Map
team_info = extract_team_info(shot_events, "shot_map")
match_info = format_match_info(shot_events, team_info)
visualisation_params = setup_visualisation_params(theme='light')
team_colors = get_team_colors(team_info, theme='light')

## Select Team
selected_team = 'Dunkerque'  # or 'Paris Saint-Germain'
# selected_team = away_team

# Filter the events
team_shot_events = shot_events[shot_events['team_name'] == selected_team]

# Create and save
fig, ax = create_shot_map(shot_events, team_info, team_colors, visualisation_params, match_info)
save_plot(fig, match_info, team_info, visualisation_params)


## Territory Plot
df = preprocess_data(pass_events)
team_info = extract_team_info(df, "territory")
match_info = format_match_info(df, team_info)
team_colors = get_team_colors(team_info, theme='trad')
visualisation_params = setup_visualisation_params(theme='dark')

# Apply transformations for territory
home_team = team_info['home_team']
away_team = team_info['away_team']

df1 = df[df['team_name'] == home_team]
df2 = df[df['team_name'] == away_team]

df2.loc[:, 'start_x'] = 105 - df2['start_x']  # Adjusting the x-coordinates for away team
df2.loc[:, 'start_y'] = 68 - df2['start_y']  # Adjusting the y-coordinates for away team

# Create and save
fig, ax = create_territory(df1, df2, team_info, team_colors, visualisation_params, match_info)
save_plot(fig, match_info, team_info, visualisation_params)


## Pass End Zone Plot
team_info = extract_team_info(match_events, 'pass_end_zones')
match_info = format_match_info(match_events, team_info)
visualisation_params = setup_visualisation_params(theme='light')
team_colors = get_team_colors(team_info, theme='light')

home_team = team_info['home_team']
away_team = team_info['away_team']


# Create and save
fig, axs = create_pass_end_zones(match_events, team_info, visualisation_params,  team_colors, match_info)
save_plot(fig, match_info, team_info, visualisation_params)


## Chance Creation Zone Plot
team_info = extract_team_info(match_events, 'chance_creation_zones')
match_info = format_match_info(match_events, team_info)
visualisation_params = setup_visualisation_params(theme='light')
team_colors = get_team_colors(team_info, theme='light')

home_team = team_info['home_team']
away_team = team_info['away_team']

# Create and save
fig, axs, stats_df = create_chance_creation_zones(match_events, team_info, visualisation_params, team_colors, match_info)
save_plot(fig, match_info, team_info, visualisation_params)