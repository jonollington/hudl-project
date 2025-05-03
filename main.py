from lib.shared_funcs import extract_team_info, format_match_info, save_plot
from lib.shared_viz_funcs import get_team_colors, setup_visualisation_params


from fetch.shot_events import get_shot_events
from lib.shared_viz_funcs import get_team_colors, setup_visualisation_params
from lib.shared_funcs import extract_team_info, format_match_info, save_plot
from lib.shared_viz_funcs import get_team_colors, setup_visualisation_params



from visualise.shot_map.shot_map import create as create_shot_map


# Fetch data
shot_events = get_shot_events(1358854)


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
