import json
import requests
from bs4 import BeautifulSoup, SoupStrainer
from matches_html import get_match_by_html

fp = open('campeonatos.json', 'r')
data = json.load(fp)

partidas_campeonato = {}
for campeonato in data:
    partidas = []
    soup = BeautifulSoup(data[campeonato], features="lxml")
    for link in soup.find_all('a'):
        partidas.append(link.get('href').replace("https://gamersclub.com.br/campeonatos/csgo/"+str(campeonato)+"/partida/", ""))
    partidas_campeonato.update({campeonato : [k for k in list(set(partidas)) if len(k) < 7]})

with open('partidas_campeonatos.json', 'w') as fp:
    json.dump(partidas_campeonato, fp)

for campeonato in partidas_campeonato:
    for partida in partidas_campeonato[campeonato]:
            url = "https://gamersclub.com.br/api/ebacon2/stats/scoreboards/{}/{}".format(campeonato, partida)

            headers = {
            'Cookie': "__cfduid=daa46fdf071f015d3e0aa50c2874688ff1534266040; _ga=GA1.3.1588820037.1538761089; SL_C_23361dd035530_KEY=a14d3638cda988422792e3613234743b983fdd9e; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102=session_57ed498d-d875-4902-9be5-a2f04edd3693; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102%2Fc3b2fd43f122359ddf0a576a7d4d75ab74b4d92f9feb92c94eeb2406a6d36192=session_57ed498d-d875-4902-9be5-a2f04edd3693; gclubsess=9969960cdda75b9dedeb7af242495c14ffc135e4; _gid=GA1.3.1431837867.1543524480; _gat_UA-64910362-1=1",
            'Referer': "https://gamersclub.com.br/campeonatos/csgo/1257/partida/103992",
            'cache-control': "no-cache",
            'Postman-Token': "918ccadf-a7e8-4d54-b672-e3cd1026ecae"
            }

            response = requests.request("GET", url, headers=headers)
            if response.text == "[]":
                # print("Erro: {}:{}".format(campeonato, partida))
                partida = get_match_by_html(campeonato, partida)
                # print(partida)
            else:
                print("CORRETO: {}:{}".format(campeonato, partida))

            