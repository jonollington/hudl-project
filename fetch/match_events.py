import requests
import pandas as pd
from auth.token_manager import access_token

def get_match_data(match_id: int) -> pd.DataFrame:
    graphql_url = "https://live-api.statsbomb.com/v1/graphql"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # Query: Shots
    query_events = f"""
    {{
      live_match_event(
        where: {{ match_id: {{ _eq: {match_id} }} }}
      ) {{
        name
        outcome
        player_id
        team_id
        start_x
        start_y
        end_x
        end_y
        minute
        second
        duration
        timestamp
      }}
    }}
    """


    # Query: Player info
    query_players = f"""
    {{
      live_lineup(
        where: {{ match_id: {{ _eq: {match_id} }} }}
      ) {{
        player_id
        player_name
        team_name
      }}
    }}
    """

    # Query: Match metadata
    query_match = f"""
    {{
      live_match(
        where: {{ match_id: {{ _eq: {match_id} }} }}
      ) {{
        match_date
        match_local_kick_off
        match_id
        match_home_team_name
        match_home_team_id
        match_away_team_name
        match_away_team_id
        round_type_name
        round_id
      }}
    }}
    """

    # Query: Competition season info
    query_competition = """
    {
      live_competition_season {
        season_name
        competition_name
        competition_id
        season_id
      }
    }
    """

    # Send requests
    r1 = requests.post(graphql_url, json={"query": query_events}, headers=headers)
    r2 = requests.post(graphql_url, json={"query": query_players}, headers=headers)
    r3 = requests.post(graphql_url, json={"query": query_match}, headers=headers)
    r4 = requests.post(graphql_url, json={"query": query_competition}, headers=headers)

    passes = r1.json()["data"]["live_match_event"]
    players = r2.json()["data"]["live_lineup"]
    match_info = r3.json()["data"]["live_match"]
    competition_info = r4.json()["data"]["live_competition_season"]

    df_passes = pd.DataFrame(passes)
    df_players = pd.DataFrame(players)
    df_match = pd.DataFrame(match_info)
    df_competition = pd.DataFrame(competition_info)

    if df_passes.empty or df_players.empty or df_match.empty or df_competition.empty:
        return pd.DataFrame()

    # Merge player info into pass data
    match_events = df_passes.merge(df_players, on="player_id", how="left")

    # Merge match info into pass data
    for col in df_match.columns:
        match_events[col] = df_match.at[0, col]

    # Add competition season info (broadcasting to match data)
    for col in df_competition.columns:
        match_events[col] = df_competition.at[0, col]

    return match_events
