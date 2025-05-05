def pass_stats(ax, home_row, away_row, bg, home_color, away_color, text_color, text_box_style):
    rows = 7
    cols = 3
    
    ax.set_ylim(0, rows + 0.2)
    ax.set_xlim(0, cols)
    ax.set_facecolor(bg)
    
    # Calculate percentages
    home_pass_percent = round((home_row['total_successful_passes'] / home_row['total_passes']) * 100)
    away_pass_percent = round((away_row['total_successful_passes'] / away_row['total_passes']) * 100)

    home_long_pass_percent = round((home_row['total_successful_long_passes'] / home_row['total_long_passes']) * 100)
    away_long_pass_percent = round((away_row['total_successful_long_passes'] / away_row['total_long_passes']) * 100)

    home_cross_percent = round((home_row['total_successful_crosses'] / home_row['total_crosses']) * 100)
    away_cross_percent = round((away_row['total_successful_crosses'] / away_row['total_crosses']) * 100)
    
    stats = [
        ('Total passes', home_row['total_passes'], away_row['total_passes']),
        ('Accurate passes', 
         f"{home_row['total_successful_passes']} ({home_pass_percent}%)", 
         f"{away_row['total_successful_passes']} ({away_pass_percent}%)"),
        ('Own half', home_row['total_passes_own_half'], away_row['total_passes_own_half']),
        ('Opposition half', home_row['total_passes_opposition_half'], away_row['total_passes_opposition_half']),
        ('Accurate long passes', 
         f"{home_row['total_successful_long_passes']} ({home_long_pass_percent}%)", 
         f"{away_row['total_successful_long_passes']} ({away_long_pass_percent}%)"),
        ('Accurate crosses', 
         f"{home_row['total_successful_crosses']} ({home_cross_percent}%)", 
         f"{away_row['total_successful_crosses']} ({away_cross_percent}%)"),
        ('Field Tilt', home_row['field_tilt'], away_row['field_tilt'])
    ]
    
    # Map each label to the corresponding DataFrame column
    label_to_column = {
        'Total passes': 'total_passes',
        'Accurate passes': 'total_successful_passes',
        'Own half': 'total_passes_own_half',
        'Opposition half': 'total_passes_opposition_half',
        'Accurate long passes': 'total_successful_long_passes',
        'Accurate crosses': 'total_crosses',
        'Field Tilt': 'field_tilt'
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
