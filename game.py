
import pgzrun
from trainer import Trainer, Rival
from battle import Battle
from starters import make_starters
import random

starters = make_starters()

WIDTH = 800     # size of the window
HEIGHT = 600


game_state = "intro_sequence"  #determines the what part of the game the player is in, will change alot
user_name = ""

def draw():
    global game_state

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
        screen.draw.text(f"You chose {chosen_starter}!", (250, 50))

def on_key_down(key, unicode):
    global user_name, game_state, chosen_starter

###Intro input###
    if game_state == "intro_sequence":
        if key == keys.BACKSPACE:
            user_name = user_name[:-1]
        elif key == keys.RETURN:
            if len(user_name) > 0:   #Need more here maybe, allow special characters and numbers?
                game_state = "choose_starter"
        elif unicode: 
                user_name += unicode

###Starter selection input###
    if game_state == "choose_starter":
        if key == keys.K_1:
            chosen_starter = starters[0].species
            game_state = "starter_confirmed"
        elif key == keys.K_2:
            chosen_starter = starters[1].species
            game_state = "starter_confirmed"
        elif key == keys.K_3:
            chosen_starter = starters[2].species
            game_state = "starter_confirmed"



pgzrun.go()