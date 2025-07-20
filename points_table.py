from collections import defaultdict
import json

def load_data():
    with open("tournament_data.json", 'r') as f:
        return json.load(f)

def calculate_points_table():
    data = load_data()
    table = defaultdict(lambda: {"MP": 0, "W": 0, "D": 0, "L": 0, "GF": 0, "GA": 0, "GD": 0, "Pts": 0})
    for match in data['matches']:
        if match['score1'] is None:
            continue
        t1, t2 = match['team1'], match['team2']
        s1, s2 = match['score1'], match['score2']
        table[t1]['MP'] += 1
        table[t2]['MP'] += 1
        table[t1]['GF'] += s1
        table[t1]['GA'] += s2
        table[t2]['GF'] += s2
        table[t2]['GA'] += s1

        if s1 > s2:
            table[t1]['W'] += 1
            table[t2]['L'] += 1
            table[t1]['Pts'] += 2
        elif s1 < s2:
            table[t2]['W'] += 1
            table[t1]['L'] += 1
            table[t2]['Pts'] += 2
        else:
            table[t1]['D'] += 1
            table[t2]['D'] += 1
            table[t1]['Pts'] += 1
            table[t2]['Pts'] += 1

    for team in table:
        table[team]['GD'] = table[team]['GF'] - table[team]['GA']
    return table

def show_points_table():
    table = calculate_points_table()
    sorted_teams = sorted(table.items(), key=lambda x: (-x[1]['Pts'], -x[1]['GD'], -x[1]['GF']))
    print("\nPoints Table:")
    print(f"{'Team':<15} MP  W  D  L  GF  GA  GD  Pts")
    for team, stats in sorted_teams:
        print(f"{team:<15} {stats['MP']:>2} {stats['W']:>2} {stats['D']:>2} {stats['L']:>2} "
              f"{stats['GF']:>3} {stats['GA']:>3} {stats['GD']:>3} {stats['Pts']:>3}")
    return [team for team, _ in sorted_teams]
