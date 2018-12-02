import requests
import json
import re
from bs4 import BeautifulSoup, SoupStrainer

def get_partida_html(camp_id, partida_id):
    url = "https://gamersclub.com.br/campeonatos/csgo/{}/partida/{}".format(camp_id, partida_id)
    headers = {
        'Cookie': "__utma=203582342.232122176.1489463720.1497671483.1497749677.12; _ga=GA1.3.232122176.1489463720; rdtrk=%7B%22id%22%3A%2219e6bdb6-ab8f-4549-bf65-45ff0c86e846%22%7D; intercom-lou-gp4gdmdo=1; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiMjAzNTgyMzQyLjE0ODk0NjM3MjEuMS4xLnV0bWNzcj0oZGlyZWN0KXx1dG1jY249KGRpcmVjdCl8dXRtY21kPShub25lKSIsImV4dHJhX3BhcmFtcyI6e319LCJjdXJyZW50X3Nlc3Npb24iOnsidmFsdWUiOiJodHRwczovL2dhbWVyc2NsdWIuY29tLmJyLyIsImV4dHJhX3BhcmFtcyI6e319LCJjcmVhdGVkX2F0IjoxNTE4MTM1OTYwMzAwfQ==; __cfduid=dfaae443a782f1d6d0b715bebbb0338321522639930; SL_C_23361dd035530_KEY=a14d3638cda988422792e3613234743b983fdd9e; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102=session_91c09cdd-f616-4e12-9599-8aad4f09988d; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102%2Fc3b2fd43f122359ddf0a576a7d4d75ab74b4d92f9feb92c94eeb2406a6d36192=session_91c09cdd-f616-4e12-9599-8aad4f09988d; SL_C_23361dd035530_VID=Nm59QhW-6TYP; SL_C_23361dd035530_SID=hMyy703pm5eY; gclubsess=fe6dc36080d6083b0e1060909e4d5a51218b6dd8; _gid=GA1.3.168545321.1543697640; _fbp=fb.2.1543697640249.576304885",
        'Referer': "https://gamersclub.com.br/campeonatos/csgo/846/",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers)

    partida_html = response.text
    soup = BeautifulSoup(partida_html, features="lxml")

    total_partidas = []
    final_players = []

    matches_ids = []
    for mi in soup.find_all("div", "team-map-text-info"):
        matches_ids.append(mi.get_text().replace(" ", "").split("\n")[-1:][0].split("#")[-1:][0])

    scores = []
    for s in soup.find_all("span", "score-circle"):
        scores.append(s.get_text())

    maps = soup.find("div", "map").get_text().replace(" ", "").split("\n")
    maps = maps[3].split(",")
    if not maps[0].startswith("de_"):
        return total_partidas

    teams_ids = []
    for t in soup.find_all("a", href=re.compile("gamersclub.com.br/time/"))[-2:]:
        teams_ids.append(t.get('href').split("/")[-1:][0])

    teams_names = []
    for n in soup.find_all("h4", "team-name"):
        teams_names.append(n.get_text().replace(" ", "").split("\n")[1].split("KDR")[0])

    players_stats = []
    players_ids = []
    for stats in soup.find_all("tr"):
        link_ids = stats.find_all("a", "friend")
        for id in link_ids:
            p_id = id.get("href").split("/")[-1:][0]
            players_ids.append(p_id)
        p = stats.get_text().replace(" ", "").split("\n")
        p = [x for x in p if x != ""]
        if p not in players_stats:
            players_stats.append(p)
    
    if players_stats:
        headers = players_stats.pop(0)
        headers.insert(1, "Nivel")

        team_players = []
        for i in range(len(players_stats)):
            temp_player = {"stats": {}}
            for j in range(len(players_stats[i])):
                temp_player["id"] = players_ids[i]
                temp_player["stats"][headers[j]] = players_stats[i][j]
            team_players.append(temp_player)

        for p in range(len(team_players)):
            player = {
                "id": None,
                "name": None,
                "teamid": None,
                "level": None,
                "medal": None,
                "stats": {
                    "id": None,
                    "killscount": {
                        "1": None,
                        "2": None,
                        "3": None,
                        "4": None,
                        "5": None
                    },
                    "assists": None,
                    "kills": None,
                    "hs": None,
                    "deaths": None,
                    "damage": None,
                    "hits": None,
                    "blinded": None,
                    "blindedtime": None,
                    "planted": None,
                    "defused": None,
                    "mvp": None,
                    "tk": None,
                    "clutchs": None
                }
            }

            if ((p % 10) <= 4):
                team = teams_ids[0]
            else:
                team = teams_ids[1]

            player["id"] = team_players[p]["id"]
            player["teamid"] = team
            player["name"] = team_players[p]["stats"]["Jogador"]
            player["level"] = team_players[p]["stats"]["Nivel"]
            player["stats"]["id"] = team_players[p]["id"]
            player["stats"]["killscount"]["1"] = team_players[p]["stats"]["1K"]
            player["stats"]["killscount"]["2"] = team_players[p]["stats"]["2K"]
            player["stats"]["killscount"]["3"] = team_players[p]["stats"]["3K"]
            player["stats"]["killscount"]["4"] = team_players[p]["stats"]["4K"]
            player["stats"]["killscount"]["5"] = team_players[p]["stats"]["5K"]
            player["stats"]["assists"] = team_players[p]["stats"]["A"]
            player["stats"]["kills"] = team_players[p]["stats"]["K"]
            player["stats"]["hs"] = team_players[p]["stats"]["HS"]
            player["stats"]["deaths"] = team_players[p]["stats"]["D"]
            player["stats"]["planted"] = team_players[p]["stats"]["BP"]
            player["stats"]["defused"] = team_players[p]["stats"]["BD"]
            player["stats"]["clutchs"] = team_players[p]["stats"]["1vsX"]
            final_players.append(player)
    else:
        return total_partidas

    best_of = soup.find("div", "best-of").get_text().replace(" ", "").split("\n")
    if best_of[2] == "Melhorde3":
        for i in range(len(matches_ids)):
            partida = {
                "id": None,
                "map": None,
                "team1": {
                    "players": []
                },
                "team2": {
                    "players": []
                },
                "demo": None,
                "rounds": None,
                "clutchs": None
            }
            partida["id"] = matches_ids[i]
            partida["map"] = maps[i]
            partida["team1"]["name"] = teams_names[0]
            partida["team2"]["name"] = teams_names[1]
            partida["team1"]["id"] = teams_ids[0]
            partida["team2"]["id"] = teams_ids[1]
            partida["team1"]["score"] = scores[i*2]
            partida["team2"]["score"] = scores[(i*2)+1]
            for j in range(len(final_players)//len(matches_ids)):
                indice = (((len(final_players)//len(matches_ids)) * i) + j)
                if ((indice % 10) <= 4):
                    team = "team1"
                else:
                    team = "team2"
                partida[team]["players"].append(final_players[indice])
            total_partidas.append(partida)
        return total_partidas

    else:
        partida = {
                "id": None,
                "map": None,
                "team1": {
                    "players": []
                },
                "team2": {
                    "players": []
                },
                "demo": None,
                "rounds": None,
                "clutchs": None
            }
        partida["id"] = matches_ids[0]
        partida["map"] = maps[0]
        partida["team1"]["name"] = teams_names[0]
        partida["team2"]["name"] = teams_names[1]
        partida["team1"]["id"] = teams_ids[0]
        partida["team2"]["id"] = teams_ids[1]
        partida["team1"]["score"] = scores[0]
        partida["team2"]["score"] = scores[1]
        for j in range(len(final_players)):
            if ((j % 10) <= 4):
                team = "team1"
            else:
                team = "team2"
            partida[team]["players"].append(final_players[j])
        total_partidas.append(partida)
        return total_partidas
