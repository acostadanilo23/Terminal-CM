import random
import character as c
import data.paragraphs as p
import data.monters as m
import textwrap

def print_paragraphs(story_dict, *ids, width=80):
    for pid in ids:
        texto = story_dict[pid]["texto"]
        texto_limpo = " ".join(texto.strip().split())
        print(textwrap.fill(texto_limpo, width=width))
        print("\n" + "-" * width + "\n")

def roll_dice():
    dice_result = random.randint(1,6)
    return dice_result
    

def luck_test():
    dice_1 = roll_dice()
    dice_2 = roll_dice()
    
    dice_result = dice_1 + dice_2
    
    if c.Character.luck == dice_result:
        return True
    else:
        return False


def combat():
    player_damage = c.skill + (roll_dice() + roll_dice())
    monster_damage = m.skill + (roll_dice() + roll_dice())
    
    if player_damage > monster_damage:
        m.energy -= 2
        if luck_test():
            m.energy -= 1
            c.luck -= 1
        
    

#print(f"Foi sortudo? {luck_test()}")


dados_goblin = m.MONSTERS_DATA["Aranha Gigante"]

#print(f"Habilidade do Goblin: {dados_goblin['habilidade']}")
#print(f"Energia do Goblin: {dados_goblin['energia']}")
#print(f"Notas sobre o Goblin: {dados_goblin['notas']}")
#print("\n\n\n\n\n")

print(p.TITULOS[1]["texto"])
#print("\n\n\n\n\n")
print_paragraphs(p.STORY, 1,2,3,4,5,6,7,8,9,10)