import json

data_file = "tournament_data.json"

def load_data():
    with open(data_file, 'r') as f:
        return json.load(f)

def save_data(data):
    with open(data_file, 'w') as f:
        json.dump(data, f, indent=4)

def enter_results():
    data = load_data()
    pending = [m for m in data['matches'] if m['score1'] is None]
    if not pending:
        print("All matches completed.")
        return
    print(f"{len(pending)} match(es) pending.")
    for match in pending:
        t1, t2 = match['team1'], match['team2']
        print(f"{t1} vs {t2}")
        s1 = int(input(f"{t1} score: "))
        s2 = int(input(f"{t2} score: "))
        match['score1'] = s1
        match['score2'] = s2
    save_data(data)
