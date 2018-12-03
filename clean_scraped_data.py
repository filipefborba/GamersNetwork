import json
from collections import Counter
from hltv_rating import hltv_rating
import traceback

fp = open('campeonatos_completo.json', 'r')
campeonatos = json.load(fp)

def calculate_hltv(player, rounds):
    try:
        rating = float(hltv_rating(
                    int(rounds),
                    int(player["stats"]["kills"]),
                    int(player["stats"]["deaths"]),
                    int(player["stats"]["killscount"]["1"]),
                    int(player["stats"]["killscount"]["2"]),
                    int(player["stats"]["killscount"]["3"]),
                    int(player["stats"]["killscount"]["4"]),
                    int(player["stats"]["killscount"]["5"])
                ))
        rating = round(rating, 3)
        clean_player = {
            "id": player["id"],
            "teamid": player["teamid"],
            "name" : player["name"],
            "rating" : rating
            }
        return clean_player
    except Exception:
        traceback.print_exc()
        print("Erro em:", player["name"])

def clean_teams(players_list, rounds):
    clean_team = []
    for p in players_list:
        clean_team.append(calculate_hltv(p, rounds))
    return clean_team

def bo3_winner(lst):
    return max(set(lst), key=lst.count)  

data = {}
for campeonato in campeonatos:
    data[campeonato] = {}
    for partida in campeonatos[campeonato]:
        data[campeonato][partida] = {}
        n_mapas = len(campeonatos[campeonato][partida])
        total_mapas = []
        for mapa in range(n_mapas):
            campeonatos_mapa = campeonatos[campeonato][partida][mapa]

            ## Match Winner
            score_team1 = int(campeonatos[campeonato][partida][mapa]["team1"]["score"])
            score_team2 = int(campeonatos[campeonato][partida][mapa]["team2"]["score"])
            rounds = score_team1 + score_team2
            id_team1 = campeonatos[campeonato][partida][mapa]["team1"]["id"]
            id_team2 = campeonatos[campeonato][partida][mapa]["team2"]["id"]
            if score_team1 > score_team2:
                match_winner = id_team1
            else:
                match_winner = id_team2

            match_map = campeonatos[campeonato][partida][mapa]["map"]
            match_id = campeonatos[campeonato][partida][mapa]["id"]

            team1 = campeonatos[campeonato][partida][mapa]["team1"]
            team2 = campeonatos[campeonato][partida][mapa]["team2"]

            clean_team1_players = clean_teams(campeonatos[campeonato][partida][mapa]["team1"]["players"], rounds)
            clean_team2_players = clean_teams(campeonatos[campeonato][partida][mapa]["team2"]["players"], rounds)

            clean_map = {
                "id": match_id,
                "mapa": match_map,
                "winner": match_winner,
                "teams" : {
                    id_team1: {
                        "players": clean_team1_players,
                        "score1": score_team1,
                        "name": team1["name"]
                    },
                    id_team2: {
                        "players": clean_team2_players,
                        "score2": score_team2,
                        "name": team2["name"]
                    }
                }
            }
            total_mapas.append(clean_map)
        if n_mapas > 1:
            winner_list = []
            for m in total_mapas:
                winner_list.append(m["winner"])
            total_winner = bo3_winner(winner_list)
        else:
            total_winner = match_winner
        data[campeonato][partida] = {"winner": total_winner, "maps_played": total_mapas}

with open('clean_scraped_data.json', 'w') as fp:
    json.dump(data, fp)