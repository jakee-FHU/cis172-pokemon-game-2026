import random
from trainer import Trainer, Rival
from battle import Battle
from starters import make_starters, choose_starter

def main():
    # --- PLAYER ---
    # ask player to input name:
    print("Enter your name (or press Enter to keep default name):")
    player_name = input("\n> ")
    starters = make_starters()

    # use default player name if none entered, else use player_name input:
    if not player_name:
        player = Trainer('Player')
    else:
        player = Trainer(player_name)

    # let player choose starting Pokemon and initialize player party:
    player_starter_pokemon = choose_starter(starters)
    player.party = [player_starter_pokemon]
    player.active_pokemon = player_starter_pokemon

    # --- RIVAL ---
    # use default name and choose starter from remaining options:
    rival = Rival("Rival")
    rival_starter_pokemon = random.choice(starters)
    rival.party = [rival_starter_pokemon]
    rival.active_pokemon = rival_starter_pokemon

    # --- BATTLE ---
    # initialize battle:
    battle = Battle(player, rival)
    battle.start_battle()

if __name__ == "__main__":
    main()