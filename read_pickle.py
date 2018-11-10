import pickle
import json

def main():
    d = pickle.load(open("player_infos.p", "rb"))

    with open('player_infos.txt', 'w') as file:
        file.write(json.dumps(d))


if __name__ == "__main__":
    main()