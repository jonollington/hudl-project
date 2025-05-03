


def get_defensive_action_df(df):

    df['qualifiers'] = df['qualifiers'].astype(str)
    # filter only defensive actions
    defensive_actions_ids = df.index[(df['type_display_name'] == 'Aerial') & (df['qualifiers'].str.contains('Defensive')) |
                                     (df['type_display_name'] == 'BallRecovery') |
                                     (df['type_display_name'] == 'BlockedPass') |
                                     (df['type_display_name'] == 'Challenge') |
                                     (df['type_display_name'] == 'Clearance') |
                                     (df['type_display_name'] == 'Error') |
                                     (df['type_display_name'] == 'Foul') |
                                     (df['type_display_name'] == 'Interception') |
                                     (df['type_display_name'] == 'Tackle')]
    df_defensive_actions = df.loc[defensive_actions_ids, ["index", "x", "y", "team_name", "player_id", "type_display_name", "outcome_type_display_name"]]

    return df_defensive_actions

defensive_actions_df = get_defensive_action_df(df)
players_df = df[['player_id', 'name', 'shirt_no', 'position', 'is_first_eleven']]

def get_da_count_df(defensive_actions_df, players_df, team_info):

    home_team = team_info['home_team']
    away_team = team_info['away_team']

    team_names = [home_team, away_team]
    # Filter defensive actions for the teams in the list
    defensive_actions_df = defensive_actions_df[defensive_actions_df["team_name"].isin(team_names)]
    # add column with first eleven players only
    defensive_actions_df = defensive_actions_df.merge(players_df[["player_id", "is_first_eleven"]], on='player_id', how='left')
    # calculate mean positions for players
    average_locs_and_count_df = (defensive_actions_df.groupby('player_id').agg({'x': ['median'], 'y': ['median', 'count']}))
    average_locs_and_count_df.columns = ['x', 'y', 'count']
    average_locs_and_count_df = average_locs_and_count_df.reset_index()
    average_locs_and_count_df = average_locs_and_count_df.merge(players_df[['player_id', 'name', 'shirt_no', 'position', 'is_first_eleven']], on='player_id', how='left')
    average_locs_and_count_df = average_locs_and_count_df.set_index('player_id')

    return  average_locs_and_count_df


defensive_home_average_locs_and_count_df = get_da_count_df(home_team, defensive_actions_df, players_df)
defensive_away_average_locs_and_count_df = get_da_count_df(away_team, defensive_actions_df, players_df)
defensive_home_average_locs_and_count_df = defensive_home_average_locs_and_count_df[defensive_home_average_locs_and_count_df['position'] != 'GK']
defensive_away_average_locs_and_count_df = defensive_away_average_locs_and_count_df[defensive_away_average_locs_and_count_df['position'] != 'GK']

def defensive_block(ax, average_locs_and_count_df, team_name, col):
    defensive_actions_team_df = defensive_actions_df[defensive_actions_df["team_name"] == team_name]
    pitch = Pitch(pitch_type='uefa', pitch_color=bg, line_color=line_color, linewidth=2, line_zorder=2, corner_arcs=True)
    pitch.draw(ax=ax)
    ax.set_facecolor(bg)
    ax.set_xlim(-0.5, 105.5)
    ax.set_ylim(-0.5, 68.5)

    # using variable marker size for each player according to their defensive engagements
    MAX_MARKER_SIZE = 3500
    average_locs_and_count_df['marker_size'] = (average_locs_and_count_df['count']/ average_locs_and_count_df['count'].max() * MAX_MARKER_SIZE)
    # plotting the heatmap of the team defensive actions
    color = np.array(to_rgba(col))
    flamingo_cmap = LinearSegmentedColormap.from_list("Flamingo - 100 colors", [bg, col], N=500)
    kde = pitch.kdeplot(defensive_actions_team_df.x, defensive_actions_team_df.y, ax=ax, fill=True, levels=5000, thresh=0.02, cut=4, cmap=flamingo_cmap)

    # using different node marker for starting and substitute players
    average_locs_and_count_df = average_locs_and_count_df.reset_index(drop=True)
    for index, row in average_locs_and_count_df.iterrows():
        if row['is_first_eleven'] == True:
            da_nodes = pitch.scatter(row['x'], row['y'], s=row['marker_size']+100, marker='o', color=bg, edgecolor=line_color, linewidth=1, 
                                 alpha=1, zorder=3, ax=ax)
        else:
            da_nodes = pitch.scatter(row['x'], row['y'], s=row['marker_size']+100, marker='s', color=bg, edgecolor=line_color, linewidth=1, 
                                     alpha=1, zorder=3, ax=ax)
    # plotting very tiny scatterings for the defensive actions
    da_scatter = pitch.scatter(defensive_actions_team_df.x, defensive_actions_team_df.y, s=10, marker='x', color='yellow', alpha=0.2, ax=ax)

    # Plotting the shirt no. of each player
    # for index, row in average_locs_and_count_df.iterrows():
    #     player_initials = row["shirt_no"]
    #     pitch.annotate(player_initials, xy=(row.x, row.y), c=line_color, ha='center', va='center', size=(14), ax=ax)

    # Plotting a vertical line to show the median vertical position of all defensive actions, which is called Defensive Actions Height
    dah = round(average_locs_and_count_df['x'].mean(), 2)
    dah_show = round((dah*1.05), 2)
    ax.axvline(x=dah, color='gray', linestyle='--', alpha=0.75, linewidth=2)

    # Defense line Defensive Actions Height
    center_backs_height = average_locs_and_count_df[average_locs_and_count_df['position']=='DC']
    def_line_h = round(center_backs_height['x'].median(), 2)
    ax.axvline(x=def_line_h, color='gray', linestyle='dotted', alpha=0.5, linewidth=2)
    # Forward line Defensive Actions Height
    Forwards_height = average_locs_and_count_df[average_locs_and_count_df['is_first_eleven']==1]
    Forwards_height = Forwards_height.sort_values(by='x', ascending=False)
    Forwards_height = Forwards_height.head(2)
    fwd_line_h = round(Forwards_height['x'].mean(), 2)
    ax.axvline(x=fwd_line_h, color='gray', linestyle='dotted', alpha=0.5, linewidth=2)

    # Getting the compactness value 
    compactness = round((1 - ((fwd_line_h - def_line_h) / 105)) * 100, 2)

    # Headings and other texts
    if team_name == away_team:
        # inverting the axis for away team
        ax.invert_xaxis()
        ax.invert_yaxis()
        ax.text(dah-1, 73, f"{dah_show}m", fontsize=15, color=line_color, ha='left', va='center')
    else:
        ax.text(dah-1, -5, f"{dah_show}m", fontsize=15, color=line_color, ha='right', va='center')

    # Headlines and other texts
    if team_name == home_team:
        ax.text(105, -5, f'Compact:{compactness}%', fontsize=15, color=line_color, ha='right', va='center')
        ax.text(2,66, "circle = starter\nbox = sub", color='gray', size=12, ha='left', va='top')
        ax.set_title(f"{home_team}\nDefensive Block", color=line_color, fontsize=25, fontweight='bold')
    else:
        ax.text(105, 73, f'Compact:{compactness}%', fontsize=15, color=line_color, ha='left', va='center')
        ax.text(2,2, "circle = starter\nbox = sub", color='gray', size=12, ha='right', va='top')
        ax.set_title(f"{away_team}\nDefensive Block", color=line_color, fontsize=25, fontweight='bold')

    return {
        'Team_Name': team_name,
        'Average_Defensive_Action_Height': dah,
        'Forward_Line_Pressing_Height': fwd_line_h
    }
