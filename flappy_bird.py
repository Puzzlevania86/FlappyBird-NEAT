import os

from human_player import mainHuman
from ai_player import run

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config-feedforward.txt")
    res = input("Human or AI?\n").upper()
    if res == "AI":
        run(config_path)
    elif res == "HUMAN":
        mainHuman()
    else:
        print("Result is Not Found")
        print("Terminating")
        quit()