import json
from collections import Counter
from hltv_rating import hltv_rating

fp = open('gamers_network_with_rating.json', 'r')
players = json.load(fp)

data = {}

for player in players:
    played_with = []
    data[player] = {
        "player_info": {
            "nick": players[player]["infos"]["player_info"]["nick"],
            "level": players[player]["infos"]["player_info"]["level"],
            "reputation": players[player]["infos"]["player_info"]["reputation"],
            "subscription": players[player]["infos"]["player_info"]["subscription"]["type"] if players[player]["infos"]["player_info"]["subscription"] else None
            },
        "friends": [friend.replace("https://gamersclub.com.br/jogador/", "") for friend in players[player]["player_friends"]],
        "matches": {},
        "played_with": None
    }

    matches = players[player]["infos"]["matches"]
    for match in matches:
        data[player]["matches"].update({match: {"duration": matches[match]["duration"], "map": matches[match]["map"], "winner": matches[match]["winner"], "team_a_score": matches[match]["team_a"]["score"], "team_a": {}, "team_b_score": matches[match]["team_b"]["score"], "team_b": {}}})
        
        players_a = players[player]["infos"]["matches"][match]["team_a"]["players"]
        for player_a in players_a:
            if player in players_a:
                played_with.append(player_a)
            try:
                data[player]["matches"][match]["team_a"].update({player_a: {"nick": players_a[player_a][player_a]["infos"][0],
                                                                        "kill": players_a[player_a][player_a]["infos"][1],
                                                                        "death": players_a[player_a][player_a]["infos"][3],
                                                                        "kdd": players_a[player_a][player_a]["infos"][4],
                                                                        "kdr": players_a[player_a][player_a]["infos"][7],
                                                                        "adr": players_a[player_a][player_a]["infos"][8],
                                                                        "points": players_a[player_a][player_a]["infos"][9],
                                                                        "clutchs": players_a[player_a][player_a]["infos"][19],
                                                                        "fk": players_a[player_a][player_a]["infos"][18],
                                                                        "rating": round(hltv_rating(int(players_a[player_a][player_a]["infos"][20]), int(players_a[player_a][player_a]["infos"][1]), 
                                                                                                int(players_a[player_a][player_a]["infos"][3]), int(players_a[player_a][player_a]["infos"][13]), 
                                                                                                int(players_a[player_a][player_a]["infos"][14]), int(players_a[player_a][player_a]["infos"][15]), 
                                                                                                int(players_a[player_a][player_a]["infos"][16]), int(players_a[player_a][player_a]["infos"][17])), 4)
                                                                        }})
            except:
                print("An exception occurred with match {} and user {}".format(match, player_a))
            
            
        players_b = players[player]["infos"]["matches"][match]["team_b"]["players"]
        for player_b in players_b:
            if player in players_b:
                played_with.append(player_b)
            try:
                data[player]["matches"][match]["team_b"].update({player_b: {"nick": players_b[player_b][player_b]["infos"][0],
                                                                            "kill": players_b[player_b][player_b]["infos"][1],
                                                                            "death": players_b[player_b][player_b]["infos"][3],
                                                                            "kdd": players_b[player_b][player_b]["infos"][4],
                                                                            "kdr": players_b[player_b][player_b]["infos"][7],
                                                                            "adr": players_b[player_b][player_b]["infos"][8],
                                                                            "points": players_b[player_b][player_b]["infos"][9],
                                                                            "clutchs": players_b[player_b][player_b]["infos"][19],
                                                                            "fk": players_b[player_b][player_b]["infos"][18],
                                                                            "rating": round(hltv_rating(int(players_b[player_b][player_b]["infos"][20]), int(players_b[player_b][player_b]["infos"][1]), 
                                                                                                    int(players_b[player_b][player_b]["infos"][3]), int(players_b[player_b][player_b]["infos"][13]), 
                                                                                                    int(players_b[player_b][player_b]["infos"][14]), int(players_b[player_b][player_b]["infos"][15]), 
                                                                                                    int(players_b[player_b][player_b]["infos"][16]), int(players_b[player_b][player_b]["infos"][17])), 4)
                                                                            }})
            except:
                print("An exception occurred with match {} and user {}".format(match, player_b))
        break
    data[player]["played_with"] = Counter([x for x in played_with if x != player])
    break

with open('test_clean_data.json', 'w') as fp:
    json.dump(data, fp)