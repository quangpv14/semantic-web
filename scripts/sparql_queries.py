# 1. List all players with their names and nationalities
QUERY_ALL_PLAYERS = """
PREFIX ex: <http://example.org/football/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?nationality ?teamName ?goals ?assists
WHERE {
  ?player a ex:Player ;
          foaf:name ?name ;
          ex:nationality ?nationality ;
          ex:playsFor ?team ;
          ex:hasStatistic ?stat .
  ?team rdfs:label ?teamName .
  ?stat ex:goals ?goals ;
        ex:assists ?assists .
  FILTER(?goals >= 10)
}
ORDER BY DESC(?goals) ?name
"""

# 2. List all matches with score and date
QUERY_ALL_MATCHES = """
PREFIX ex: <http://example.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?homeTeamName ?awayTeamName ?score ?refereeName ?stadiumName ?date
WHERE {
  ?match a ex:Match ;
         rdfs:label ?label ;
         ex:homeTeam ?homeTeam ;
         ex:awayTeam ?awayTeam ;
         ex:score ?score ;
         ex:matchDate ?date ;
         ex:referee ?referee ;
         ex:stadium ?stadium .
  ?homeTeam rdfs:label ?homeTeamName .
  ?awayTeam rdfs:label ?awayTeamName .
  ?referee foaf:name ?refereeName .
  ?stadium rdfs:label ?stadiumName .
}
ORDER BY ?date
"""

# 3. List all referees with age and certification
QUERY_REFEREES = """
PREFIX ex: <http://example.org/football/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?age ?level ?matchesOfficiated ?matchLabel ?stadiumName
WHERE {
  ?referee a ex:Referee ;
           foaf:name ?name ;
           ex:age ?age ;
           ex:certificationLevel ?level ;
           ex:matchesOfficiated ?matchesOfficiated .
  ?match ex:referee ?referee ;
         rdfs:label ?matchLabel ;
         ex:stadium ?stadium .
  ?stadium rdfs:label ?stadiumName .
}
ORDER BY ?name ?matchLabel
"""

# 4. Join players with their statistics
QUERY_PLAYER_STATS_JOIN = """
PREFIX ex: <http://example.org/football/>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?name ?goals ?assists ?appearances
WHERE {
  ?player a ex:Player ;
          foaf:name ?name ;
          ex:hasStatistic ?stat .
  ?stat ex:goals ?goals ;
        ex:assists ?assists ;
        ex:appearances ?appearances .
}
ORDER BY DESC(?goals)
"""

# 5. Join matches with referee names and stadiums
QUERY_MATCH_REFEREES_JOIN = """
PREFIX ex: <http://example.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX foaf: <http://xmlns.com/foaf/0.1/>

SELECT ?label ?score ?date ?refereeName ?stadiumName ?stadiumCapacity
WHERE {
  ?match a ex:Match ;
         rdfs:label ?label ;
         ex:homeTeam ?homeTeam ;
         ex:awayTeam ?awayTeam ;
         ex:score ?score ;
         ex:matchDate ?date ;
         ex:referee ?referee ;
         ex:stadium ?stadium .
  ?homeTeam rdfs:label ?homeTeamName .
  ?awayTeam rdfs:label ?awayTeamName .
  ?referee foaf:name ?refereeName .
  ?stadium rdfs:label ?stadiumName ;
           ex:capacity ?stadiumCapacity .
}
ORDER BY ?date ?label
"""

# Dictionary of all queries for easy access
QUERIES = {
    "all_players": QUERY_ALL_PLAYERS,
    "matches": QUERY_ALL_MATCHES,
    "referees": QUERY_REFEREES,
    "player_stats_join": QUERY_PLAYER_STATS_JOIN,
    "match_referees_join": QUERY_MATCH_REFEREES_JOIN,
}

if __name__ == "__main__":
    print("Available SPARQL queries:")
    for key in QUERIES.keys():
        print(f"- {key}")
