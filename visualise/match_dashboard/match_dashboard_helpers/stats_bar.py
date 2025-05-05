import matplotlib.pyplot as plt
import matplotlib.patheffects as path_effects
import numpy as np
from decimal import Decimal

def stats_bar(ax, home_row, away_row, bg, home_color, away_color):
    # Helper function to ensure values are floats
    def to_float(value):
        if isinstance(value, Decimal):
            return float(value)
        return value

    # Data
    stats = [
        ('Possession', home_row['possession'], away_row['possession']),
        ('Field tilt', home_row['field_tilt'], away_row['field_tilt']),
        ('PPDA', home_row['field_tilt'], away_row['field_tilt']),
        ('Touches in oppo. box', home_row['possession'], away_row['possession'])
    ]

    # Normalize the values to a range of 0 to 100
    normalized_values = [
        (to_float(stat[1]), to_float(stat[2])) if to_float(stat[1]) + to_float(stat[2]) == 100 
        else (to_float(stat[1]) / (to_float(stat[1]) + to_float(stat[2])) * 100, 
              to_float(stat[2]) / (to_float(stat[1]) + to_float(stat[2])) * 100)
        for stat in stats
    ]

    # Reverse the order to have "Possession" on top
    labels = [stat[0] for stat in stats][::-1]
    normalized_values = normalized_values[::-1]

    # Create a horizontal bar chart with rounded ends
    for i, stat in enumerate(normalized_values):
        # Lengths of the home and away bars
        home_length = stat[0]
        away_length = stat[1]
        
        # Draw home bar with adjusted length
        ax.barh(labels[i], home_length, color=home_color, edgecolor='none', alpha=0.9)
        # Draw away bar with adjusted length, starting after home bar
        ax.barh(labels[i], away_length, left=home_length, color=away_color, edgecolor='none', alpha=0.9)
        
        # Add a thin edge line in the middle of the bars
        edge_offset = 0.5  # Adjust this value to fit your style
        ax.barh(labels[i], edge_offset, left=home_length - edge_offset / 2, color=bg, edgecolor=bg)
        ax.barh(labels[i], edge_offset, left=home_length + away_length - edge_offset / 2, color=bg, edgecolor=bg)
        
        # Add text to the middle of each bar
        if labels[i] == 'Possession':
            ax.text(home_length / 9.8, i, f'{home_length:.1f}%', color='white', ha='left', va='center', size=20,
                     path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
            ax.text(home_length + away_length / 1.1, i, f'{away_length:.1f}%', color='white', ha='right', va='center', size=20,
                     path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
        else:
            ax.text(home_length / 9.8, i, f'{home_length:.1f}', color='white', ha='left', va='center', size=20,
                     path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
            ax.text(home_length + away_length / 1.1, i, f'{away_length:.1f}', color='white', ha='right', va='center', size=20,
                     path_effects=[path_effects.withStroke(linewidth=3, foreground=bg)])
        
        # Add text with the metric name centered on the y-axis
        ax.text(50, i, labels[i], color='w', ha='center', va='center', size=20,
                 path_effects=[path_effects.withStroke(linewidth=2, foreground=bg)])

    # Set the x-axis limit to 100 for normalization
    ax.set_xlim(0, 100)
    ax.set_facecolor(bg)
    ax.set_yticks([])
