import pandas as pd

df = pd.read_csv('collect_matches.csv')
new_data = []
result_map = {
    'W': 'Win',
    'L': 'Loss',
    'D': 'Draw'
}

for i, row in df.iterrows():
    if row['venue'] == 'Home':
        home = row['team']
        away = row['opponent']
    else:
        home = row['opponent']
        away = row['team']
    
    score = f"{int(row['gf'])}-{int(row['ga'])}"
    
    new_data.append({
        'id': i + 1,
        'matchDate': row['date'],
        'dateTime': row['day'] + ' ' + row['time'],
        'homeTeam': home,
        'awayTeam': away,
        'formation': row['formation'],
        'referee': row['referee'],
        'score': score,
        'round': row['round'],
        'result': result_map.get(row['result'], row['result'])
    })

new_df = pd.DataFrame(new_data)
new_df.to_csv('../data/matches.csv', index=False)