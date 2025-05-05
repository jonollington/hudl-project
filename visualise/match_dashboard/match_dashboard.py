# Standard library imports
import matplotlib
import matplotlib.pyplot as plt
from mplsoccer.pitch import Pitch
from PIL import Image

# Local application/library imports
from lib.util import path_effect_stroke, get_team_colors, extract_team_info, format_match_details
import lib.defence_stats as defence_stats
import lib.other_stats as other_stats
import lib.pass_stats as pass_stats
import lib.shot_stats as shot_stats
# from lib.stats_bar import stats_bar
from lib.plot_goal_post_home import plot_goal_post_home
from lib.plot_goal_post_away import plot_goal_post_away
from lib.plot_shots import plot_shots
from fetch.get_match_stats import get_match_stats
from fetch.get_match_shots import get_match_shots

# Constants
WHOSCORED_MATCH_ID = 1821321
FOTMOB_MATCH_ID = 4506534
bg = '#1b1f2b'
line_color = 'w'
titlefont = "BBC Reith Sans"
bodyfont = "BBC Reith Sans Cd"
FIG_SIZE = (12, 10)

# Fetch data
stats_df = get_match_stats(WHOSCORED_MATCH_ID, FOTMOB_MATCH_ID)
shots_df = get_match_shots(WHOSCORED_MATCH_ID)

# Extract team information and format details
home_team, away_team, home_row, away_row, save_string = extract_team_info(stats_df)
match_date, match_score, match_comp, match_season = format_match_details(stats_df)

# Setup fonts and pitch
matplotlib.rcParams['font.family'] = bodyfont
matplotlib.rcParams['figure.dpi'] = 150
pitch = Pitch(corner_arcs=True, goal_type='box', pitch_type='opta', linewidth=1)
pitch2 = Pitch(pitch_type='opta', pitch_color=bg, line_color=bg, linewidth=2)

# Get team colors
home_color, away_color = get_team_colors(home_team, away_team)

# Setup text properties
text_color = 'w'
text_box_style = 'round,pad=0.11'
pe = path_effect_stroke(linewidth=3, foreground=bg)
bbox_pad = 1.5
bboxprops = {'linewidth': 0, 'pad': bbox_pad}
highlight_textprops = [
    {'c': 'w', 'bbox': {'facecolor': home_color, **bboxprops}},
    {'c': 'w', 'bbox': {'facecolor': 'w', **bboxprops}},
    {'c': 'w', 'bbox': {'facecolor': away_color, **bboxprops}}
]

# Create figure and axes
fig = plt.figure(figsize=FIG_SIZE, constrained_layout=True)
gs = fig.add_gridspec(nrows=4, ncols=10)

ax1 = fig.add_subplot(gs[0:1,:4])
# shots_on_target(ax1, stats_df, bg, home_color, away_color, titlefont)
plot_goal_post_home(ax1, shots_df, pitch2, line_color, home_color)
ax1.axis('off')

ax2 = fig.add_subplot(gs[1:2, :4])
plot_goal_post_away(ax2, shots_df, pitch2, line_color, away_color)
ax2.axis('off')

ax3 = fig.add_subplot(gs[0:2, 4:])
pitch.draw(ax3)
plot_shots(shots_df, pitch, ax3, home_color, away_color)
ax3.axis('off')

ax4 = fig.add_subplot(gs[2:3,:5])
pass_stats.pass_stats(ax4, home_row, away_row, bg, home_color, away_color, text_color, text_box_style)
ax4.set_title("passes".upper(), color='w', size=20, weight='bold', family=titlefont)
ax4.axis('off')

ax5 = fig.add_subplot(gs[2:3,5:])
shot_stats.shot_stats(ax5, home_row, away_row, bg, home_color, away_color, text_color, text_box_style)
ax5.set_title("shots".upper(), color='w', size=20, weight='bold', family=titlefont)
ax5.axis('off')

ax6 = fig.add_subplot(gs[3:4,:5])
defence_stats.defence_stats(ax6, home_row, away_row, bg, home_color, away_color, text_color, text_box_style)
ax6.set_title("defence".upper(), color='w', size=20, weight='bold', family=titlefont)
ax6.axis('off')

ax7 = fig.add_subplot(gs[3:4,5:])
other_stats.other_stats(ax7, home_row, away_row, bg, home_color, away_color, text_color, text_box_style)
ax7.set_title("other".upper(), color='w', size=20, weight='bold', family=titlefont)
ax7.axis('off')

fig.text(0.5, 1.11, home_team.upper()+" "+match_score+" "+away_team.upper(),
         size=30, c='w', fontfamily=titlefont, ha='center', va='center',
         fontweight='black', zorder=2, style='italic')

fig.text(0.5, 1.07, match_comp+" • Season "+match_season+" • "+match_date,
         size=20, c='#a78d58', fontfamily=bodyfont, ha='center', va='center')

fig.text(1, -0.05, '@ j o n o l l i n g t o n', size=19, c='#a78d58', ha='right', va='center', weight='bold')

ax2 = fig.add_axes([0.05,1.05,0.1,0.1]) # badge
ax2.axis("off")
img = Image.open('../../logo//colour/arseblogGold.png')
ax2.imshow(img)

ax3 = fig.add_axes([-0.025,0,1.04,1.16]) # badge
ax3.axis("off")

fig.set_facecolor(bg)
# plt.show()
plt.savefig(f"../output_pngs/{save_string}.jpeg", bbox_inches='tight',facecolor=bg)