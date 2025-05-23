import random
import subprocess
import platform
from character import Character
import data.paragraphs as p
import data.monters as m
import textwrap

def print_paragraphs(story_dict, *ids, width=80):
    for pid in ids:
        texto = story_dict[pid]["texto"]
        texto_limpo = " ".join(texto.strip().split())
        print(textwrap.fill(texto_limpo, width=width))
        print("\n" + "-" * width + "\n")
    
def screen_clear():
    os = platform.system()
    if os == "Linux":
        subprocess.run("clear")
    elif os == "Windows":
        subprocess.run("cls")
    else:
        subprocess.run("clear")

def roll_dice(amount):
    roll_result = []
    for i in range(amount):
        roll = random.randint(1,6)
        roll_result.append(roll)
    return sum(roll_result)    

def luck_test(player_character: 'Character'):
    dice_result = roll_dice(2)
    player_character.remove_luck()
    if dice_result <= player_character.luck:
        print("Você deu sorte! O teste de SORTE foi concluído.")
        return True
    else:
        print("Você deu azar. O teste de SORTE falhou.")
        return False

def start_combat(player_character: 'Character', mosnter_data: dict):
    current_monster_energy = mosnter_data[""]
    
    
    pass