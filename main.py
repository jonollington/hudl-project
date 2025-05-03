import matplotlib.pyplot as plt


from fetch.shot_events import get_shot_events
from lib.shared_viz_funcs import get_team_colors, setup_visualisation_params


# Fetch data
shot_events = get_shot_events(1358854)


##############################################################

# Prepare team info and visualisation parameters for each plot

##############################################################

## Shot Map
# team_info = extract_team_info(match_events, "shot_map")
# match_info = format_match_info(match_events, team_info)
# visualisation_params = setup_visualisation_params(theme='dark')
# team_colors = get_team_colors(team_info, theme='dark')

# # Create and save
# fig, ax = create_high_turnover(match_events, visualisation_params, team_colors, match_info, team_info)
# save_plot(fig, match_info, team_info, visualisation_params)
