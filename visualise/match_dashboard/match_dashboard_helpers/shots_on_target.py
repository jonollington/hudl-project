import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects

def shots_on_target(ax, stats_df, bg, home_color, away_color, titlefont):

        # Extract data from home_data and away_data
        home_shots_on_target = stats_df['total_shots_on_target'].iloc[0]
        home_shots_off_target = stats_df['total_shots_on_target'].iloc[0]
        away_shots_on_target = stats_df['total_shots_on_target'].iloc[1]
        away_shots_off_target = stats_df['total_shots_on_target'].iloc[1]

        # Plot shapes
        ax.plot([1, 1], [0, 2], color='w', lw=7,
                path_effects=[path_effects.withStroke(linewidth=10, foreground=bg)])
        ax.plot([1, 1], [0, 2], color='w', lw=7, zorder=4)
        ax.plot([1, 9], [2, 2], color='w', lw=7, zorder=3,
                path_effects=[path_effects.withStroke(linewidth=10, foreground=bg)])
        ax.plot([9, 9], [2, 0], color='w', lw=7, zorder=2,
                path_effects=[path_effects.withStroke(linewidth=10, foreground=bg)])
        ax.plot([9, 9], [2, 0], color='w', lw=7, zorder=3)

        # Total width for each team's section (arbitrary width for example, adjust as needed)
        total_width = 10
        rect_height = 3

        # Total shots off target
        total_shots_off_target = home_shots_off_target + away_shots_off_target
        total_shots_on_target = home_shots_on_target + away_shots_on_target

        # Calculate the widths of the rectangles for each team
        home_width = (home_shots_off_target / total_shots_off_target) * total_width
        away_width = (away_shots_off_target / total_shots_off_target) * total_width
        home_width_on_target = (home_shots_on_target / total_shots_on_target) * total_width
        away_width_on_target = (away_shots_on_target / total_shots_on_target) * total_width

        # Plot home shots off target rectangle
        home_rect = plt.Rectangle((0, 0), home_width, rect_height, color=home_color)
        ax.add_patch(home_rect)

        # Plot away shots off target rectangle
        away_rect = plt.Rectangle((home_width, 0), away_width, rect_height, color=away_color)
        ax.add_patch(away_rect)        

        # Plot home shots on target rectangle
        home_rect_on_target = plt.Rectangle((0, 0), home_width_on_target, 2, color=home_color, zorder=2)
        ax.add_patch(home_rect_on_target)

        # Plot away shots on target rectangle
        away_rect_on_target = plt.Rectangle((home_width_on_target, 0), away_width_on_target, 2, color=away_color, zorder=2)
        ax.add_patch(away_rect_on_target)
        
        ax.set_xlim(0, 10)
        ax.set_ylim(0, 3)
        
        # Add text
        ax.text(5, 2.52, "Shots off Target".upper(), fontsize=20, color='w', weight='bold', 
                va='center', ha='center', family=titlefont,
                path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
        ax.text(5, 1, "Shots on\nTarget".upper(), fontsize=20, color='w', weight='bold', 
                va='center', ha='center', family=titlefont,
                path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
        
        ax.text(1, 2.5, home_shots_off_target, fontsize=40, fontfamily=titlefont, color='w', weight='bold', 
                va='center', ha='right', family=titlefont,
                path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
        
        ax.text(9, 2.5, away_shots_off_target, fontsize=40, fontfamily=titlefont, color='w', weight='bold', 
                va='center', ha='left', family=titlefont,
                path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
        
        ax.text(2.2, 1, home_shots_on_target, fontsize=40, fontfamily=titlefont, color='w', weight='bold', 
                va='center', ha='right', family=titlefont,
                path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
        
        ax.text(7.8, 1, away_shots_on_target, fontsize=40, fontfamily=titlefont, color='w', weight='bold', 
                va='center', ha='left', family=titlefont,
                path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])