import json
from collections import Counter
import traceback
import numpy as np

fp = open('clean_scraped_data.json', 'r')
campeonatos = json.load(fp)

def create_player(player_id, current_team, name):
    new_player = { player_id : {
                                "current_team": current_team,
                                "name": name,
                                "mean_rating" : 0,
                                "maps_played" : 0,
                                "ratings" : [],
                                "teams": [],
                                "team_mates": {},
                                "played_with" : []
                                }
                            }
    return new_player

players = {}
for campeonato in campeonatos:
    for partida in campeonatos[campeonato]:
        for mapa in range(len(campeonatos[campeonato][partida]["maps_played"])):
            for time in campeonatos[campeonato][partida]["maps_played"][mapa]["teams"]:
                for jogador in campeonatos[campeonato][partida]["maps_played"][mapa]["teams"][time]["players"]:
                    played_with = [player['id'] for player in campeonatos[campeonato][partida]["maps_played"][mapa]["teams"][time]["players"]]              
                    player_id = jogador["id"]

                    if player_id in players:
                        players[player_id]["maps_played"] += 1
                        players[player_id]["played_with"] += played_with
                        players[player_id]["ratings"].append(jogador["rating"])
                        players[player_id]["mean_rating"] = np.mean(players[player_id]["ratings"])


                        if time not in players[player_id]["teams"]:
                            players[player_id]["teams"].append(time)
                        players[player_id]["team_mates"] = Counter([x for x in players[player_id]["played_with"] if x != player_id])

                    else:
                        novo_jogador = create_player(player_id, time, jogador["name"])
                        novo_jogador[player_id]["maps_played"] += 1
                        novo_jogador[player_id]["ratings"].append(jogador["rating"])
                        novo_jogador[player_id]["teams"].append(time)
                        novo_jogador[player_id]["played_with"] += played_with
                        novo_jogador[player_id]["team_mates"] = Counter([x for x in novo_jogador[player_id]["played_with"] if x != player_id])
                        
                        players.update(novo_jogador)



with open('network_cleaned_data.json', 'w') as fp:
    json.dump(players, fp)