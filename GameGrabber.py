import random
import io

def main():
    file = io.open("FreeSteamGamesList.txt", 'r', encoding="utf-8")
    lines = file.readlines()
    game = random.choice(lines)

    print(game)


if __name__ == "__main__":
    main()