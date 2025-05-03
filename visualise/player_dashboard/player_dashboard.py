from lib.cumulative_match_mins import cumulative_match_mins
from lib.insert_ball_carries import insert_ball_carries
import numpy as np
import pandas as pd
import os

def create(match_events):
    match_events = cumulative_match_mins(match_events)

    match_events = insert_ball_carries(match_events, min_carry_length=3, max_carry_length=60, min_carry_duration=1, max_carry_duration=10)
    match_events = match_events.reset_index(drop=True)
    match_events['index'] = range(1, len(match_events) + 1)
    match_events = match_events[['index'] + [col for col in match_events.columns if col != 'index']]


    match_events = match_events.fillna({'end_x': 0, 'end_y': 0, 'uefa_end_x': 0, 'uefa_end_y':0})

    df_xT = match_events.copy()


    df_xT['qualifiers'] = df_xT['qualifiers'].astype(str)
    df_xT = df_xT[(~df_xT['qualifiers'].str.contains('Corner'))]
    df_xT = df_xT[(df_xT['type_display_name'].isin(['Pass', 'Carry'])) & (df_xT['outcome_type_display_name'] == 'Successful')]
    
    ### add expected threat
    xT = np.array([[0.00638303, 0.00779616, 0.00844854, 0.00977659, 0.01126267,
                    0.01248344, 0.01473596, 0.0174506, 0.02122129, 0.02756312,
                    0.03485072, 0.0379259],
                    [0.00750072, 0.00878589, 0.00942382, 0.0105949, 0.01214719,
                    0.0138454, 0.01611813, 0.01870347, 0.02401521, 0.02953272,
                    0.04066992, 0.04647721],
                    [0.0088799, 0.00977745, 0.01001304, 0.01110462, 0.01269174,
                    0.01429128, 0.01685596, 0.01935132, 0.0241224, 0.02855202,
                    0.05491138, 0.06442595],
                    [0.00941056, 0.01082722, 0.01016549, 0.01132376, 0.01262646,
                    0.01484598, 0.01689528, 0.0199707, 0.02385149, 0.03511326,
                    0.10805102, 0.25745362],
                    [0.00941056, 0.01082722, 0.01016549, 0.01132376, 0.01262646,
                    0.01484598, 0.01689528, 0.0199707, 0.02385149, 0.03511326,
                    0.10805102, 0.25745362],
                    [0.0088799, 0.00977745, 0.01001304, 0.01110462, 0.01269174,
                    0.01429128, 0.01685596, 0.01935132, 0.0241224, 0.02855202,
                    0.05491138, 0.06442595],
                    [0.00750072, 0.00878589, 0.00942382, 0.0105949, 0.01214719,
                    0.0138454, 0.01611813, 0.01870347, 0.02401521, 0.02953272,
                    0.04066992, 0.04647721],
                    [0.00638303, 0.00779616, 0.00844854, 0.00977659, 0.01126267,
                    0.01248344, 0.01473596, 0.0174506, 0.02122129, 0.02756312,
                    0.03485072, 0.0379259]])

    xT_rows, xT_cols = xT.shape

    df_xT['x1_bin_xT'] = pd.cut(df_xT['uefa_x'], bins = xT_cols, labels=False)
    df_xT['y1_bin_xT'] = pd.cut(df_xT['uefa_y'], bins = xT_rows, labels=False)
    df_xT['x2_bin_xT'] = pd.cut(df_xT['uefa_end_x'], bins = xT_cols, labels=False)
    df_xT['y2_bin_xT'] = pd.cut(df_xT['uefa_end_y'], bins = xT_rows, labels=False)
    

    df_xT['start_zone_value_xT'] = df_xT[['x1_bin_xT', 'y1_bin_xT']].apply(
    lambda x: xT[int(x[1])] [int(x[0])] if pd.notna(x[1]) and pd.notna(x[0]) else np.nan, 
    axis=1)
    df_xT['end_zone_value_xT'] = df_xT[['x2_bin_xT', 'y2_bin_xT']].apply(lambda x: xT[x[1]][x[0]], axis=1)

    df_xT['xT'] = df_xT['end_zone_value_xT'] - df_xT['start_zone_value_xT']

    columns_to_keep = ['index', 'xT']
    df_xT = df_xT.filter(items=columns_to_keep)
    df = match_events.merge(df_xT, on='index', how='left')
    
    df['start_dist'] = np.sqrt(np.square(105 - df.uefa_x) + np.square(34 - df.uefa_y))
    df['end_dist'] = np.sqrt(np.square(105 - df.uefa_end_x) + np.square(34 - df.uefa_end_y))
    df['pass_length'] = np.sqrt(np.square(df.uefa_x - df.uefa_end_x) + np.square(df.uefa_y - df.uefa_end_y))
    df['diffdist'] = df['start_dist'] - df['end_dist']

    # Pitch Masks
    # Defining masks based on the pitch zones and distances
    final_third_mask = (df.uefa_end_x > 70) & (df.uefa_x <= 70)  # Final third of the pitch
    own_half_mask = (df.uefa_x < 52.5)  # Own half
    opposition_half_mask = (df.uefa_x > 52.5)  # Opposition half
    penalty_area_end_mask = (df.uefa_end_x > 88.5) & (np.abs(df.uefa_end_y - 34) < 20.16)  # End of penalty area
    penalty_area_start_mask = (df.uefa_x > 88.5) & (np.abs(df.uefa_y - 34) < 20.16)  # Start of penalty area
    outside_penalty_area_mask = ~penalty_area_start_mask  # Outside the penalty area
    dist_mask = (df['start_dist'] - df['end_dist']) / df['start_dist'] > 0.25  # Significant distance change
    box_mask = (df.x > 102) & (np.abs(df.y - 40) < 22)  # In the box

    # Pass Masks
    # Filtering various types of passes
    pass_mask = df.type_display_name == 'Pass'  # General pass
    success_mask = df.outcome_type_display_name == 'Successful'  # Successful passes
    open_play_mask = df.is_open_play == True  # Open play passes
    short_pass_mask = (df.pass_length >= 4.572) & (df.pass_length < 13.716)  # Short passes
    medium_pass_mask = (df.pass_length >= 13.716) & (df.pass_length < 27.432)  # Medium passes
    long_pass_mask = df.pass_length >= 27.432  # Long passes
    through_ball_mask = df.is_through_ball == True  # Through balls
    switch_mask = (df.type_display_name == 'Pass') & ((df.end_y - df.y) ** 2 >= 36.57 ** 2)  # Switches
    cross_mask = df.is_cross == True  # Crosses
    prog_mask = dist_mask | box_mask  # Progressive passes
    key_pass_mask = df.is_key_pass == True  # Key passes
    assist_mask = (df.is_key_pass == True) & (df.type_display_name == 'Goal')  # Assists
    carry_mask = df.type_display_name == 'Carry'  # Carrying the ball
    take_on_mask = df.type_display_name == 'TakeOn'  # Take-ons

    # Defensive Masks
    # Filtering defensive actions
    foul_mask = df.type_display_name == 'Foul'  # Fouls
    aerial_mask = df.type_display_name == 'Aerial'  # Aerial duels
    clearance_mask = df.type_display_name == 'Clearance'  # Clearances
    interception_mask = df.type_display_name == 'Interception'  # Interceptions
    tackle_mask = df.type_display_name == 'Tackle'  # Tackles
    block_mask = df.type_display_name == 'BlockedPass'  # Blocked passes
    challenge_mask = df.type_display_name == 'Challenge'  # Challenges

    df['Passes'] = np.where(pass_mask & open_play_mask,1,0)
    df['Successful Passes'] = np.where(pass_mask & open_play_mask & success_mask,1,0)

    df['Short Passes'] = np.where(pass_mask & open_play_mask & short_pass_mask,1,0)
    df['Successful Short Passes'] = np.where((df['Short Passes']==1) & success_mask,1,0)

    df['Medium Passes'] = np.where(pass_mask & open_play_mask & medium_pass_mask,1,0)
    df['Successful Medium Passes'] = np.where((df['Medium Passes']==1) & success_mask,1,0)

    df['Long Passes'] = np.where(pass_mask & open_play_mask & long_pass_mask,1,0)
    df['Successful Long Passes'] = np.where((df['Long Passes']==1) & success_mask,1,0)

    df['Final Third Passes'] = np.where(pass_mask & final_third_mask & open_play_mask,1,0)
    df['Successful Final Third Passes'] = np.where((df['Final Third Passes']==1) & success_mask,1,0)

    df['Penalty Area Passes'] = np.where(pass_mask & penalty_area_end_mask & open_play_mask,1,0)
    df['Successful Penalty Area Passes'] = np.where((df['Penalty Area Passes']==1) & success_mask,1,0)

    df['Passes Own Half'] = np.where(open_play_mask & own_half_mask,1,0)
    df['Successful Passes Own Half'] = np.where((df['Passes Own Half']==1) & success_mask,1,0)

    df['Passes Opposition Half'] = np.where(open_play_mask & opposition_half_mask,1,0)
    df['Successful Passes Opposition Half'] = np.where((df['Passes Opposition Half']==1) & success_mask,1,0)

    df['Passes into Penalty Area'] = np.where(open_play_mask & outside_penalty_area_mask & penalty_area_end_mask,1,0)
    df['Successful Passes into Penalty Area'] = np.where(open_play_mask & outside_penalty_area_mask & penalty_area_end_mask & open_play_mask & success_mask,1,0)

    df['Throughballs'] = np.where(through_ball_mask,1,0)
    df['Successful Throughballs'] = np.where(through_ball_mask & success_mask,1,0)

    df['Switches'] = np.where(switch_mask & open_play_mask ,1,0)
    df['Successful Switches'] = np.where(switch_mask & open_play_mask & success_mask,1,0)

    df['Crosses'] = np.where(cross_mask & open_play_mask,1,0)
    df['Successful Crosses'] = np.where(cross_mask & open_play_mask & success_mask,1,0)

    df['Penalty Area Crosses'] = np.where(cross_mask & penalty_area_end_mask & open_play_mask,1,0)
    df['Successful Penalty Area Crosses'] = np.where(cross_mask & penalty_area_end_mask & open_play_mask & success_mask,
                                                    1,0)
    df['Progressive Passes'] = np.where(pass_mask & prog_mask & open_play_mask,1,0)
    df['Successful Progressive Passes'] = np.where(pass_mask & prog_mask & open_play_mask & success_mask,1,0)
    df['Progressive Pass Distance'] = np.where(pass_mask & (df.diffdist > 0), df.diffdist, 0)

    df['Key Passes'] = np.where(key_pass_mask,1,0)
    df['Assists'] = np.where(assist_mask, 1,0)
    df['Through Balls'] = np.where(through_ball_mask, 1,0)

    df['Carries'] = np.where(carry_mask,1,0)
    df['Final Third Carries'] = np.where(carry_mask & final_third_mask,1,0)
    df['Progressive Carries'] = np.where(carry_mask & prog_mask,1,0)
    df['Progressive Carry Distance'] = np.where(carry_mask & (df.diffdist > 0), df.diffdist, 0)

    df['Take Ons'] = np.where(take_on_mask,1,0)
    df['Successful Take Ons'] = np.where(take_on_mask & success_mask,1,0)

    df['Fouls'] = np.where(foul_mask,1,0)
    df['Clearances'] = np.where(clearance_mask & success_mask,1,0)
    df['Interceptions'] = np.where(interception_mask & success_mask,1,0)
    df['Tackles'] = np.where(tackle_mask & success_mask, 1,0)
    df['Blocks'] = np.where(block_mask & success_mask,1,0)
    df['Challenges'] = np.where(challenge_mask,1,0)
    df['BallRecovery'] = np.where(challenge_mask,1,0)


    aggdict = {'team_name': 'first', 
            'Passes':'sum','Successful Passes':'sum','Short Passes':'sum', 
            'Successful Short Passes':'sum','Medium Passes':'sum', 
            'Successful Medium Passes':'sum','Long Passes':'sum', 
            'Successful Long Passes':'sum','Final Third Passes':'sum',
            'Successful Final Third Passes':'sum','Penalty Area Passes':'sum',
            'Successful Penalty Area Passes':'sum',
            'Passes into Penalty Area':'sum','Successful Passes into Penalty Area':'sum',
            'Passes Own Half':'sum', 'Successful Passes Own Half':'sum',
            'Passes Opposition Half':'sum', 'Successful Passes Opposition Half':'sum',
            'Throughballs':'sum','Successful Throughballs':'sum','Switches':'sum',
            'Successful Switches':'sum', 'Key Passes':'sum','Through Balls':'sum','Assists':'sum',
            'Crosses':'sum', 'Successful Crosses':'sum','Penalty Area Crosses':'sum',
            'Successful Penalty Area Crosses':'sum','Progressive Passes':'sum',
            'Successful Progressive Passes':'sum','pass_length':'sum',
            'Progressive Pass Distance':'sum','Carries':'sum',
            'Final Third Carries':'sum','Progressive Carries':'sum',
            'Progressive Carry Distance':'sum','Take Ons':'sum', 'Successful Take Ons':'sum',
            'Fouls':'sum','Clearances':'sum', 'Interceptions':'sum','Tackles':'sum',
            'Blocks':'sum','Challenges':'sum','BallRecovery':'sum','xT':'sum'
            }

    groupedstats = df.groupby('player_name').agg(aggdict).reset_index()
    groupedstats.rename(columns={'pass_length': 'Total Pass Length'}, inplace=True)
    groupedstats = groupedstats.sort_values(by=['player_name', 'team_name'], ascending=[False, False]).reset_index(drop=True)

    xtreceiver = df[df['receiver'] != ''].groupby('receiver').agg({'xT': 'sum'}).reset_index()
    xtreceiver.rename(columns={'xT': 'xT Received', 'receiver': 'player_name'}, inplace=True)

    final_df = pd.merge(groupedstats, xtreceiver, on='player_name', how='inner')
    final_df['Defensive Actions'] = final_df['Fouls']+final_df['Clearances']+final_df['Interceptions']+final_df['Tackles']+final_df['Blocks']+final_df['Challenges']+final_df['BallRecovery']

    player = player_name
    name_parts = player.split()

    if len(name_parts) >= 2:
        surname = name_parts[-1].lower()
    else:
        surname = full_name

    receiver_df = df[(df['receiver'] == player)]
    df = df[(df['player_name'] == player)]
    pass_df = df.query("(type_display_name=='Pass')")

    # Create a boolean condition for fouls
    foul_cond = (df.type_display_name == 'Foul') & (df.outcome_type_display_name == 'Unsuccessful')

    # Filter for defensive actions
    defense_df = df.query("(type_display_name in ['Aerial', 'Clearance', 'Interception', \
                        'Tackle', 'BlockedPass', 'Challenge', 'BallRecovery'])")

    # Use pd.concat instead of append
    defense_df = pd.concat([defense_df, df[foul_cond]], ignore_index=True)

    # Add a column indicating defensive actions
    defense_df['defensive'] = 1

    # Adjust the defensive flag based on qualifiers
    for i in range(len(defense_df)):
        if defense_df.loc[i, 'type_display_name'] in ['Aerial', 'Challenge']:
            qualifiers = defense_df.qualifiers[i]
            if '286' in qualifiers:
                defense_df.loc[i, 'defensive'] = 0

    # Filter out non-defensive actions
    defense_df = defense_df[defense_df.defensive == 1]

    takeon_df = df[(df['type_display_name'] == 'TakeOn') & (df['outcome_type_display_name'] == 'Successful')]

    # Define the list of columns you want to calculate ranks for
    columns_to_rank = [
        'Passes',
        'Successful Passes',
        'xT',
        'xT Received',
        'Successful Passes into Penalty Area',
        'Successful Progressive Passes',
        'Progressive Carries',
        'Switches',
        'Successful Take Ons',
        'Defensive Actions'
    ]

    import numpy as np

    # Columns to exclude from processing
    exclude_columns = ['name_team', 'home_team', 'away_team']

    # Iterate through all columns in the DataFrame
    for column in final_df.columns:
        if column not in exclude_columns:
            # Calculate ranks for the current column
            final_df[column + '_rank'] = final_df[column].rank(ascending=False, method='min')
            
            # Replace ranks with the length of final_df for rows with original values equal to 0
            zero_rows = final_df[final_df[column] == 0].index
            final_df.loc[zero_rows, column + '_rank'] = len(final_df)

    circleColor = '#1b98e6'


        # Plot pitch
    pitch = VerticalPitch(pitch_type='uefa', pitch_color=bg, half=False, linewidth=3, corner_arcs=True,
                        positional=True, positional_color=line_color, positional_linestyle='dotted',
                        shade_middle=True, shade_color='#f2f2f2',
                        stripe=False, line_zorder=2, line_color=pitch_line, goal_type='box')

    pitch2 = VerticalPitch(pitch_type='uefa', pitch_color=bg, half=False, linewidth=3, corner_arcs=True,
                        line_zorder=4, line_color=pitch_line, goal_type='box')

    pitch3 = VerticalPitch(pitch_type='uefa', pitch_color=bg, half=False, linewidth=3, corner_arcs=True,
                        stripe=False, line_zorder=2, line_color=pitch_line, goal_type='box')

    FIGWIDTH, FIGHEIGHT = 16, 9
    PITCH_WIDTH = 0.58
    PITCH_HEIGHT = PITCH_WIDTH / pitch2.ax_aspect * FIGWIDTH / FIGHEIGHT

    KEY_WIDTH = 0.27
    KEY_HEIGHT = KEY_WIDTH / pitch2.ax_aspect * FIGWIDTH / FIGHEIGHT

    fig = plt.figure(figsize=(16, 9), facecolor=bg)

    ax = fig.add_axes((0.05, 0, 1.65, 1))
    ax.axis('off')

    # Pitch 
    ax_pitch = fig.add_axes((0.05, 0.02, PITCH_WIDTH, PITCH_HEIGHT))
    pitch.draw(ax=ax_pitch)


    ## passes and carries
    for outcome, color, zorder_base in [('Unsuccessful', '#c0c1c0', 1), ('Successful', pass_color, 2)]:
        passes = pass_df[pass_df.outcome_type_display_name == outcome]
        angle, distance = pitch.calculate_angle_and_distance(
            passes.uefa_x, passes.uefa_y, passes.uefa_end_x, passes.uefa_end_y, standardized=False, degrees=True
        )
        
        zorder = zorder_base * 10  # Adjust this scaling factor as needed
        
        pitch.lines(passes.uefa_x, passes.uefa_y, passes.uefa_end_x, passes.uefa_end_y,
                    comet=True, color=color, zorder=zorder + 3, transparent=True, lw=6, alpha_start=0, alpha_end=0.5, ax=ax_pitch)
        
        pitch.scatter(passes.uefa_end_x, passes.uefa_end_y, rotation_degrees=angle, c=color, zorder=zorder + 6,
                    s=700, ax=ax_pitch, marker=arrowhead_marker)
        
    ax_pitch.text(34,110, "open-play passes", color='#5e605f', size=20, va='center',ha='center')
        
    ax_pitch.text(10,-4.5, "receiver location", color='#5e605f', size=20, va='center',ha='right')
    ax_pitch.text(40,-4.5, player+" location", color='#5e605f', size=20, va='center',ha='right')


    ax_arrow = fig.add_axes([0.3, -0.01, 0.09, 0.05])
    ax_arrow.axis('off')

    # Add fancy arrow
    style = "fancy,tail_width=0.4,head_width=15,head_length=15"
    kw = dict(arrowstyle=style, color=bg, ec='#5e605f')

    a = patches.FancyArrowPatch((0, 0.4), (1, 0.4),**kw, zorder=20, lw=2)

    ax_arrow.add_patch(a)

    ## Key1 receiver heatmap
    ax_key1 = fig.add_axes((0.65, 0.80, KEY_WIDTH, KEY_HEIGHT))
    pitch2.draw(ax=ax_key1)


    # pitch2
    #kdeplot(receiver_df.end_x, receiver_df.end_y, ax=ax_key1, fill=True, levels=100, shade_lowest=False, cmap=cmap)
    ax_key1.text(34,-6, "open-play passes received", color='#5e605f', size=20, va='center',ha='center')


    bin_statistic = pitch.bin_statistic_positional(receiver_df.x, receiver_df.y, statistic='count',
                                                positional='full', normalize=True)

    pitch.heatmap_positional(bin_statistic, ax=ax_key1, cmap=cmap, edgecolors=None,alpha=0.8)
    labels = pitch.label_heatmap(bin_statistic, color='#5e605f', fontsize=21, weight='black',
                                ax=ax_key1, ha='center', va='center',
                                str_format='{:.0%}'
                                , path_effects=[path_effects.withStroke(linewidth=4,foreground='w')])


    # Key2 defensive actions
    ax_key2 = fig.add_axes((0.65, 0.05, KEY_WIDTH, KEY_HEIGHT))
    pitch3.draw(ax=ax_key2)
    pitch3.scatter(defense_df.uefa_x, defense_df.uefa_y, ax=ax_key2, color=bg, ec=pass_color, s=300, lw=4, alpha=0.85, zorder=3)
    pitch3.scatter(takeon_df.uefa_x, takeon_df.uefa_y, ax=ax_key2, color=bg, marker='*', ec=pass_color, s=600, lw=3, alpha=0.85, zorder=3)
    ax_key2.text(34,-6, "defensive actions", color='#5e605f', size=20, va='center',ha='center')
    ax_key2.text(34,-12, "successful dribbles", color='#5e605f', size=20, va='center',ha='center')

    ax6 = fig.add_axes([0.85, -0.023, 0.05, 0.05])
    ax6.scatter(1,1,marker='*', s=400, c=bg,ec='#5e605f',lw=2)
    ax6.axis('off')
    ax7 = fig.add_axes([0.85, 0.015, 0.05, 0.05])
    ax7.scatter(1,1,marker='o', s=200, c=bg,ec='#5e605f',lw=2)
    ax7.axis('off')


    ax1 = fig.add_axes((0.96, 0.1, 0.4, 1.4))
    # Get the data for the chosen team
    playerdf = final_df[final_df['player_name'] == player]

    # Define a list of metrics to display
    metrics = ['Passes', 'Successful Passes', 'Key Passes', 'Progressive Passes', 'Successful Take Ons', 'Carries', 'xT', 'Defensive Actions']

    # Iterate through the metrics and plot them
    for i, metric in enumerate(metrics):
        rank_col = metric + '_rank'
        values = playerdf[metric]  # Get the values for the current metric
        
        
        # Map rank values to colors using the colormap
        colors = cmap2(playerdf[rank_col] / 20.0)  # Divide by 20 to normalize ranks to [0, 1]
        
        # Scatter plot for the rank with colormap-based edgecolor
        ax1.scatter(playerdf[rank_col], [i] * len(playerdf),
    #                 s=2900, c='w', edgecolor=colors, linewidth=10, zorder=3)
                    s=2100, c='w', edgecolor=circleColor, linewidth=10, zorder=3)
        for j, value in enumerate(values):
            # Set the number of decimal places based on the metric
            if metric in ['xt_value', 'xt_value_receiver','Expected Goals']:
                decimal_places = 2
            else:
                decimal_places = 0

            ax1.text(playerdf[rank_col].values[j], i+0.4, f'{value:.{decimal_places}f}',ha='center',va='center',
                    size=25,
                    bbox=dict(boxstyle='round,pad=0.3', edgecolor='grey', facecolor=bg, alpha=0.5,
                            path_effects=[path_effects.withStroke(linewidth=1,foreground=bg)]))       
            
        
        # Draw a horizontal line for each metric at its respective y-coordinate (i)
        ax1.hlines(y=i, xmin=-5, xmax=len(final_df)+2, colors='#5e605f', lw=8, alpha=1, zorder=2)



    ax1.yaxis.tick_right()

    # Customize the plot
    ax1.set_yticks(np.arange(len(metrics)))
    ax1.set_yticklabels(['ATTEMPTED PASSES', 'SUCCESSFUL PASSES', 'KEY PASSES', 'PROGRESSIVE PASSES', 'SUCCESSFUL DRIBBLES', 'CARRIES', 'EXPECTED THREAT (xT)', 'DEFENSIVE ACTIONS'],
                        fontsize=34, weight='bold', color='#5e605f',position=(1.01, 0))

    x_ticks = [5, 10, 15, 20, 25, 30]
    ax1.set_xticks(x_ticks)
    ax1.grid(axis='x', linestyle='--', alpha=0.5,zorder=0)


    ax1.tick_params(axis='y', which='both', length=0)
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)
    ax1.set_facecolor(bg)
    ax1.set_xlim(-1, len(final_df)+2.5)
    ax1.invert_yaxis()
    ax1.invert_xaxis()



    for spine in ax1.spines.values():
        spine.set_visible(False)

        
    # Add the additional text to the figure
    fig.text(0.6, 1.7, player.upper(),
            size=60, c='k', ha='left', va='center',
            fontweight='black', zorder=2)

    fig.text(0.9, 1.75, 'w'.upper(),
            size=60, c=bg, fontfamily=titlefont, ha='center', va='center',
            fontweight='black', zorder=-1)

    fig.text(0.6, 1.62, match_comp+" • "+match_date+" • "+home_team+" "+match_score+" "+awayTeam,
            size=30, c='grey', fontfamily=bodyfont, ha='left', va='center')


    fig.text(1.69, -0.01, '@ j o n o l l i n g t o n',
            ha='right', fontsize=30, color=line_color, family = sigfont)


    ax3 = fig.add_axes([0.48, 1.58, 0.11, 0.2])
    playerPlot(ax=ax3, playername=playerP)
    ax3.axis('off')

    # Save the plot
    fig.set_facecolor(bg)
    plt.savefig("../../png/output/ØDash.jpeg", bbox_inches='tight', format='jpeg');

