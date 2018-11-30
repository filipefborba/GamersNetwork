import os
from time import sleep
import requests
import json
import requests

# url = "https://gamersclub.com.br/lobby/partida/3802271/1"

# payload = ""
# headers = {
#     'Referer': "https://gamersclub.com.br/lobby/partida/3802271",
#     'Cookie': "__cfduid=daa46fdf071f015d3e0aa50c2874688ff1534266040; _ga=GA1.3.1588820037.1538761089; SL_C_23361dd035530_KEY=a14d3638cda988422792e3613234743b983fdd9e; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102=session_57ed498d-d875-4902-9be5-a2f04edd3693; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102%2Fc3b2fd43f122359ddf0a576a7d4d75ab74b4d92f9feb92c94eeb2406a6d36192=session_57ed498d-d875-4902-9be5-a2f04edd3693; gclubsess=9969960cdda75b9dedeb7af242495c14ffc135e4; _gid=GA1.3.1431837867.1543524480; _gat_UA-64910362-1=1",
#     'cache-control': "no-cache",
#     }

# response = requests.request("GET", url, data=payload, headers=headers)

# print(response.text)

campeonatos_ids = [846, 881, 915, 957, 1008, 1019, 1039, 1079, 1116, 1164, 1209, 1257]

def get_partidas(id):
    url = "https://gamersclub.com.br/campeonatos/csgo/" + str(id)
    querystring = {"pag":"partidas"}

    payload = ""
    headers = {
        'Referer': "https://gamersclub.com.br/campeonatos/csgo/846",
        'X-Requested-With': "XMLHttpRequest",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, data=payload, headers=headers, params=querystring)

    return response.text

campeonatos = {}

for id in campeonatos_ids:
    partida = str(get_partidas(id))
    campeonatos[id] = partida
    break

with open('campeonatos.json', 'w') as fp:
    json.dump(campeonatos, fp)

