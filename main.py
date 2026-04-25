import pgzrun, random
from trainer import Trainer, Rival
# from battle import Battle
from starters import make_starters, make_pokemon

starters = make_starters()

WIDTH = 800     # size of the window
HEIGHT = 600


game_state = "intro_sequence"  #determines the what part of the game the player is in, will change alot
user_name = ""
battle_count = 1
max_battles = 3
new_pokemon = None
music_playing = False

battle_message = []

winner = None

#start music
def update():
    global music_playing
    if music_playing == False:
        music.play("battle_bgm")
        music.set_volume(0.1)
        music_playing = True

def draw():
    screen.blit("battle_bg", (0, 0))

###Choose your name (text)###
    if game_state == "intro_sequence":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))
        screen.draw.text(f"Enter your name: " + user_name, (50, 450), color="black")

###Choose your starter (text)###
    elif game_state == "choose_starter":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))
        screen.draw.text(f"Hello {user_name}! Choose your Pokemon! (Use 1 / 2 / 3 keys)", (50, 450), color="black")  
        
        for i, pokemon in enumerate(starters):
            screen.draw.text(f"{i+1}. {pokemon.species}", (50, 490 + (i * 30)), color="black")  # 3 starters

###Placeholder, will most likely change, just tells the user what starter they chose###
    elif game_state == "starter_confirmed":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))
        screen.draw.text(f"You chose {chosen_starter.species}!", (50, 450), color="black")
        screen.draw.text(f"Your partner is {player.party[1].species}", (50, 500), color="black")

        screen.draw.text("Controls:", (400, 420), color="black")
        screen.draw.text("1 / 2 - Choose move", (400, 450), color="black")
        screen.draw.text("3 - Use potion", (400, 480), color="black")
        screen.draw.text("S - Switch Pokemon", (400, 510), color="black")

        screen.draw.text(f"Are you ready {user_name}? Press ENTER to fight!", (50, 550), color="black")

###Simple battle
    elif game_state == "battle":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))
        top_panel = Rect((0, 0), (800, 100))
        screen.draw.filled_rect(top_panel, (240, 240, 200))
        
        # player pokemon
        player_sprite = Actor(player.active_pokemon.sprite)
        player_sprite.pos = (220, 250)
        player_sprite.draw()

        # rival pokemon
        rival_sprite = Actor(rival.active_pokemon.sprite)
        rival_sprite.pos = (600, 250)
        rival_sprite.draw()

        screen.draw.text(f"{player.name.upper()}:\t {player.active_pokemon.name} ({player.active_pokemon.health}/{player.active_pokemon.max_health} HP)", (50, 420), color="black")
        screen.draw.text(f"{rival.name.upper()}:\t {rival.active_pokemon.name} ({rival.active_pokemon.health}/{rival.active_pokemon.max_health} HP)", (400, 50), color="black")

        screen.draw.text("Press a key to play:", (50, 450), color="black")

        for i, move in enumerate(player.active_pokemon.moves):
            screen.draw.text(f"{i+1}. {move.name}", (50, 490 + i * 30), color="black")
                
        screen.draw.text(f"{len(player.active_pokemon.moves) + 1}. Use Potion ({player.potions}/10)", (50, 490 + (len(player.active_pokemon.moves)) * 30), color="black")

        for i, msg in enumerate(battle_message):
            screen.draw.text(msg, (400, 450 + i * 30), color="black")
    
    elif game_state == "battle_end":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))
        screen.draw.text(f"Congrats {user_name}! You won the battle!", (50, 450), color="black")

    elif game_state == "new_pokemon":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))
        screen.draw.text(f"A {new_pokemon.species} has been added to your party!", (50, 450), color="black")
        screen.draw.text(f"Are you ready {user_name}? Press ENTER to fight!", (50, 490), color="black")

    elif game_state == "gg":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))

        if winner == "player":
            screen.draw.text(f"Congrats {user_name}! You won!", (50, 450), color="black")
        elif winner == "rival":
            screen.draw.text(f"Sorry {user_name}! You lost...", (50, 450), color="black")
    
    elif game_state == "switching":
        bottom_panel = Rect((0, 400), (800, 200))
        screen.draw.filled_rect(bottom_panel, (240, 240, 200))

        screen.draw.text("Choose a Pokemon to switch to:", (50, 420), color="black")

        for i, pokemon in enumerate(player.party):
            status = ""
            if pokemon.health <= 0:
                status = " (Fainted)"

            screen.draw.text(f"{i+1}. {pokemon.name} ({pokemon.health}/{pokemon.max_health} HP){status}", (50, 460 + i * 30),color="black")

        
