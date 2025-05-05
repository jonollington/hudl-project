def shot_stats(ax, home_row, away_row, bg, home_color, away_color, text_color, text_box_style):

    rows = 7
    cols = 3
    
    ax.set_ylim(0, rows + 0.2)
    ax.set_xlim(0, cols)
    ax.set_facecolor(bg)
    
    stats = [
        ('Expected goal (xG)', home_row['total_xg'], away_row['total_xg']),
        ('Post shot xG (psxG)', home_row['total_psxg'], away_row['total_psxg']),
        ('xG open play', home_row['total_xg_open_play'], away_row['total_xg_open_play']),
        ('Blocked shots', home_row['total_blocked_shots'], away_row['total_blocked_shots']),
        ('Hit woodwork', home_row['total_hit_woodwork'], away_row['total_hit_woodwork']),
        ('Shots inside box', home_row['total_shots'] - home_row['total_shots_outside_box'], away_row['total_shots'] - away_row['total_shots_outside_box']),
        ('Shots outside box', home_row['total_shots_outside_box'], away_row['total_shots_outside_box'])
    ]
    
    font_size = 18
    for row, (label, home_stat, away_stat) in enumerate(stats, start=1):
        y_position = rows - row + 0.5
        
        if home_stat > away_stat:
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
        
        ax.text(box_x_position_higher + 0.2, y_position, str(higher_stat), ha=align_higher, va='center', size=font_size, color=text_color, 
                bbox=dict(boxstyle=text_box_style, facecolor=text_facecolor, alpha=0.9) if higher_stat != lower_stat else None)
        
    ax.plot([0, cols + 1], [7.1, 7.1], lw='1', c='grey')
    ax.axis('off')