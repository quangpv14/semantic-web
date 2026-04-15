import os
import requests
import json
import time
import pandas as pd
from dotenv import load_dotenv


# =========================
# CONFIG
# =========================
load_dotenv()
API_KEY = os.getenv("API_KEY")
print("API_KEY:", "FOUND" if API_KEY else "NOT FOUND")
if not API_KEY:
    raise RuntimeError("API_KEY not found.")

BASE_URL = "https://v3.football.api-sports.io"

HEADERS = {
    "x-apisports-key": API_KEY
}

LEAGUE_ID = 39      # Premier League
SEASON = 2024

# GET TEAMS
def get_teams():
    url = f"{BASE_URL}/teams?league={LEAGUE_ID}&season={SEASON}"
    res = requests.get(url, headers=HEADERS)
    data = res.json()

    teams = []
    stadiums = []

    for t in data["response"]:
        team = t["team"]
        venue = t.get("venue", {})

        team_id = team["id"]
        stadium_id = venue.get("id")

        teams.append({
            "team_id": team_id,
            "team_name": team["name"],
            "country": team.get("country"),
            "founded": team.get("founded"),
            "stadium_id": stadium_id
        })

        # STADIUM DATA
        stadiums.append({
            "stadium_id": stadium_id,
            "stadium_name": venue.get("name"),
            "city": venue.get("city"),
            "address": venue.get("address"),
            "capacity": venue.get("capacity"),
            "surface": venue.get("surface"),
            "image": venue.get("image"),
            "team_id": team_id
        })

    return teams, stadiums

#GET COACHES
def get_coaches(team_id):
    url = f"{BASE_URL}/coachs?team={team_id}"
    res = requests.get(url, headers=HEADERS)

    if res.status_code != 200:
        print("ERROR:", res.text)
        return []

    data = res.json()

    coaches = []

    for c in data.get("response", []):
        coaches.append({
            "coach_id": c.get("id"),
            "name": c.get("name"),
            "firstname": c.get("firstname"),
            "lastname": c.get("lastname"),
            "age": c.get("age"),
            "nationality": c.get("nationality"),

            # birth info
            "birth_date": c.get("birth", {}).get("date"),
            "birth_place": c.get("birth", {}).get("place"),
            "birth_country": c.get("birth", {}).get("country"),

            # physical
            "height": c.get("height"),
            "weight": c.get("weight"),

            # team hiện tại
            "team_id": c.get("team", {}).get("id"),
            "team_name": c.get("team", {}).get("name"),
            # image
            "photo": c.get("photo"),
        })

    return coaches


# GET PLAYERS
def get_players(team_id, team_name):
    url = f"{BASE_URL}/players?team={team_id}&season={SEASON}"
    res = requests.get(url, headers=HEADERS)
    data = res.json()

    players = []

    for item in data.get("response", []):
        p = item.get("player", {})
        stats = item.get("statistics", [{}])[0]

        games = stats.get("games", {})
        cards = stats.get("cards", {})
        goals = stats.get("goals", {})

        players.append({
            "player_id": p.get("id"),
            "name": p.get("name"),
            "age": p.get("age"),
            "nationality": p.get("nationality"),
            "team_id": team_id,
            "team_name": team_name,
            "position": games.get("position"),
            "appearances": games.get("appearences"),
            "rating": games.get("rating"),
            "goals": goals.get("total"),
            "assists": goals.get("assists"),
            "yellow_cards": cards.get("yellow"),
            "red_cards": cards.get("red")
        })

    return players


# CRAWLER
def crawlData():
    teams, stadiums = get_teams()

    all_players = []
    all_coaches = []
    print(f"Teams: {len(teams)}")

    for i, team in enumerate(teams):
        print(f"[{i+1}/{len(teams)}] {team['team_name']}")
        team_id = team["team_id"]

        try:
            # players
            players = get_players(team_id, team["team_name"])
            all_players.extend(players)

            # coaches
            coaches = get_coaches(team_id)
            all_coaches.extend(coaches)

            time.sleep(2)

        except Exception as e:
            print("Error:", team["team_name"], e)

    return teams, stadiums, all_players, all_coaches


# SAVE FILES
def save(teams, stadiums, players, coaches):
    output_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
    os.makedirs(output_dir, exist_ok=True)

    pd.DataFrame(teams).to_csv(os.path.join(output_dir, "teams.csv"), mode="w", index=False)
    pd.DataFrame(stadiums).to_csv(os.path.join(output_dir, "stadiums.csv"), mode="w", index=False)
    pd.DataFrame(players).to_csv(os.path.join(output_dir, "players.csv"), mode="w", index=False)
    pd.DataFrame(coaches).to_csv(os.path.join(output_dir, "coaches.csv"), mode="w", index=False)

    print("Saved: teams.csv, stadiums.csv, players.csv, coaches.csv")


# Crawl and save data
teams, stadiums, players, coaches = crawlData()
save(teams, stadiums, players, coaches)
