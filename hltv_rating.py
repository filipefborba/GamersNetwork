# Calculadora de HLTV rating não oficial
# Créditos: http://www.mruy.de/csgo/hltv-rating/
import os
import pickle

matches = {
    3743748: {
        'team_a': {
            'score': 16,
            'players': {
                '294675': {
                    'link': 'https://gamersclub.com.br/jogador/294675',
                    'infos': ['Coltshot\n14', '22', '5', '5', '+ 17', '10', '45%', '4.4000', '129.3', '55', '2', '1', '0', '3', '6', '1', '1', '0', '4', '1', '18']
                },
                '73022': {
                    'link': 'https://gamersclub.com.br/jogador/73022',
                    'infos': ['x2pz\n—', '17', '1', '6', '+ 11', '16', '94%', '2.8333', '98.2', '39', '0', '1', '0', '5', '6', '0', '0', '0', '2', '1', '18']
                },
                '222249': {
                    'link': 'https://gamersclub.com.br/jogador/222249',
                    'infos': ['hardstyle; 11', '13', '2', '5', '+ 8', '3', '23%', '2.6000', '71.4', '29', '0', '0', '0', '9', '2', '0', '0', '0', '2', '0', '18']
                },
                '19204': {
                    'link': 'https://gamersclub.com.br/jogador/19204',
                    'infos': ['feijao 13', '20', '2', '9', '+ 11', '6', '30%', '2.2222', '98.3', '42', '0', '0', '0', '6', '7', '0', '0', '0', '2', '0', '18']
                }
            }
        },
        'team_b': {
            'score': 2,
            'players': [{
                '11679': {
                    'link': 'https://gamersclub.com.br/jogador/11679',
                    'infos': ['level 14 eterno\n14', '12', '1', '16', '-4', '8', '67%', '0.7500', '73.9', '31', '0', '2', '0', '5', '2', '1', '0', '0', '1', '1', '18']
                }
            }, {
                '426665': {
                    'link': 'https://gamersclub.com.br/jogador/426665',
                    'infos': ['Chapolim\n12', '11', '1', '16', '-5', '5', '45%', '0.6875', '74.4', '26', '0', '1', '0', '5', '0', '2', '0', '0', '1', '1', '18']
                }
            }, {
                '768085': {
                    'link': 'https://gamersclub.com.br/jogador/768085',
                    'infos': ['gazela thompson 13', '7', '1', '18', '-11', '2', '29%', '0.3889', '55.3', '17', '0', '1', '0', '3', '2', '0', '0', '0', '1', '0', '18']
                }
            }, {
                '610092': {
                    'link': 'https://gamersclub.com.br/jogador/610092',
                    'infos': ['Carreta\n—', '5', '0', '18', '-13', '1', '20%', '0.2778', '37.3', '10', '0', '0', '0', '5', '0', '0', '0', '0', '0', '0', '18']
                }
            }]
        },
        'duration': '29 Minutos',
        'map': 'de_train',
        'type': 'Competitivo',
        'winner': 'team_a'
    }
}

AVERAGE_KPR = 0.679
AVERAGE_SPR = 0.317
AVERAGE_RMK = 1.277

def hltv_rating(rounds, kills, deaths, one_k, two_k, three_k, four_k, five_k):
    kill_rating = kills / rounds / AVERAGE_KPR 
    survival_rating = (rounds - deaths) / rounds / AVERAGE_SPR
    rmk_rating = (one_k + 4 * two_k + 9 * three_k + 16 * four_k + 25 * five_k) / rounds / AVERAGE_RMK
    hltv_rating = (kill_rating + 0.7 * survival_rating + rmk_rating) / 2.7 
    return hltv_rating

# players = pickle.load(open("gamers_network_with_matches.p", "rb"))

for m in matches:
    print(m)
    players_list = list(matches[m]["team_a"]["players"] + matches[m]["team_b"]["players"])
    print(players_list)
    hltv_dict = {}
    # for p in players_list:
    #     print(players_list[p])
    #     break
    # break