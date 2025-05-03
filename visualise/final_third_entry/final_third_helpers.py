import matplotlib.pyplot as plt
from matplotlib import patheffects
from lib.player_plot import player_plot

MAX_MARKER_SIZE = 3500

def analyse_final_third_entries(df_pass, df_carry):

    df_carry_team_groupby = df_carry.groupby(['player_name', 'type_display_name', 'outcome_type_display_name']).size().reset_index(name='count')
    grouped_carry = df_carry_team_groupby.sort_values(by='count', ascending=False).head(3).reset_index(drop=True)

    df_pass_team_groupby = df_pass.groupby(['player_name', 'type_display_name', 'outcome_type_display_name']).size().reset_index(name='count')
    grouped_pass = df_pass_team_groupby.sort_values(by='count', ascending=False).head(3).reset_index(drop=True)

    return grouped_carry, grouped_pass

def plot_stats(ax1, df_pass, df_carry, grouped_pass, grouped_carry, visualisation_params):
    bg = visualisation_params['bg']
    bodyfont = visualisation_params['bodyfont']
    line_color = visualisation_params['line_color']
    text_color = visualisation_params['text_color']
    carry_color = visualisation_params['carry_color']
    pass_color = visualisation_params['pass_color']

    vertical_shift = -0.9*3
    vertical_shift1 = -0.05*3.5
    positions = {
        "PASSES INTO FINAL THIRD": (0.72, 0.46 + vertical_shift1),
        "CARRIES INTO FINAL THIRD": (0.72, 0.65 + vertical_shift1)
    }

    y_lines = [11.5+vertical_shift, 8.5+vertical_shift]
    y_dots = [9.3+vertical_shift, 6.3+vertical_shift]
    text_y_positions = [11.8+vertical_shift, 8.8+vertical_shift]
    
    ax1.axis('off')
    ax1.set_ylim(0, 13)
    ax1.set_xlim(0, 3)

    # Adding labels
    for label, y in zip(positions.keys(), text_y_positions):
        ax1.text(x=0.1, y=y, s=label, size=15, va='center', ha='left', color='w')
        ax1.text(x=2.9, y=9.2, s=f"{len(df_pass)}", size=18, va='center', ha='right', color=bg, weight='bold',
                   bbox=dict(facecolor=pass_color, edgecolor='none', boxstyle='round,pad=0.1'))
        ax1.text(x=2.9, y=6.2, s=f"{len(df_carry)}", size=18, va='center', ha='right', color=bg, weight='bold',
                   bbox=dict(facecolor=carry_color, edgecolor='none', boxstyle='round,pad=0.1'))


    # Adding horizontal lines
    for y in y_lines:
        ax1.plot([0, 3], [y, y], lw='1.5', color='w')

    # Adding dotted lines
    for y in y_dots:
        ax1.plot([0, 3], [y, y], lw='0.5', color=line_color, linestyle='dotted')

    # Define a helper function for plotting players
    def plot_players(grouped_data, position_prefix):
        # Find the key that matches the prefix (e.g., "PASSES INTO FINAL THIRD")
        position_key = next(key for key in positions if key.startswith(position_prefix))
        
        for i in range(min(len(grouped_data), 3)):  # Max 3 players per category
            pos = positions[position_key]
            spacing = 0.12  # Adjust this value for more or less space
            player_ax = plt.axes([pos[0] + i * spacing, pos[1], 0.1, 0.15])

            full_name = grouped_data.iloc[i]['player_name']
            
            # Use 'Gabriel' for Gabriel Magalhães, otherwise use the surname
            if 'Gabriel' in full_name:
                display_name = 'Gabriel'
            else:
                display_name = full_name.split()[-1]  # Get the surname

            folder_path = '../players/'

            player_plot(player_ax, display_name, folder_path, line_color, text_color, bodyfont, bg)
            count_to_display = str(grouped_data.iloc[i]['count'])
            player_ax.text(4.8, 2.4, count_to_display, size=22, va='center', ha='left',
                        color=text_color, weight='black',
                        path_effects=[patheffects.withStroke(linewidth=6, foreground=bg)])
            player_ax.axis('off')

    # Update the plot_players function calls:
    plot_players(grouped_pass, "PASSES INTO FINAL THIRD")
    plot_players(grouped_carry, "CARRIES INTO FINAL THIRD")