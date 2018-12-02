import requests
import json
from bs4 import BeautifulSoup, SoupStrainer
from get_match_html import get_partida_html
#pip install bs4
#pip install lxml

def get_partidas_campeonato(id):
    url = "https://gamersclub.com.br/campeonatos/csgo/" + str(id)
    querystring = {"pag":"partidas"}
    headers = {
        'Referer': "https://gamersclub.com.br/campeonatos/csgo/846",
        'X-Requested-With': "XMLHttpRequest",
        'cache-control': "no-cache"
        }
    response = requests.request("GET", url, headers=headers, params=querystring)
    partidas_html = response.text

    camp_partidas = {id: {}}
    soup = BeautifulSoup(partidas_html, features="lxml")
    for link in soup.find_all('a'):
        partida_id = link.get("href").split("/")[-1:][0]
        if (partida_id not in camp_partidas[id]) and (partida_id != None) and (not partida_id.startswith("#")) :
            camp_partidas[id][partida_id] = {}

    return camp_partidas

def get_partida(camp_id, partida_id):
    url = "https://gamersclub.com.br/api/ebacon2/stats/scoreboards/{}/{}".format(str(camp_id), str(partida_id))
    headers = {
        'Referer': "https://gamersclub.com.br/campeonatos/csgo/1257/partida/104124",
        'Cookie': "__utma=203582342.232122176.1489463720.1497671483.1497749677.12; _ga=GA1.3.232122176.1489463720; rdtrk=%7B%22id%22%3A%2219e6bdb6-ab8f-4549-bf65-45ff0c86e846%22%7D; intercom-lou-gp4gdmdo=1; __trf.src=encoded_eyJmaXJzdF9zZXNzaW9uIjp7InZhbHVlIjoiMjAzNTgyMzQyLjE0ODk0NjM3MjEuMS4xLnV0bWNzcj0oZGlyZWN0KXx1dG1jY249KGRpcmVjdCl8dXRtY21kPShub25lKSIsImV4dHJhX3BhcmFtcyI6e319LCJjdXJyZW50X3Nlc3Npb24iOnsidmFsdWUiOiJodHRwczovL2dhbWVyc2NsdWIuY29tLmJyLyIsImV4dHJhX3BhcmFtcyI6e319LCJjcmVhdGVkX2F0IjoxNTE4MTM1OTYwMzAwfQ==; __cfduid=dfaae443a782f1d6d0b715bebbb0338321522639930; SL_C_23361dd035530_KEY=a14d3638cda988422792e3613234743b983fdd9e; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102=session_91c09cdd-f616-4e12-9599-8aad4f09988d; crisp-client%2Fsession%2F839282a3-c2c1-4fd3-b493-0f2d3c1e2102%2Fc3b2fd43f122359ddf0a576a7d4d75ab74b4d92f9feb92c94eeb2406a6d36192=session_91c09cdd-f616-4e12-9599-8aad4f09988d; SL_C_23361dd035530_VID=Nm59QhW-6TYP; SL_C_23361dd035530_SID=hMyy703pm5eY; gclubsess=fe6dc36080d6083b0e1060909e4d5a51218b6dd8; _gid=GA1.3.168545321.1543697640; _fbp=fb.2.1543697640249.576304885",
        'cache-control': "no-cache",
        }
    response = requests.request("GET", url, headers=headers)
    resultados_partida = response.json()
    return resultados_partida

