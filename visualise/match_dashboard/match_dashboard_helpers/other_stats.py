def other_stats(ax, home_row, away_row, bg, home_color, away_color, text_color, text_box_style):

    rows = 7
    cols = 3
    
    ax.set_ylim(0, rows + 0.2)
    ax.set_xlim(0, cols)
    ax.set_facecolor(bg)

    # Calculate percentages
    home_dribble_percent = round((home_row['total_successful_dribbles'] / home_row['total_dribbles']) * 100)
    away_dribble_percent = round((away_row['total_successful_dribbles'] / away_row['total_dribbles']) * 100)
    
    stats = [
        ('Successful dribbles', 
         f"{home_row['total_successful_dribbles']} ({home_dribble_percent}%)", 
         f"{away_row['total_successful_dribbles']} ({away_dribble_percent}%)"),
        ('Fouls committed', home_row['total_fouls'], away_row['total_fouls']),
        ('Yellow cards', home_row['total_yellow_cards'], away_row['total_yellow_cards']),
        ('Red cards', home_row['total_red_cards'], away_row['total_red_cards']),
        ('Offsides', home_row['total_offsides'], away_row['total_offsides']),
        ('Corners', home_row['total_corners'], away_row['total_corners']),
        ('Throws', home_row['total_throws'], away_row['total_throws'])
    ]
    
    # Map each label to the corresponding DataFrame column
    label_to_column = {
        'Successful dribbles': 'total_successful_dribbles',
        'Fouls committed': 'total_fouls',
        'Yellow cards': 'total_yellow_cards',
        'Red cards': 'total_red_cards',
        'Offsides': 'total_offsides',
        'Corners': 'total_corners',
        'Throws': 'total_throws'
    }
    
    # Define which stats should highlight the lower value
    highlight_lower = {'Fouls committed', 'Yellow cards', 'Red cards', 'Offsides'}
    
    font_size = 18
    for row, (label, home_stat, away_stat) in enumerate(stats, start=1):
        y_position = rows - row + 0.5
        
        # Use the label_to_column mapping to get the correct column name
        column_name = label_to_column[label]
        
        if label in highlight_lower:
            # For these labels, highlight the lower value
            if home_row[column_name] < away_row[column_name]:
                higher_stat, lower_stat = home_stat, away_stat
                box_x_position_higher, box_x_position_lower = 0.45, 2.25
                align_higher, align_lower = 'right', 'left'
                text_facecolor = home_color
            else:
                higher_stat, lower_stat = away_stat, home_stat
                box_x_position_higher, box_x_position_lower = 2.25, 0.45
                align_higher, align_lower = 'left', 'right'
                text_facecolor = away_color
        else:
            # For other labels, highlight the higher value
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
        
        # Apply highlighting to the correct stat based on the logic
        ax.text(box_x_position_higher + 0.2, y_position, str(higher_stat), ha=align_higher, va='center', size=font_size, color=text_color, 
                bbox=dict(boxstyle=text_box_style, facecolor=text_facecolor, alpha=0.9) if higher_stat != lower_stat else None)
        
    ax.plot([0, cols + 1], [7.1, 7.1], lw='1', c='grey')
    ax.axis('off')
