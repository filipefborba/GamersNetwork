import pickle
import json

def main():
        #scraper_gamersclub
        # d = pickle.load(open("gamers_network.p", "rb"))
        # with open('gamers_network.txt', 'w') as file:
        #         file.write(json.dumps(d))
        
        #scraper_matches
        # d = pickle.load(open("gamers_network_with_matches.p", "rb"))
        # with open('gamers_network_with_matches.txt', 'w') as file:
        #         file.write(json.dumps(d))

        #hltv_rating
        # with open('gamers_network_with_rating.txt', 'w') as file:
        #         file.write(json.dumps(d))
        
        # #fix pickle
        # with open('gamers_network_with_rating.txt', 'r') as file:
        #         d = json.load(file.read())
        #         pickle.dump(d, open("gamers_network_final.p", "wb"))


if __name__ == "__main__":
    main()