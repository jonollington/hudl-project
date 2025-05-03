import os
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import matplotlib.patheffects as path_effects

def player_plot(ax, player_name, folder_path, line_color, text_color, bodyfont):
    rows = 5
    cols = 5
    
    ax.set_ylim(0, rows)
    ax.set_xlim(0, cols)
    
    # Player background
    ax.scatter(2.5, 2.5, c='w', s=2600, marker='o', alpha=1, lw=1, 
               ec=line_color, path_effects=[path_effects.withStroke(linewidth=3, foreground='w')])
    
    ax.text(2.5, 0.5, player_name.upper(), color=text_color, va='center', ha='center', size=11, zorder=3,
            weight='bold', fontfamily=bodyfont)
    
    # Add player image if available
    image_path = os.path.join(folder_path, player_name + '.png')
    
    if os.path.exists(image_path):
        try:
            image = OffsetImage(plt.imread(image_path), zoom=.21, alpha=1)
            ab = AnnotationBbox(image, (2.5, 2.577), frameon=False)
            ax.add_artist(ab)
        except Exception:
            # Silent fail, just skip adding the image
            pass
