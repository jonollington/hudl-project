# Initialise the pitch
pitch = VerticalPitch(pitch_type='uefa', pitch_color=bg, linewidth=1, corner_arcs=True,
                      line_zorder=2, line_color=pitch_line_color, goal_type='box')
fig, ax = pitch.draw(figsize=(16, 9))

# ax.set_xlim(-0.5, 105.5)
ax.set_ylim(-19, 110)

# Analyse defensive actions
average_locs, grouped_true_tackles_interceptions, grouped_true_interceptions, grouped_aerial_duels, grouped_recoveries = analyse_defensive_actions(
    average_locs_and_count_df,
    defensive_actions_df,
    team_name='Arsenal'
)

average_locs_and_count_df = average_locs_and_count_df[average_locs_and_count_df['team_name'] == 'Arsenal']
defensive_actions_team_df = defensive_actions_df[defensive_actions_df["team_name"] == 'Arsenal']

plot_defensive_action_lines(ax, average_locs_and_count_df)
# plotting the heatmap of the team defensive actions
color = np.array(to_rgba(away_color))
cmap = LinearSegmentedColormap.from_list("", [bg, away_color], N=500)
kde = pitch.kdeplot(defensive_actions_team_df.x, defensive_actions_team_df.y, ax=ax, fill=True, levels=5000, thresh=0.02, cut=4, cmap=cmap)
# da_scatter = pitch.scatter(defensive_actions_team_df.x, defensive_actions_team_df.y, s=10, marker='x', color='w', alpha=0.2, ax=ax)


average_locs_and_count_df.loc[average_locs_and_count_df['player_name'] == 'Riccardo Calafiori', 'is_first_eleven'] = False
average_locs_and_count_df.loc[average_locs_and_count_df['player_name'] == 'Ben White', 'is_first_eleven'] = True
average_locs_and_count_df.loc[average_locs_and_count_df['player_name'] == 'Leandro Trossard', 'is_first_eleven'] = True

# Scatter plot for defensive actions
for index, row in average_locs_and_count_df.iterrows():
    marker_shape = 'o' if row['is_first_eleven'] else 's'
    da_nodes = pitch.scatter(
        row['x'], row['y'], 
        s=row['marker_size'] + 100, 
        marker=marker_shape, 
        color=bg, 
        edgecolor=line_color, 
        linewidth=2, 
        alpha=0.8, 
        zorder=4 if row['is_first_eleven'] else 3, 
        ax=ax
    )

    # Annotate player initials
    player_initials = row["shirt_no"]
    pitch.annotate(
        player_initials, 
        xy=(row.x, row.y), 
        c=line_color, 
        ha='center', 
        va='center', 
        size=14, 
        zorder=5, 
        ax=ax, 
        weight='bold',
        path_effects=[path_effects.withStroke(linewidth=5, foreground=bg)]
    )

# Create an additional axis for defensive stats
ax1 = fig.add_axes((0.7, 0.06, 0.38, 0.815))
ax1.axis('off')

# Plot defensive stats
plot_defensive_stats(ax1, grouped_true_tackles_interceptions, grouped_true_interceptions, grouped_aerial_duels, grouped_recoveries, folder_path, line_color, text_color, bodyfont, bg)

# Set title for the shot map
ax.set_title("defensive block".upper(), size=40, weight='black', family=titlefont,
             y=1.05, style='italic', c='w')
ax.text(0.5, 1.02, 'Premier League • '+match_date+' • '+home_team+' '+match_score+' '+away_team, size=16, ha='center', va='center', c=line_color,transform=ax.transAxes)
ax.text(67,104, "circle: starter\nsquare: sub", color='gray', size=11, ha='left', va='top',
          path_effects=[path_effects.withStroke(linewidth=6, foreground=bg)]
        )

# Set figure background color
fig.patch.set_facecolor(bg)
ax.set_facecolor(bg)

fig.text(1.09, 0.03, '@ j o n o l l i n g t o n',
           ha='right', fontsize=15, color=line_color)


ax2 = fig.add_axes([1,0.91,0.1,0.1]) # badge
ax2.axis("off")
img = Image.open('../../logo/colour/cannonSilver.png')
ax2.imshow(img)

cSize = [50,150,300,0]
cSizeS = [10000 * i for i in cSize]
cx = [0,0.027,0.06,0.15]
cy = [0,0,0,0]

#arrow
arrow="Simple,tail_width=0.05,head_width=0.8,head_length=0.8"
ax2 = fig.add_axes([0.45,0.04,0.25,0.05])
ax2.axis("off")
ax2.annotate('', (0.4,0),(0,0), zorder=10, arrowprops=dict(arrowstyle=arrow, color=line_color,alpha=1))


fig.text(0.5,0.055, "Defensive Actions", color=text_color, fontfamily=titlefont, size=10, va='center',ha='center')
ax3 = fig.add_axes([0.465,0.06,0.15,0.05])
ax3.axis("off")
ax3.scatter(cx,cy,s=cSize, color=bg,ec=text_color,lw=1,alpha=1)

# Single colorbar with increased height (taller)
a1 = plt.axes([0.455, -0.03, 0.08, 0.4])  # Increased the height to make it taller
cbar = fig.colorbar(cm.ScalarMappable(norm=None, cmap=cmap), ax=a1, location='bottom')
cbar.set_ticks([])
cbar.outline.set_visible(False)
a1.axis("off")
a1.set_facecolor(bg)


# Save the figure
plt.savefig("../../output-scripts/output_pngs/defensive_actions.jpeg", bbox_inches='tight', format='jpeg')