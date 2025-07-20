import itertools
import random

def generate_round_robin(teams, double):
    matches = []
    rounds = list(itertools.combinations(teams, 2))
    if double:
        rounds += [(b, a) for a, b in rounds]
    for t1, t2 in rounds:
        matches.append({"team1": t1, "team2": t2, "score1": None, "score2": None})
    return matches

def generate_knockout(teams):
    random.shuffle(teams)
    matches = []
    while len(teams) > 1:
        t1 = teams.pop()
        t2 = teams.pop()
        matches.append({"team1": t1, "team2": t2, "score1": None, "score2": None})
    return matches