def start_battle():
    global rival, battle_message, battle_count
    battle_message.clear()

    # restore player's party health before each battle
    for pokemon in player.party:
        pokemon.health = pokemon.max_health

    rival = Rival("Opponent")

    if battle_count == 1:
        rival_team_size = 1
    elif battle_count == 2:
        rival_team_size = 2
    else:
        rival_team_size = 3

    rival.party = []

    for i in range(rival_team_size):
        rival_species = random.choice(starters).species
        rival_pokemon = make_pokemon(rival_species)
        rival.party.append(rival_pokemon)

    rival.active_pokemon = rival.party[0]

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
        chosen_species = None

        if key == keys.K_1:
            chosen_species = starters[0].species
        elif key == keys.K_2:
            chosen_species = starters[1].species
        elif key == keys.K_3:
            chosen_species = starters[2].species
        else:
            return #in case player does not input a valid number

        chosen_starter = make_pokemon(chosen_species)
        player.party.append(chosen_starter)
        player.active_pokemon = chosen_starter

        available = [p for p in starters if p.species != chosen_species]
        second_species = random.choice(available).species
        second_pokemon = make_pokemon(second_species)
        player.party.append(second_pokemon)
        
        game_state = "starter_confirmed"

    elif game_state == "starter_confirmed":
        if key == keys.RETURN:
            global rival

            start_battle()

            game_state = "battle"

    elif game_state == "battle":
        global battle_message, winner, battle_count

        battle_message.clear()

        # PLAYER CHOICE
        if key == keys.S:
            game_state = "switching"
            return
        if key == keys.K_1:
            move = player.active_pokemon.moves[0]
            player.active_pokemon.attack(move, rival.active_pokemon)
            battle_message.append(f"{player.active_pokemon.name} used {move.name}!")            
        elif key == keys.K_2:
            move = player.active_pokemon.moves[1]
            player.active_pokemon.attack(move, rival.active_pokemon)
            battle_message.append(f"{player.active_pokemon.name} used {move.name}!") 
        elif key == keys.K_3:
            if player.potions > 0 and player.active_pokemon.health == player.active_pokemon.max_health:
                battle_message.append(f"{player.active_pokemon.name} is at full health!")
                return
            elif player.potions > 0:
                heal_amount = player.use_potion(player.active_pokemon)
                battle_message.append(f"{player.active_pokemon.name} healed {heal_amount} HP!")
            else:
                battle_message.append(f"No potions to use!")
                return
        else:
            return


        # RIVAL ATTACKS IF STILL ALIVE
        if rival.active_pokemon.health > 0:
            r_move = random.choice(rival.active_pokemon.moves)
            rival.active_pokemon.attack(r_move, player.active_pokemon)
            battle_message.append(f"{rival.active_pokemon.name} used {r_move.name}!")

        #RIVAL CHOICE
        if rival.active_pokemon.health <= 0:
            if rival.has_usable_pokemon():
                rival.switch_pokemon()
                battle_message.append(f"Opponent sent out {rival.active_pokemon.name}!")
            else:
                if battle_count < max_battles:
                    battle_count += 1
                    game_state = "battle_end"
                else:
                    winner = "player"
                    game_state = "gg"

        elif player.active_pokemon.health <= 0:
            if player.has_usable_pokemon():
                game_state = "switching"
                battle_message.append(f"{player.active_pokemon.name} fainted! Choose another Pokemon.")
            else:
                winner = "rival"
                game_state = "gg"
    
    elif game_state == "switching":
        if key == keys.K_1:
            index = 0
        elif key == keys.K_2:
            index = 1
        elif key == keys.K_3:
            index = 2
        else:
            return

        if index < len(player.party):
            selected = player.party[index]

            if selected.health <= 0:
                battle_message.clear()
                battle_message.append(f"{selected.name} has fainted!")
                return

            if selected == player.active_pokemon:
                battle_message.clear()
                battle_message.append(f"{selected.name} is already active!")
                game_state = "battle"
                return

            player.active_pokemon = selected
            battle_message.clear()
            battle_message.append(f"Go, {selected.name}!")

            # switching costs a turn, so rival attacks
            if rival.active_pokemon.health > 0:
                r_move = random.choice(rival.active_pokemon.moves)
                rival.active_pokemon.attack(r_move, player.active_pokemon)
                battle_message.append(f"{rival.active_pokemon.name} used {r_move.name}!")

            if player.active_pokemon.health <= 0:
                if player.has_usable_pokemon():
                    game_state = "switching"
                    battle_message.append("Choose another Pokemon!")
                else:
                    winner = "rival"
                    game_state = "gg"
            else:
                game_state = "battle"
    
    elif game_state == "battle_end":
        if key == keys.RETURN:
            global new_pokemon

            if battle_count == 2:
                reward_species = random.choice(starters).species
                new_pokemon = make_pokemon(reward_species)
                player.party.append(new_pokemon)
                game_state = "new_pokemon"
            else:
                start_battle()
                game_state = "battle"

    elif game_state == "new_pokemon":
        if key == keys.RETURN:
            start_battle()
            game_state = "battle"

pgzrun.go()