import json

fp = open('gamers_network_with_rating.json', 'r')
players = json.load(fp)

clean_players = {}

for p in players:
    clean_players[p] = {
        "player_friends": players[p]["player_friends"],
        "matches": players[p]["infos"]["matches"],
        "mean_rating": players[p]["infos"]["mean_rating"],
        "player_id": players[p]["infos"]["player_info"]["player_id"],
        "nick": players[p]["infos"]["player_info"]["nick"]
    }

with open('gn.json', 'w') as fp:
    json.dump(clean_players, fp)
            