import matplotlib
import matplotlib.font_manager as fm

import matplotlib.patheffects as path_effects

def is_font_available(font_name):
    return any(font_name in font.name for font in fm.fontManager.ttflist)

def setup_visualisation_params(theme='dark'):
    # Define theme colors
    if theme == 'dark':
        bg = '#1b1f2b'
        pitch_line_color = '#59595a'
        line_color = '#e5e4e7'
        text_color = '#f8f8f9'
        pass_color = '#ffc53c'
        carry_color = '#5aace2'
    elif theme == 'light':
        bg = '#f8f8f9'
        text_color = '#1d1c1c'
        line_color = '#a4a4a4'
        pitch_line_color = '#1d1c1c'
        pass_color = '#ffc53c'
        carry_color = '#5aace2'
    else:
        raise ValueError("Invalid theme specified. Choose 'dark' or 'light'.")

    # Primary and fallback fonts
    primary_titlefont = "BBC Reith Sans"
    primary_bodyfont = "BBC Reith Sans Cd"
    fallback_titlefont = "Neusa Next Std"
    fallback_bodyfont = "Neusa Next Std"

    # Check if primary fonts are available, otherwise use fallback
    titlefont = primary_titlefont if is_font_available(primary_titlefont) else fallback_titlefont
    bodyfont = primary_bodyfont if is_font_available(primary_bodyfont) else fallback_bodyfont

    # Set font family and figure DPI
    matplotlib.rcParams['font.family'] = bodyfont
    matplotlib.rcParams['figure.dpi'] = 550

    folder_path = '../../players/'

    # Return all parameters as a dictionary
    visualisation_params = {
        "bg": bg,
        "line_color": line_color,
        "pitch_line_color": pitch_line_color,
        "pass_color": pass_color,
        "carry_color": carry_color,
        "text_color": text_color,
        "titlefont": titlefont,
        "bodyfont": bodyfont,
        "figure_dpi": 550,
        "folder_path": folder_path
    }

    return visualisation_params


def get_team_colors(team_info, theme='dark'):
    home_team = team_info['home_team']
    away_team = team_info['away_team']
    # Define theme colors
    if theme == 'dark':
        home_color = '#be0a24'
        away_color = '#959595'
    elif theme == 'light':
        home_color = '#f2096f'
        away_color = '#3089f9'
    elif theme == 'trad':
        home_color = '#ff4b44'
        away_color = '#00a0de'

    team_colors = {
    "home_color": home_color,
    "away_color": away_color
    }
    
    return team_colors