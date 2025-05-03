
bg, titlefont, bodyfont, text_color, line_color, folder_path = setup_visualisation_params()
df, xg_df = load_and_preprocess_data(WHOSCORED_MATCH_ID, FOTMOB_MATCH_ID, 'Arsenal')

home_team, away_team, home_prefix, away_prefix, save_string = extract_team_info(df)
match_date, match_score, match_comp, match_season = format_match_details(df)

labels, values, start_x, spacing = calculate_metrics(df)
xG_min, xG_max = df['expected_goals_on_target'].min(), df['expected_goals_on_target'].max()
norm = mcolors.Normalize(vmin=xG_min, vmax=xG_max)

pitch, fig, ax, cmap = setup_pitch_and_colormap(bg, text_color)
plot_events(ax, df, pitch, cmap, norm, bg)
add_metrics_boxes(ax, pitch, values, start_x, spacing, text_color, bg)

rectangle = patches.Rectangle((17, 52.57), 30, 20, linewidth=2, facecolor=bg, zorder=2)
ax.add_patch(rectangle)

ax1 = fig.add_axes((0.93, 0.06, 0.5, 0.815))
add_metric_labels(ax1, text_color, line_color)

# Player plot dictionaries
positiondict = {'line':[[0.9,.65],[1.04,.65],[1.18,.65],[1.32,.65],[1.46,.65]]}
positiondict1 = {'line1':[[0.9,.452],[1.07,.452],[1.24,.452]]}
positiondict2 = {'line2':[[0.9,.264],[1.07,.264],[1.24,.264]]}
positiondict3 = {'line3':[[0.9,.076],[1.07,.076],[1.24,.076]]}

plot_top_players(df, xg_df, positiondict, 'line', 'total_goals', folder_path, line_color, text_color, bodyfont, ascending=True)
plot_top_players(df, xg_df, positiondict1, 'line1', 'total_shots', folder_path, line_color, text_color, bodyfont)
plot_top_players(df, xg_df, positiondict2, 'line2', 'total_xg', folder_path, line_color, text_color, bodyfont)
plot_top_players(df, xg_df, positiondict3, 'line3', 'total_xgot', folder_path, line_color, text_color, bodyfont)

fig.set_facecolor(bg)