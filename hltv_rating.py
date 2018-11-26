# Calculadora de HLTV rating nao oficial
# Creditos: http://www.mruy.de/csgo/hltv-rating/

AVERAGE_KPR = 0.679
AVERAGE_SPR = 0.317
AVERAGE_RMK = 1.277

def hltv_rating(rounds, kills, deaths, one_k, two_k, three_k, four_k, five_k):
    kill_rating = kills / rounds / AVERAGE_KPR 
    survival_rating = (rounds - deaths) / rounds / AVERAGE_SPR
    rmk_rating = (one_k + 4 * two_k + 9 * three_k + 16 * four_k + 25 * five_k) / rounds / AVERAGE_RMK
    hltv_rating = (kill_rating + 0.7 * survival_rating + rmk_rating) / 2.7 
    return hltv_rating