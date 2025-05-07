import pandas as pd
import numpy as np
import matplotlib.patheffects as path_effects
from mplsoccer import VerticalPitch, arrowhead_marker

from lib.player_plot import player_plot

def calculate_metrics(df):
    goal_count = (df['outcome'] == 'goal').sum() 
    shot_count = len(df)
    xG = round(df['xg'].sum(), 2)
    
    labels = ['goals', 'shots', 'xG']
    values = [goal_count, shot_count, xG]
    start_x = 25
    spacing = 15
    
    return labels, values, start_x, spacing

def setup_pitch(bg, text_color):
    pitch = VerticalPitch(
        corner_arcs=True, pitch_color=bg, line_color=text_color,
        linewidth=1.5, line_zorder=2, goal_type='box',
        half=True, pitch_type='statsbomb', pad_bottom=0.1
    )
    fig, ax = pitch.draw(figsize=(10, 7.727))
    
    return pitch, fig, ax

def plot_events(ax, df, pitch, bg):
    for event_type in df['outcome'].unique():
        events = df[df['outcome'] == event_type]
        sizes = events['xg'] * 1000

        scatter_kwargs = dict(
            x=events['start_x'], y=events['start_y'],
            s=sizes, ax=ax, zorder=4, alpha=0.8
        )
        if event_type == 'goal':
            pitch.scatter(**scatter_kwargs, c='red')
        else:
            pitch.scatter(**scatter_kwargs, c=bg, lw=2, edgecolors='blue')

        angle, _ = pitch.calculate_angle_and_distance(
            events['start_x'], events['start_y'],
            events['end_x'], events['end_y'],
            standardized=False, degrees=True
        )
        pitch.lines(
            events['start_x'], events['start_y'],
            events['end_x'], events['end_y'],
            comet=False,
            transparent=True,
            lw=2,
            alpha_start=0,
            alpha_end=0.8,
            color='#e7e7e7',
            ax=ax,
            zorder=2
        )
        pitch.scatter(
            events['end_x'], events['end_y'],
            rotation_degrees=angle,
            color='#e7e7e7',
            s=50,
            ax=ax,
            marker=arrowhead_marker,
            zorder=3
        )

def add_metrics_boxes(ax, pitch, values, start_x, spacing, text_color, bg):
    labels = ['goals', 'shots', 'xG']
    for i, label in enumerate(labels):
        x_position = start_x + i * spacing
        y_position = 140 / 2
        pitch.scatter(y_position, x_position, s=5000, ax=ax, marker='s', color='#e7e7e7', alpha=1, zorder=3)
        ax.text(x_position, y_position-6, label, va='center', ha='center', size=18, c=text_color)
        ax.text(x_position, y_position-0.1, values[i], va='center', ha='center', size=32, weight='black',
                color=text_color, path_effects=[path_effects.withStroke(linewidth=5, foreground=bg)])

def add_metric_labels(ax1, text_color, line_color):
    ax1.axis('off')
    ax1.set_ylim(0, 13)
    ax1.set_xlim(0, 3)

    labels = [
        ("GOALS", 11.8), ("SHOTS", 8.8),
        ("EXPECTED GOALS (xG)", 5.8), ("EXPECTED GOALS ON TARGET (xGOT)", 2.8)
    ]
    for text, y in labels:
        ax1.text(x=0.3, y=y, s=text, size=15, va='center', ha='left', c=text_color)

    for y in [11.5, 8.5, 5.5, 2.5]:
        ax1.plot([0.2, 3.3], [y, y], lw='1.5', c=text_color)
    for y in [9.3, 6.3, 3.3, 0.3]:
        ax1.plot([0.2, 3.2], [y, y], lw='0.5', c=line_color, ls='dotted')

def plot_top_players(df, positiondict, metric, key, folder_path, line_color, text_color, bodyfont, ascending=False):
    players_df = df[df[key] > 0].sort_values(by=key, ascending=ascending)
    positions = positiondict[metric]
    for i in range(min(len(players_df), len(positions))):
        pos = positions[i]
        a1 = plt.axes([pos[0], pos[1], .15, .15])
        surname = players_df.iloc[i]['player_name'].split()[-1]
        player_plot(a1, surname, folder_path, line_color, text_color, bodyfont)
        value = str(players_df.iloc[i][key])
        a1.text(5.1, 2.4, value, size=22, va='center', ha='center', color=text_color, weight='black',
                path_effects=[path_effects.withStroke(linewidth=6, foreground='w')])
        a1.axis('off')


