# 1. List all players with their names and nationalities
def QUERY_ALL_PLAYERS():
    return """
PREFIX ex: <http://semanticweb.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?nationality ?teamName ?goals
FROM <http://semanticweb.org/football>
WHERE {
  ?player a ex:Player ;
          ex:name ?name ;
          ex:nationality ?nationality ;
          ex:playsFor ?team ;
          ex:goals ?goals .
  ?team rdfs:label ?teamName .
  FILTER(?goals >= 5)
}
ORDER BY DESC(?goals) ?name
"""

# 2. List all matches with score and date
def QUERY_ALL_MATCHES():
    return """
PREFIX ex: <http://semanticweb.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

SELECT ?homeTeamName ?awayTeamName ?score ?date
FROM <http://semanticweb.org/football>
WHERE {
  ?match a ex:Match ;
         ex:homeTeam ?homeTeam ;
         ex:awayTeam ?awayTeam ;
         ex:score ?score ;
         ex:matchDate ?date .

  ?homeTeam rdfs:label ?homeTeamName .
  ?awayTeam rdfs:label ?awayTeamName .

  BIND(xsd:integer(STRBEFORE(?score, "-")) AS ?homeGoals)
  BIND(xsd:integer(STRAFTER(?score, "-")) AS ?awayGoals)
  BIND(ABS(?homeGoals - ?awayGoals) AS ?diff)
  FILTER(?diff >= 3)
}
ORDER BY DESC(?diff)
"""

# 3. Club details for Manchester United

def QUERY_CLUB_DETAILS():
    return """
PREFIX ex: <http://semanticweb.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT DISTINCT ?teamName ?teamCountry ?stadiumName ?stadiumCapacity 
                ?coachName ?coachAge ?coachNationality
FROM <http://semanticweb.org/football>
WHERE {
  ?team a ex:Team ;
        ex:name "Manchester United" ;
        rdfs:label ?teamName ;
        ex:country ?teamCountry ;
        ex:stadiumId ?stadiumId .

  ?stadium ex:teamId ?stadiumId ;
           rdfs:label ?stadiumName ;
           ex:capacity ?stadiumCapacity .

  ?coach ex:teamName "Manchester United" ;
         ex:name ?coachName ;
         ex:age ?coachAge ;
         ex:nationality ?coachNationality .
}
"""

# 4. List all referees with age and certification
def QUERY_REFEREES():
    return """
PREFIX ex: <http://semanticweb.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?age ?level ?matchesOfficiated ?matchLabel ?stadiumName
WHERE {
  ?referee a ex:Referee ;
           ex:name ?name ;
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
def QUERY_PLAYER_STATS_JOIN():
    return """
PREFIX ex: <http://semanticweb.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?name ?goals ?assists ?appearances
WHERE {
  ?player a ex:Player ;
          ex:name ?name ;
          ex:goals ?goals ;
          ex:assists ?assists ;
          ex:appearances ?appearances .
}
ORDER BY DESC(?goals)
"""

# 5. Join matches with referee names and stadiums
def QUERY_MATCH_REFEREES_JOIN():
    return """
PREFIX ex: <http://semanticweb.org/football/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?label ?score ?date ?refereeName ?stadiumName ?stadiumCapacity
WHERE {
  ?match a ex:Match ;
         rdfs:label ?label ;
         ex:referee ?referee ;
         ex:stadium ?stadium ;
         ex:score ?score ;
         ex:matchDate ?date .
  ?referee rdfs:label ?refereeName .
  ?stadium rdfs:label ?stadiumName ;
           ex:capacity ?stadiumCapacity .
}
ORDER BY ?date ?label
"""

# Dictionary of all queries for easy access
QUERIES = {
    "all_players": QUERY_ALL_PLAYERS(),
    "matches": QUERY_ALL_MATCHES(),
    "club_details": QUERY_CLUB_DETAILS(),
    "referees": QUERY_REFEREES(),
    "player_stats_join": QUERY_PLAYER_STATS_JOIN(),
    "match_referees_join": QUERY_MATCH_REFEREES_JOIN(),
}

if __name__ == "__main__":
    print("Available SPARQL queries:")
    for key in QUERIES.keys():
        print(f"- {key}")
