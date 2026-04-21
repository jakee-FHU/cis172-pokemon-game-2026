import pgzrun, random
from trainer import Trainer, Rival
# from battle import Battle
from starters import make_starters

starters = make_starters()

WIDTH = 800     # size of the window
HEIGHT = 600


game_state = "intro_sequence"  #determines the what part of the game the player is in, will change alot
user_name = ""
battle_count = 1
max_battles = 3
new_pokemon = None

battle_message = []

winner = None

def draw():

###Choose your name (text)###
    if game_state == "intro_sequence":
        screen.clear() #clears previous text
        screen.draw.text(f"Enter your name: " + user_name, (250, 50)) #adds new text

###Choose your starter (text)###
    elif game_state == "choose_starter":
        screen.clear()  
        screen.draw.text(f"Hello {user_name}! Choose your Pokemon!", (250, 50 ))  
        
        for i, pokemon in enumerate(starters):
            screen.draw.text(f"{i+1}. {pokemon.species}", (250, 150 + (i * 50)))  # 3 starters

###Placeholder, will most likely change, just tells the user what starter they chose###
    elif game_state == "starter_confirmed":
        screen.clear()
        screen.draw.text(f"You chose {chosen_starter.species}!", (250, 50))
        screen.draw.text(f"Are you ready {user_name}? Press ENTER to fight!", (250, 100))

###Simple battle
    elif game_state == "battle":
        screen.clear()
        
        screen.draw.text(f"{player.name.upper()}:\t {player.active_pokemon.name} ({player.active_pokemon.health}/{player.active_pokemon.max_health} HP)", (50, 350))
        screen.draw.text(f"{rival.name.upper()}:\t {rival.active_pokemon.name} ({rival.active_pokemon.health}/{rival.active_pokemon.max_health} HP)", (400, 50))

        screen.draw.text("Choose a move by pressing a key:", (50, 380))

        for i, move in enumerate(player.active_pokemon.moves):
            screen.draw.text(f"\n {i+1}. {move.name}", (50, 400 + i * 30))

        for i, msg in enumerate(battle_message):
            screen.draw.text(msg, (400, 380 + i * 50))
    
    elif game_state == "battle_end":
        screen.clear()
        screen.draw.text(f"Congrats {user_name}! You won the battle!", (250, 50))

    elif game_state == "new_pokemon":
        screen.clear()
        screen.draw.text(f"A {new_pokemon.species} has been added to your party!", (250, 50))
        screen.draw.text(f"Are you ready {user_name}? Press ENTER to fight!", (250, 100))

    elif game_state == "gg":
        screen.clear()

        if winner == "player":
            screen.draw.text(f"Congrats {user_name}! You won!", (250, 50))
        elif winner == "rival":
            screen.draw.text(f"Sorry {user_name}! You lost...")

        
def start_battle():
    global rival, battle_message, battle_count
    battle_message.clear()

    # restore player's party health before each battle
    for pokemon in player.party:
        pokemon.health = pokemon.max_health

    rival = Rival("Opponent")
    rival_starter = random.choice(starters)
    rival.party = [rival_starter]
    rival.active_pokemon = rival_starter

def on_key_down(key, unicode):
    global user_name, game_state, chosen_starter, player, battle_message

###Intro input###
    if game_state == "intro_sequence":
        if key == keys.BACKSPACE:
            user_name = user_name[:-1]
        elif key == keys.RETURN:
            if len(user_name) > 0:   #Need more here maybe, allow special characters and numbers?
                game_state = "choose_starter"
                player = Trainer(name = user_name)
        elif unicode: 
                user_name += unicode

###Starter selection input###
    elif game_state == "choose_starter":
        chosen_starter = None

        if key == keys.K_1:
            chosen_starter = starters[0]
        elif key == keys.K_2:
            chosen_starter = starters[1]
        elif key == keys.K_3:
            chosen_starter = starters[2]
        else:
            return #in case player does not input a valid number

        if chosen_starter:
            player.party.append(chosen_starter)
            player.active_pokemon = chosen_starter

            game_state = "starter_confirmed"

    elif game_state == "starter_confirmed":
        if key == keys.RETURN:
            global rival

            start_battle()

            game_state = "battle"

    elif game_state == "battle":
        global battle_message, winner, battle_count

        battle_message.clear()

        if key == keys.K_1:
            move = player.active_pokemon.moves[0]
        elif key == keys.K_2:
            move = player.active_pokemon.moves[1]
        else:
            return 
        
        
        #PLAYER ATTACK
        player.active_pokemon.attack(move, rival.active_pokemon)
        battle_message.append(f"{player.active_pokemon.name} used {move.name}!")

        #RIVAL ATTACK
        if rival.active_pokemon.health > 0:
            r_move = random.choice(rival.active_pokemon.moves)
            rival.active_pokemon.attack(r_move, player.active_pokemon)
            battle_message.append(f"{rival.active_pokemon.name} used {r_move.name}!")


        if rival.active_pokemon.health <= 0:
            if battle_count < max_battles:
                battle_count += 1
                game_state = "battle_end"
            else:
                winner = "player"
                game_state = "gg"
        elif player.active_pokemon.health <= 0:
            winner = "rival"
            game_state = "gg"

    elif game_state == "battle_end":
        if key == keys.RETURN:
            global new_pokemon
            new_pokemon = random.choice(starters[:])
            player.party.append(new_pokemon)
            game_state = "new_pokemon"

    elif game_state == "new_pokemon":
        if key == keys.RETURN:
            start_battle()
            game_state = "battle"

pgzrun.go()