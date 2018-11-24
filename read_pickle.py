import pickle
import json

def main():
#     d = pickle.load(open("gamers_network.p", "rb"))
    d = pickle.load(open("gamers_network_with_matches.p", "rb"))
#     with open('gamers_network.txt', 'w') as file:
    with open('gamers_network_with_matches.txt', 'w') as file:
        file.write(json.dumps(d))


if __name__ == "__main__":
    main()