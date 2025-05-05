def defence_stats(ax, home_row, away_row, bg, home_color, away_color, text_color, text_box_style):

    rows = 7
    cols = 3
    
    ax.set_ylim(0, rows + 0.2)
    ax.set_xlim(0, cols)
    ax.set_facecolor(bg)

    # Calculate percentages
    home_tackle_won_percent = round((home_row['total_tackles_won'] / home_row['total_tackles']) * 100)
    away_tackle_won_percent = round((away_row['total_tackles_won'] / away_row['total_tackles']) * 100)

    home_duels_won_percent = round((home_row['total_duels_won'] / home_row['total_duels']) * 100)
    away_duels_won_percent = round((away_row['total_duels_won'] / away_row['total_duels']) * 100)

    home_ground_duels_won_percent = round((home_row['total_ground_duels_won'] / home_row['total_ground_duels']) * 100)
    away_ground_duels_won_percent = round((away_row['total_ground_duels_won'] / away_row['total_ground_duels']) * 100)

    home_aerial_duels_won_percent = round((home_row['total_aerial_duels_won'] / home_row['total_aerial_duels']) * 100)
    away_aerial_duels_won_percent = round((away_row['total_aerial_duels_won'] / away_row['total_aerial_duels']) * 100)
    
    stats = [
        ('Tackles won', 
         f"{home_row['total_tackles_won']} ({home_tackle_won_percent}%)", 
         f"{away_row['total_tackles_won']} ({away_tackle_won_percent}%)"),
        ('Interceptions won', home_row['total_interceptions'], away_row['total_interceptions']),
        ('Blocked passes', home_row['total_blocked_passes'], away_row['total_blocked_passes']),
        ('Clearances', home_row['total_clearances'], away_row['total_clearances']),
        ('Duels won', 
         f"{home_row['total_duels_won']} ({home_duels_won_percent}%)", 
         f"{away_row['total_duels_won']} ({away_duels_won_percent}%)"),
        ('Ground duels won', 
         f"{home_row['total_ground_duels_won']} ({home_ground_duels_won_percent}%)", 
         f"{away_row['total_ground_duels_won']} ({away_ground_duels_won_percent}%)"),
        ('Aerial duels won', 
         f"{home_row['total_aerial_duels_won']} ({home_aerial_duels_won_percent}%)", 
         f"{away_row['total_aerial_duels_won']} ({away_aerial_duels_won_percent}%)"),
    ]


    # Map each label to the corresponding DataFrame column
    label_to_column = {
        'Tackles won': 'total_tackles_won',
        'Interceptions won': 'total_interceptions',
        'Blocked passes': 'total_blocked_passes',
        'Clearances': 'total_clearances',
        'Duels won': 'total_duels_won',
        'Ground duels won': 'total_ground_duels_won',
        'Aerial duels won': 'total_aerial_duels_won'
    }
    
    font_size = 18
    for row, (label, home_stat, away_stat) in enumerate(stats, start=1):
        y_position = rows - row + 0.5
        
        # Use the label_to_column mapping to get the correct column name
        column_name = label_to_column[label]
        
        if home_row[column_name] > away_row[column_name]:
            higher_stat, lower_stat = home_stat, away_stat
            box_x_position_higher, box_x_position_lower = 0.45, 2.25
            align_higher, align_lower = 'right', 'left'
            text_facecolor = home_color
        else:
            higher_stat, lower_stat = away_stat, home_stat
            box_x_position_higher, box_x_position_lower = 2.25, 0.45
            align_higher, align_lower = 'left', 'right'
            text_facecolor = away_color
        
        ax.text(1.5, y_position, label, ha='center', va='center', size=font_size, color='silver')
        ax.text(box_x_position_lower + 0.2, y_position, str(lower_stat), ha=align_lower, va='center', size=font_size, color=text_color)
        
        # Apply highlighting to the higher stat if they are not equal
        ax.text(box_x_position_higher + 0.2, y_position, str(higher_stat), ha=align_higher, va='center', size=font_size, color=text_color, 
                bbox=dict(boxstyle=text_box_style, facecolor=text_facecolor, alpha=0.9) if higher_stat != lower_stat else None)
        
    ax.plot([0, cols + 1], [7.1, 7.1], lw='1', c='grey')
    ax.axis('off')