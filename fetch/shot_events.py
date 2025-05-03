import requests
import pandas as pd
from auth.token_manager import access_token

# Set up access
graphql_url = "https://live-api.statsbomb.com/v1/graphql"
headers = {
    "Authorization": f"Bearer {access_token}"
}

# Query 1: Shots
query_shots = """
{
  live_match_event(
    where: { match_id: { _eq: 1358854 }, name: { _eq: "shot" } }
  ) {
    name
    outcome
    player_id
    xg
    team_id
    start_x
    start_y
    end_x
    end_y
    minute
    second
  }
}
"""

# Query 2: Player info
query_players = """
{
  live_lineup(
    where: { match_id: { _eq: 1358854 } }
  ) {
    player_id
    player_name
    team_name
  }
}
"""

# Request shots
resp_shots = requests.post(graphql_url, json={"query": query_shots}, headers=headers)
shots_data = resp_shots.json()["data"]["live_match_event"]
df_shots = pd.DataFrame(shots_data)

# Request player info
resp_players = requests.post(graphql_url, json={"query": query_players}, headers=headers)
players_data = resp_players.json()["data"]["live_lineup"]
df_players = pd.DataFrame(players_data)

# Merge player info into shot data
df = df_shots.merge(df_players, on="player_id", how="left")
print(df)
