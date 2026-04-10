from rdflib import Graph, Namespace, Literal, RDF, RDFS, XSD, URIRef
import csv
import os
from urllib.parse import quote

# Define namespaces
EX = Namespace("http://example.org/football/")
FOAF = Namespace("http://xmlns.com/foaf/0.1/")
DBP = Namespace("http://dbpedia.org/resource/")  # External links for 5-star compliance

g = Graph()
g.bind("ex", EX)
g.bind("foaf", FOAF)
g.bind("dbp", DBP)

# Helper function to convert text to valid URI slug
def make_uri_slug(text):
    """Convert text to URL-safe slug for URI"""
    return quote(text.strip(), safe='')

# ==================== LOAD LEAGUES ====================
leagues = {}  # Map by name
if os.path.exists("crawl/data/leagues.csv"):
    with open("crawl/data/leagues.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            league = EX["league/" + row["id"]]
            leagues[row["name"]] = league  # Map by name, not ID
            
            g.add((league, RDF.type, EX.League))
            g.add((league, EX.name, Literal(row["name"])))
            g.add((league, EX.level, Literal(row["level"])))
            g.add((league, EX.numberOfTeams, Literal(int(row["numberOfTeams"]))))
            g.add((league, EX.season, Literal(row["season"])))
            g.add((league, EX.organizer, Literal(row["organizer"])))
            g.add((league, RDFS.label, Literal(row["name"])))

# ==================== LOAD STADIUMS ====================
stadiums = {}  # Map by name
if os.path.exists("crawl/data/stadiums.csv"):
    with open("crawl/data/stadiums.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            stadium_slug = make_uri_slug(row["name"])
            stadium = EX["stadium/" + stadium_slug]
            stadiums[row["name"]] = stadium  # Map by name, not ID
            
            g.add((stadium, RDF.type, EX.Stadium))
            g.add((stadium, EX.name, Literal(row["name"])))
            g.add((stadium, EX.location, Literal(row["location"])))
            g.add((stadium, EX.capacity, Literal(int(row["capacity"]))))
            g.add((stadium, EX.builtYear, Literal(int(row["builtYear"]))))
            g.add((stadium, EX.owner, Literal(row["owner"])))
            g.add((stadium, EX.surfaceType, Literal(row["surfaceType"])))
            g.add((stadium, RDFS.label, Literal(row["name"])))

# ==================== LOAD COACHES ====================
coaches = {}  # Map by name
if os.path.exists("crawl/data/coaches.csv"):
    with open("crawl/data/coaches.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            coach_slug = make_uri_slug(row["name"])
            coach = EX["coach/" + coach_slug]
            coaches[row["name"]] = coach  # Map by name, not ID
            
            g.add((coach, RDF.type, EX.Coach))
            g.add((coach, EX.name, Literal(row["name"])))
            g.add((coach, EX.experienceYears, Literal(int(row["experienceYears"]))))
            g.add((coach, EX.currentTeam, Literal(row["currentTeam"])))
            g.add((coach, EX.formationPreference, Literal(row["formationPreference"])))
            g.add((coach, FOAF.name, Literal(row["name"])))

# ==================== LOAD REFEREES ====================
referees = {}  # Map by name
if os.path.exists("crawl/data/referees.csv"):
    with open("crawl/data/referees.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            ref_slug = make_uri_slug(row["name"])
            referee = EX["referee/" + ref_slug]
            referees[row["name"]] = referee  # Map by name, not ID
            
            g.add((referee, RDF.type, EX.Referee))
            g.add((referee, EX.name, Literal(row["name"])))
            g.add((referee, EX.matchesOfficiated, Literal(int(row["matchesOfficiated"]))))
            g.add((referee, EX.certificationLevel, Literal(row["certificationLevel"])))
            g.add((referee, EX.age, Literal(int(row["age"]))))
            g.add((referee, FOAF.name, Literal(row["name"])))

# ==================== LOAD TEAMS ====================
teams = {}  # Map by name
if os.path.exists("crawl/data/teams.csv"):
    with open("crawl/data/teams.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            team_slug = make_uri_slug(row["name"])
            team = EX["team/" + team_slug]
            teams[row["name"]] = team
            
            g.add((team, RDF.type, EX.Team))
            g.add((team, EX.name, Literal(row["name"])))
            g.add((team, EX.foundedYear, Literal(int(row["foundedYear"]))))
            g.add((team, EX.country, Literal(row["country"])))
            g.add((team, EX.numberOfPlayers, Literal(int(row["numberOfPlayers"]))))
            g.add((team, RDFS.label, Literal(row["name"])))
            
            # Link to stadium, coach, league by name
            if row["homeStadium"] in stadiums:
                g.add((team, EX.homeStadium, stadiums[row["homeStadium"]]))
            
            if row["coach"] in coaches:
                g.add((team, EX.coach, coaches[row["coach"]]))
            
            if row["league"] in leagues:
                g.add((team, EX.league, leagues[row["league"]]))

# ==================== LOAD PLAYERS ====================
if os.path.exists("crawl/data/players.csv"):
    with open("crawl/data/players.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            player = EX["player/" + row["id"]]
            stat = EX["stat/" + row["id"]]
            
            # Get team by name from teams mapping
            team = teams.get(row["team"], EX["team/" + make_uri_slug(row["team"])])
            
            # Player
            g.add((player, RDF.type, EX.Player))
            g.add((player, EX.name, Literal(row["name"])))
            g.add((player, EX.dateOfBirth, Literal(row["dob"], datatype=XSD.date)))
            g.add((player, EX.nationality, Literal(row["nationality"])))
            g.add((player, EX.position, Literal(row["position"])))
            g.add((player, EX.height, Literal(float(row["height"]))))
            g.add((player, EX.weight, Literal(float(row["weight"]))))
            g.add((player, EX.playsFor, team))
            g.add((player, EX.hasStatistic, stat))
            g.add((player, FOAF.name, Literal(row["name"])))
            g.add((player, RDFS.label, Literal(row["name"])))
            
            # Link to DBpedia for 5-star compliance (use URL-encoded name)
            player_slug = make_uri_slug(row["name"])
            g.add((player, RDFS.seeAlso, DBP[player_slug]))
            
            # Statistic
            g.add((stat, RDF.type, EX.Statistic))
            g.add((stat, EX.player, player))
            g.add((stat, EX.goals, Literal(int(row["goals"]))))
            g.add((stat, EX.assists, Literal(int(row["assists"]))))
            g.add((stat, EX.appearances, Literal(int(row["appearances"]))))
            g.add((stat, EX.yellowCards, Literal(int(row["yellowCards"]))))
            g.add((stat, EX.redCards, Literal(int(row["redCards"]))))
            g.add((stat, EX.minutesPlayed, Literal(int(row["minutesPlayed"]))))

# ==================== LOAD MATCHES ====================
if os.path.exists("crawl/data/matches.csv"):
    with open("crawl/data/matches.csv", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            match = EX["match/" + row["id"]]
            
            # Get entities by name from mapping dictionaries
            home_team = teams.get(row["homeTeam"], EX["team/" + make_uri_slug(row["homeTeam"])])
            away_team = teams.get(row["awayTeam"], EX["team/" + make_uri_slug(row["awayTeam"])])
            stadium = stadiums.get(row["stadium"], EX["stadium/" + make_uri_slug(row["stadium"])])
            referee = referees.get(row["referee"], EX["referee/" + make_uri_slug(row["referee"])])
            
            g.add((match, RDF.type, EX.Match))
            g.add((match, EX.matchDate, Literal(row["matchDate"], datatype=XSD.date)))
            g.add((match, EX.homeTeam, home_team))
            g.add((match, EX.awayTeam, away_team))
            g.add((match, EX.stadium, stadium))
            g.add((match, EX.referee, referee))
            g.add((match, EX.score, Literal(row["score"])))
            g.add((match, EX.competition, Literal(row["competition"])))
            g.add((match, RDFS.label, Literal(f"{row['homeTeam']} vs {row['awayTeam']}")))

# Save
os.makedirs("rdf", exist_ok=True)
g.serialize(destination="rdf/football.ttl", format="turtle")