try:
    campeonatos_ids = [846, 881, 915, 957, 1008, 1019, 1039, 1079, 1116, 1164, 1209, 1257]
    campeonatos = {}
    for str(camp_id) in campeonatos_ids:
        camp = get_partidas_campeonato(camp_id)
        campeonatos.update(camp)

    #campeonatos = {846: {'66817': {}, '66818': {}, '66386': {}, '66819': {}, '66387': {}, '66820': {}, '66385': {}, '66920': {}, '66885': {}, '66884': {}, '66919': {}, '66388': {}, '66917': {}, '66918': {}, '67081': {}, '67082': {}, '66981': {}, '66921': {}, '67083': {}, '67115': {}, '67119': {}, '67117': {}, '67116': {}, '67118': {}, '68711': {}, '68712': {}, '68775': {}}, 881: {'69447': {}, '69448': {}, '69449': {}, '69456': {}, '69455': {}, '69452': {}, '69454': {}, '69451': {}, '69489': {}, '69492': {}, '69490': {}, '69633': {}, '69493': {}, '69494': {}, '69495': {}, '69488': {}, '69634': {}, '69630': {}, '69631': {}, '69632': {}, '70936': {}, '71172': {}, '70935': {}, '70934': {}, '71187': {}, '71188': {}, '71704': {}}, 915: {'73003': {}, '73004': {}, '73007': {}, '73005': {}, '73076': {}, '73008': {}, '73011': {}, '73009': {}, '73010': {}, '73194': {}, '73195': {}, '73197': {}, '73196': {}, '73212': {}, '73213': {}, '73405': {}, '73272': {}, '73273': {}, '73599': {}, '73598': {}, '73406': {}, '73637': {}, '73636': {}, '73634': {}, '73600': {}, '76347': {}, '75972': {}, '76382': {}}, 957: {'76641': {}, '77119': {}, '77117': {}, '77120': {}, '76642': {}, '77121': {}, '76643': {}, '76640': {}, '77245': {}, '77248': {}, '77243': {}, '77242': {}, '77240': {}, '77247': {}, '77241': {}, '77244': {}, '77643': {}, '77611': {}, '77642': {}, '77610': {}, '79525': {}, '79524': {}, '77645': {}, '79597': {}, '79980': {}, '79981': {}, '80325': {}}, 1008: {'80886': {}, '80888': {}, '80889': {}, '80890': {}, '80892': {}, '80893': {}, '80887': {}, '80891': {}, '80960': {}, '80895': {}, '80961': {}, '80894': {}}, 1019: {'81425': {}, '81432': {}, '81430': {}, '81435': {}, '81428': {}, '81436': {}, '81427': {}, '81431': {}, '81429': {}, '81433': {}, '81426': {}, '81434': {}, '82905': {}, '82906': {}, '82908': {}, '82907': {}, '82950': {}, '82951': {}, '83230': {}}, 1039: {'84509': {}, '84510': {}, '84511': {}, '84512': {}, '84513': {}, '84514': {}, '84515': {}, '84516': {}, '84517': {}, '84518': {}, '84519': {}, '84520': {}, '84693': {}, '84696': {}, '84694': {}, '84695': {}, '84698': {}, '84699': {}, '85588': {}}, 1079: {'88339': {}, '88343': {}, '88340': {}, '88348': {}, '88337': {}, '88344': {}, '88342': {}, '88347': {}, '88338': {}, '88345': {}, '88341': {}, '88346': {}, '88494': {}, '88496': {}, '88493': {}, '88495': {}, '88504': {}, '88505': {}, '88628': {}}, 1116: {'91382': {}, '91392': {}, '91385': {}, '91387': {}, '91391': {}, '91381': {}, '91386': {}, '91388': {}, '91383': {}, '91389': {}, '91384': {}, '91390': {}, '91598': {}, '91599': {}, '91607': {}, '91608': {}, '91703': {}}, 1164: {'96587': {}, '96590': {}, '96586': {}, '96595': {}, '96589': {}, '96593': {}, '96584': {}, '96592': {}, '96585': {}, '96588': {}, '96594': {}, '96591': {}, '96985': {}, '96986': {}, '97064': {}, '97065': {}, '97521': {}}, 1209: {'101120': {}, '101117': {}, '101143': {}, '101138': {}, '101119': {}, '101118': {}, '101139': {}, '101142': {}, '101116': {}, '101121': {}, '101140': {}, '101141': {}, '102020': {}, '102019': {}, '102044': {}, '102047': {}, '102261': {}}, 1257: {'104124': {}, '104125': {}, '103994': {}, '103992': {}, '103988': {}, '103986': {}, '104127': {}, '104126': {}, '103993': {}, '103987': {}, '104128': {}, '104129': {}, '105105': {}, '105106': {}, '105235': {}, '105240': {}, '105376': {}}} 

    for camp_id in campeonatos:
        for partida_id in campeonatos[camp_id]:
            if camp_id >= 1116:
                partida = get_partida(camp_id, partida_id)
            else:
                partida = get_partida_html(camp_id, partida_id)
            campeonatos[camp_id][partida_id] = partida
        
    with open("campeonatos_completo.json", 'w') as fp:
        json.dump(campeonatos, fp)

except Exception as e:
    print(e)
    print("Um erro ocorreu. Salvando o restante...")
    with open("campeonatos_incompleto.json", 'w') as fp:
        json.dump(campeonatos, fp)


    
