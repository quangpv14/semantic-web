from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD
import csv
import os
from urllib.parse import quote

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "crawl", "data")
OUTPUT_DIR = os.path.join(BASE_DIR, "rdf")

EX = Namespace("http://semanticweb.org/football/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DBP = Namespace("http://dbpedia.org/resource/")

g = Graph()
g.bind("ex", EX)
g.bind("foaf", FOAF)
g.bind("dbp", DBP)


def make_uri_slug(text):
    return quote(str(text).strip(), safe='')


def safe_int(value):
    try:
        return int(float(value))
    except Exception:
        return None


def safe_float(value):
    try:
        return float(value)
    except Exception:
        return None


def load_csv(filename):
    path = os.path.join(DATA_DIR, filename)
    if not os.path.exists(path):
        return []
    with open(path, encoding="utf-8") as f:
        return list(csv.DictReader(f))


def add_literal(subject, predicate, value, datatype=None):
    if value is None or value == "":
        return
    if datatype is not None:
        g.add((subject, predicate, Literal(value, datatype=datatype)))
    else:
        g.add((subject, predicate, Literal(value)))


leagues = {}
for row in load_csv("leagues.csv"):
    league_id = row.get("id") or row.get("league_id")
    if not league_id:
        continue
    league = EX[f"league/{make_uri_slug(league_id)}"]
    leagues[row.get("name", league_id)] = league

    g.add((league, RDF.type, EX.League))
    add_literal(league, EX.name, row.get("name"))
    add_literal(league, EX.level, row.get("level"))
    add_literal(league, EX.numberOfTeams, safe_int(row.get("numberOfTeams")), XSD.integer)
    add_literal(league, EX.season, row.get("season"))
    add_literal(league, EX.organizer, row.get("organizer"))
    add_literal(league, RDFS.label, row.get("name"))


stadiums = {}
stadiums_by_id = {}
for row in load_csv("stadiums.csv"):
    stadium_id = row.get("stadium_id") or row.get("id")
    name = row.get("stadium_name") or row.get("name")
    if not name:
        continue

    stadium = EX[f"stadium/{make_uri_slug(name)}"]
    stadiums[name] = stadium
    if stadium_id:
        stadiums_by_id[stadium_id] = stadium

    g.add((stadium, RDF.type, EX.Stadium))
    add_literal(stadium, EX.name, name)
    add_literal(stadium, EX.city, row.get("city"))
    add_literal(stadium, EX.address, row.get("address"))
    add_literal(stadium, EX.capacity, safe_int(row.get("capacity")), XSD.integer)
    add_literal(stadium, EX.surface, row.get("surface"))
    add_literal(stadium, EX.image, row.get("image"))
    add_literal(stadium, EX.teamId, stadium_id)
    add_literal(stadium, RDFS.label, name)


coaches = {}
for row in load_csv("coaches.csv"):
    coach_id = row.get("coach_id") or row.get("id")
    name = row.get("name")
    if not name:
        continue

    coach = EX[f"coach/{make_uri_slug(coach_id or name)}"]
    coaches[name] = coach

    g.add((coach, RDF.type, EX.Coach))
    add_literal(coach, EX.name, name)
    add_literal(coach, EX.firstName, row.get("firstname"))
    add_literal(coach, EX.lastName, row.get("lastname"))
    add_literal(coach, EX.age, safe_float(row.get("age")), XSD.decimal)
    add_literal(coach, EX.nationality, row.get("nationality"))
    add_literal(coach, EX.birthDate, row.get("birth_date"))
    add_literal(coach, EX.birthPlace, row.get("birth_place"))
    add_literal(coach, EX.birthCountry, row.get("birth_country"))
    add_literal(coach, EX.height, row.get("height"))
    add_literal(coach, EX.weight, row.get("weight"))
    add_literal(coach, EX.teamId, row.get("team_id"))
    add_literal(coach, EX.teamName, row.get("team_name"))
    add_literal(coach, EX.career, row.get("career"))
    add_literal(coach, EX.photo, row.get("photo"))
    add_literal(coach, RDFS.label, name)


referees = {}
for row in load_csv("referees.csv"):
    referee_id = row.get("referee_id") or row.get("id")
    name = row.get("name")
    if not name:
        continue

    referee = EX[f"referee/{make_uri_slug(referee_id or name)}"]
    referees[name] = referee

    g.add((referee, RDF.type, EX.Referee))
    add_literal(referee, EX.name, name)
    add_literal(referee, EX.matchesOfficiated, safe_int(row.get("matchesOfficiated")), XSD.integer)
    add_literal(referee, EX.certificationLevel, row.get("certificationLevel"))
    add_literal(referee, EX.age, safe_int(row.get("age")), XSD.integer)
    add_literal(referee, RDFS.label, name)


teams = {}
teams_by_id = {}
for row in load_csv("teams.csv"):
    team_id = row.get("team_id") or row.get("id")
    name = row.get("team_name") or row.get("name")
    if not name:
        continue

    team = EX[f"team/{make_uri_slug(name)}"]
    teams[name] = team
    if team_id:
        teams_by_id[team_id] = team

    g.add((team, RDF.type, EX.Team))
    add_literal(team, EX.name, name)
    add_literal(team, EX.country, row.get("country"))
    add_literal(team, EX.founded, safe_int(row.get("founded")), XSD.integer)
    add_literal(team, EX.stadiumId, row.get("stadium_id"))
    add_literal(team, RDFS.label, name)


for row in load_csv("players.csv"):
    player_id = row.get("player_id") or row.get("id")
    name = row.get("name")
    if not player_id or not name:
        continue

    player = EX[f"player/{make_uri_slug(player_id)}"]
    team = None
    if row.get("team_name") in teams:
        team = teams[row["team_name"]]
    elif row.get("team_id") in teams_by_id:
        team = teams_by_id[row.get("team_id")]
    elif row.get("team_name"):
        team = EX[f"team/{make_uri_slug(row['team_name'])}"]

    g.add((player, RDF.type, EX.Player))
    add_literal(player, EX.name, name)
    add_literal(player, EX.age, safe_float(row.get("age")), XSD.decimal)
    add_literal(player, EX.nationality, row.get("nationality"))
    if team:
        g.add((player, EX.playsFor, team))
    add_literal(player, EX.position, row.get("position"))
    add_literal(player, EX.appearances, safe_int(row.get("appearances")), XSD.integer)
    add_literal(player, EX.rating, safe_float(row.get("rating")), XSD.decimal)
    add_literal(player, EX.goals, safe_int(row.get("goals")), XSD.integer)
    add_literal(player, EX.assists, safe_int(row.get("assists")), XSD.integer)
    add_literal(player, EX.yellowCards, safe_int(row.get("yellow_cards")), XSD.integer)
    add_literal(player, EX.redCards, safe_int(row.get("red_cards")), XSD.integer)
    add_literal(player, RDFS.label, name)
    add_literal(player, RDFS.seeAlso, DBP[make_uri_slug(name)])


for row in load_csv("matches.csv"):
    match_id = row.get("id")
    if not match_id:
        continue

    match = EX[f"match/{make_uri_slug(match_id)}"]
    home_team = teams.get(row.get("homeTeam")) if row.get("homeTeam") else None
    away_team = teams.get(row.get("awayTeam")) if row.get("awayTeam") else None
    stadium = stadiums.get(row.get("stadium")) if row.get("stadium") else None
    referee = referees.get(row.get("referee")) if row.get("referee") else None

    g.add((match, RDF.type, EX.Match))
    add_literal(match, EX.matchDate, row.get("matchDate"), XSD.date)
    add_literal(match, EX.dateTime, row.get("dateTime"))
    if home_team:
        g.add((match, EX.homeTeam, home_team))
    if away_team:
        g.add((match, EX.awayTeam, away_team))
    if stadium:
        g.add((match, EX.stadium, stadium))
    if referee:
        g.add((match, EX.referee, referee))
    add_literal(match, EX.score, row.get("score"))
    add_literal(match, EX.formation, row.get("formation"))
    add_literal(match, EX.round, row.get("round"))
    add_literal(match, EX.result, row.get("result"))
    add_literal(match, RDFS.label, f"{row.get('homeTeam', '')} vs {row.get('awayTeam', '')}")


os.makedirs(OUTPUT_DIR, exist_ok=True)
g.serialize(destination=os.path.join(OUTPUT_DIR, "football.ttl"), format="turtle")
