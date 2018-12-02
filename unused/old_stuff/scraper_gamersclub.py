import os
import pickle
from time import sleep
import requests
import json

from selenium import webdriver

# Baixe o driver de https://sites.google.com/a/chromium.org/chromedriver/downloads
# e extraia o executável. Coloque na constante abaixo o caminho completo para ele.

def fetch_player_info(player_id):
    player = {
        "kd_ratio": None,
        "player_info": None,
        "player_rating": None,
        "player_matches_ids": None,
        "is_subscriber": None
    }
    url = "https://gamersclub.com.br/api/statistics/" + player_id + "/search/0/pt-br"

    payload = ""
    headers = {
        'Referer': "https://gamersclub.com.br/jogador/0",
        'cache-control': "no-cache",
        }

    response = requests.request("POST", url, data=payload, headers=headers)
    data = json.loads(response.text)
    player["kd_ratio"] = data["kd_ratio"]
    player["player_info"] = data["player_info"]
    player["player_rating"] = data["player_rating"]
    player["player_matches_ids"] = data["player_matches_ids"]
    player["is_subscriber"] = data["is_subscriber"]
    return player

def get_player_friends(browser):
    player_friends = []
    container = browser.find_element_by_id("mCSB_1_container")
    friends = container.find_elements_by_tag_name("a")
    for f in friends:
        player_link = f.get_attribute("href")
        player_friends.append(player_link)
    return player_friends

def get_friend_friends(link, dados_rede, id, browser, iterations, SLEEP_TIME=1):
    browser.get(link)
    sleep(SLEEP_TIME)

    player = fetch_player_info(id)
    friends = get_player_friends(browser)
    dados_rede[id] = {
        "infos": player,
        "player_friends": friends
    }

    if (iterations > 0):
        print(friends)
        for f in friends:
            player_id = f.rsplit('/', 1)[-1]
            if (player_id in dados_rede):
                continue
            else:
                iterations -= 1
                get_friend_friends(f, dados_rede, player_id, browser, iterations)
    else:
        pass

def main():
    DRIVER_PATH = r'/home/borba/Documentos/RedesSociais/GamersNetwork/chromedriver'

    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 768
    SLEEP_TIME = 1

    dados_rede = {}

    browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    browser.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    initial_player_id = str(294675)

    # browser.get("file:////home/borba/Documentos/RedesSociais/GamersNetwork/jogador.html")
    SLEEP_TIME = 30
    browser.get('https://gamersclub.com.br/auth')
    sleep(SLEEP_TIME)
    SLEEP_TIME = 1

    browser.get('https://gamersclub.com.br/jogador/' + initial_player_id)

    player = fetch_player_info(initial_player_id)
    friends = get_player_friends(browser)
    dados_rede[initial_player_id] = {
        "infos": player,
        "player_friends": friends
    }

    for f in friends:
        player_id = f.rsplit('/', 1)[-1]
        if (player_id in dados_rede):
            continue
        else:
            get_friend_friends(f, dados_rede, player_id, browser, 1)
    
    pickle.dump(dados_rede, open("gamers_network.p", "wb"))


if __name__ == '__main__':
    main()
