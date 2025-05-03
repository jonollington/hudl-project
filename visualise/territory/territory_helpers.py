import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from highlight_text import ax_text
from mplsoccer import Pitch

def create_heatmap(ax, bin_statistic1, bin_statistic2, cmap, pitch):
    cx = np.array([[8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                   [8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                   [8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                   [8.75, 26.25, 43.75, 61.25, 78.75, 96.25],
                   [8.75, 26.25, 43.75, 61.25, 78.75, 96.25]])

    cy = np.array([[61.2, 61.2, 61.2, 61.2, 61.2, 61.2],
                   [47.6, 47.6, 47.6, 47.6, 47.6, 47.6],
                   [34.0, 34.0, 34.0, 34.0, 34.0, 34.0],
                   [20.4, 20.4, 20.4, 20.4, 20.4, 20.4],
                   [6.8, 6.8, 6.8, 6.8, 6.8, 6.8]])

    cx_flat = cx.flatten()
    cy_flat = cy.flatten()

    df_cong = pd.DataFrame({'cx': cx_flat, 'cy': cy_flat})

    hd_values = []
    for i in range(bin_statistic1['statistic'].shape[0]):
        for j in range(bin_statistic1['statistic'].shape[1]):
            stat1 = bin_statistic1['statistic'][i, j]
            stat2 = bin_statistic2['statistic'][i, j]
        
            if (stat1 / (stat1 + stat2)) > 0.55:
                hd_values.append(1)
            elif (stat1 / (stat1 + stat2)) < 0.45:
                hd_values.append(0)
            else:
                hd_values.append(0.5)

    df_cong['hd'] = hd_values
    bin_stat = pitch.bin_statistic(df_cong.cx, df_cong.cy, bins=(6, 5), values=df_cong['hd'], statistic='sum', normalize=False)
    pitch.heatmap(bin_stat, ax=ax, cmap=cmap, edgecolors='#000000', lw=0, zorder=3, alpha=0.85)

def add_arrow(ax, x_start, y_start, x_end, y_end, color):
    arrow = "Simple, tail_width=0.05, head_width=0.8, head_length=0.8"
    ax.annotate('', xy=(x_end, y_end), xytext=(x_start, y_start),
                arrowprops=dict(arrowstyle=arrow, color=color, alpha=1))

def plot_texts(ax, home_team, away_team, home_color, away_color, line_color, match_comp, match_date, match_score, bg):

    bbox_pad = 1
    bboxprops = {'linewidth': 0, 'pad': bbox_pad}

    highlight_textprops = [{'c': bg, 'bbox': {'facecolor': home_color, **bboxprops}},
                           {'c': bg, 'bbox': {'facecolor': away_color, **bboxprops}},
                           {'c': bg, 'bbox': {'facecolor': 'gray', **bboxprops}}]

    ax.set_title("Who controls territory?", color=line_color, fontsize=20, fontweight='bold', x=0.025, y=1.07, ha='left')
    ax.text(0, 72.5, f"{match_comp} • {match_date} • {home_team} {match_score} {away_team}", color='gray', fontsize=8, ha='left', va='center')
    
    ax_text(0, 70, s=f"Zones are labelled  <{home_team.upper()}>  or  <{away_team.upper()}>  where either team accounts for more than 55% of total touches, while the remaining zones are considered  <CONTESTED>",
            highlight_textprops=highlight_textprops, color='gray', fontsize=8, ha='left', va='center', ax=ax)
    
    # Text for home team attack
    ax.text(0, -3, 'ATTACK', color=home_color, fontsize=10, ha='left', va='center', weight='bold')
    add_arrow(ax, 10, -3, 35, -3, home_color)  # Add arrow after the home team "Attack"

    # Text for away team attack
    ax.text(105, -3, 'ATTACK', color=away_color, fontsize=10, ha='right', va='center', weight='bold')
    add_arrow(ax, 95, -3, 70, -3, away_color)  # Add arrow after the away team "Attack"


def add_pitch_lines(ax, bg, pitch_length=105, pitch_width=68):
    for i in range(1, 6):
        ax.vlines(i * (pitch_length / 6), ymin=0, ymax=pitch_width, color=bg, lw=2, ls='--', zorder=5, linewidth=1)
    for i in range(1, 6):
        ax.hlines(i * (pitch_width / 5), xmin=0, xmax=pitch_length, color=bg, lw=2, ls='--', zorder=5, linewidth=1)