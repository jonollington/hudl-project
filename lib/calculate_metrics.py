def calculate_metrics(df):
    goal_count = (df['outcome'] == 'goal').sum() 
    shot_count = len(df)
    xG = round(df['xg'].sum(), 2)
    
    labels = ['xG', 'shots', 'goals']
    values = [xG, shot_count, goal_count]
    start_x = 25
    spacing = 15
    
    return labels, values, start_x, spacing