import json
import re
import requests
from bs4 import BeautifulSoup, SoupStrainer

def get_match_by_html(camp_id, pag_id):
    #pagina = https://gamersclub.com.br/campeonatos/csgo/846/partida/66817

    url = "https://gamersclub.com.br/campeonatos/csgo/{}/partida/{}".format(camp_id, pag_id)

    headers = {
        'Cookie': "__cfduid=daa46fdf071f015d3e0aa50c2874688ff1534266040; _ga=GA1.3.1588820037.1538761089; SL_C_23361dd035530_KEY=a14d3638cda988422792e3613234743b983fdd9e; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102=session_57ed498d-d875-4902-9be5-a2f04edd3693; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102%2Fc3b2fd43f122359ddf0a576a7d4d75ab74b4d92f9feb92c94eeb2406a6d36192=session_57ed498d-d875-4902-9be5-a2f04edd3693; gclubsess=9969960cdda75b9dedeb7af242495c14ffc135e4; _gid=GA1.3.1431837867.1543524480",
        'Referer': "https://gamersclub.com.br/campeonatos/csgo/846",
        'cache-control': "no-cache",
        'Postman-Token': "918ccadf-a7e8-4d54-b672-e3cd1026ecae"
        }

    response = requests.request("GET", url, headers=headers)
    pagina = response.text
    pagina_id = str(pag_id)
    partida = {
        pagina_id: {
            "id": pagina_id,
            "team1": {
                "players": []
            },
            "team2": {
                "players": []
            },
        }
    }

    soup = BeautifulSoup(pagina, features="lxml")

    best_of = soup.find("div", "best-of").get_text().replace(" ", "").split("\n")
    if best_of[2] == "Melhorde3":
        return "BO3"

    teams = soup.find_all("a", href=re.compile("gamersclub.com.br/time/"))[-2:]
    teams_links = []
    for t in teams:
        teams_links.append(t.get('href'))
    partida[pagina_id]["team1"]["link"] = teams_links[0]
    partida[pagina_id]["team2"]["link"] = teams_links[1]

    team_names = soup.find_all("h4", "team-name")
    team_names_list = []
    for n in team_names:
        team_names_list.append(n.get_text().replace(" ", "").split("\n"))
    partida[pagina_id]["team1"]["name"] = team_names_list[0][1]
    partida[pagina_id]["team2"]["name"] = team_names_list[1][1]

    score_1 = soup.find("div", id="matchscore1").find("span").get_text()
    partida[pagina_id]["team1"]["score"] = score_1
    score_2 = soup.find("div", id="matchscore2").find("span").get_text()
    partida[pagina_id]["team1"]["score"] = score_2

    map = soup.find("div", "map").get_text().replace(" ", "").split("\n")
    partida[pagina_id]["team1"]["map"] = map[3]

    players_ids = []
    players_stats = []
    team_players = []

    players = soup.find_all("tr")
    for stats in players:
        link_ids = stats.find_all("a", "friend")
        for id in link_ids:
            p_id = id.get("href").split("/")[-1:][0]
            players_ids.append(p_id)
        p = stats.get_text().replace(" ", "").split("\n")
        p = [x for x in p if x != ""]
        if p not in players_stats:
            players_stats.append(p)

    headers = players_stats.pop(0)
    headers.insert(1, "Nivel")

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

        if (p <= len(team_players)//2):
            team = "team1"
        else:
            team = "team2"

        player["id"] = team_players[p]["id"]
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
        partida[pagina_id][team]["players"].append(player)

    return partida