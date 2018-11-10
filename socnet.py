import os
import pickle
from time import sleep

from selenium import webdriver

# Baixe o driver de https://sites.google.com/a/chromium.org/chromedriver/downloads
# e extraia o executável. Coloque na constante abaixo o caminho completo para ele.

def get_scores(MATCH, match_info, dictionary):
        scores = match_info.find_elements_by_class_name("score")
        temp = []
        for e in scores:
            if (e.text):
                temp.append(e.text)
        score_a = int(temp[0])
        score_b = int(temp[1])
        dictionary[MATCH]["team_a"]["score"] = score_a
        dictionary[MATCH]["team_b"]["score"] = score_b
        
        if score_a > score_b:
            dictionary[MATCH]["winner"] = "team_a"
        elif score_a < score_b:
            dictionary[MATCH]["winner"] = "team_b"
        else:
            dictionary[MATCH]["winner"] = "draw"

def get_stats(MATCH, match_info, dictionary):
    stats = match_info.find_elements_by_css_selector("div.columns.medium-3.small-12.centered-mobile")
    temp = []
    for e in stats:
        if (e.text):
            temp.append(e.text)
    dictionary[MATCH]["duration"] = temp[3].splitlines(True)[1]
    dictionary[MATCH]["map"] = temp[5].splitlines(True)[1]
    dictionary[MATCH]["type"] = temp[6].splitlines(True)[1]

def get_players_infos(MATCH, players, team, dictionary):
        for p in players: #for player in players
            temp = []
            temp_dict = {}
            info_dict = {
                "link": None,
                "infos": None,
            }
            infos = p.find_elements_by_tag_name("td")
            link = p.find_element_by_tag_name("a")
            player_link = link.get_attribute("href")
            player_id = player_link.rsplit('/', 1)[-1]
            info_dict["link"] = player_link
            for i in infos: #for info in player
                if (i.text):
                    temp.append(i.text)
            info_dict["infos"] = temp
            temp_dict[player_id] = info_dict
            dictionary[MATCH][team]["players"].append(temp_dict)


def main():
    # options = webdriver.ChromeOptions()
    # options.add_experimental_option("prefs", {"profile.default_content_setting_values.notifications": 2})

    # browser = webdriver.Chrome(executable_path=DRIVER_PATH, chrome_options=options)
    DRIVER_PATH = r'/home/borba/Documentos/RedesSociais/GamersNetwork/chromedriver'

    WINDOW_WIDTH = 1024
    WINDOW_HEIGHT = 768

    MATCH = 3743748
    dicionario = {}

    browser = webdriver.Chrome(executable_path=DRIVER_PATH)
    browser.set_window_size(WINDOW_WIDTH, WINDOW_HEIGHT)

    
    # browser.get("file:///home/borba/Documentos/RedesSociais/Projeto/Resultados%20da%20Partida.html")
    SLEEP_TIME = 30
    browser.get('https://gamersclub.com.br/auth')
    sleep(SLEEP_TIME)
    SLEEP_TIME = 1

    for i in range(100):
        browser.get('https://gamersclub.com.br/lobby/partida/' + str(MATCH))
        sleep(SLEEP_TIME)

        match_info = browser.find_element_by_id("match-info-lobby")

        table_rows = match_info.find_elements_by_tag_name("tr")

        if (len(table_rows) > 12):
            MATCH += 1
        else:
            try:
                dicionario[MATCH] = {
                    "team_a": {
                        "score": None,
                        "players": []
                    },
                    "team_b": {
                        "score": None,
                        "players": []
                    },
                    "duration": None,
                    "map": None,
                    "type": None,
                    "winner": None
                }


                get_scores(MATCH, match_info, dicionario)
                get_stats(MATCH, match_info, dicionario)
                
                players_a = table_rows[1:5]
                players_b = table_rows[7:11]

                get_players_infos(MATCH, players_a, "team_a", dicionario)
                get_players_infos(MATCH, players_b, "team_b", dicionario)

                MATCH += 1
            except:
                print("Partida indisponível")
                MATCH += 1
                continue

    pickle.dump(dicionario, open("player_infos.p", "wb"))


if __name__ == '__main__':
    main()
