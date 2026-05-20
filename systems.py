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
    # Test against current luck BEFORE reducing it
    is_lucky = dice_result <= player_character.luck
    player_character.remove_luck()
    if is_lucky:
        print("    Você deu sorte! O teste de SORTE foi bem-sucedido.")
        return True
    else:
        print("    Você deu azar. O teste de SORTE falhou.")
        return False

def start_combat(player_character: 'Character', monster_data: dict):
    monster_name = monster_data['name']
    current_monster_energy = monster_data['energia']
    Turno = 0
    
    print(f"\n    Iniciando combate contra {monster_name}!")
    print(f"    HABILIDADE: {monster_data['habilidade']} | ENERGIA: {monster_data['energia']}")
    print(f"    Seus Status - HABILIDADE: {player_character.skill} | ENERGIA: {player_character.energy}\n")
    
    while player_character.energy > 0 and current_monster_energy > 0:
        Turno += 1
        print(f"\n    --- {Turno}° Turno ---")
        print(f"    Sua Energia: {player_character.energy} | Energia do {monster_name}: {current_monster_energy}")
        
        player_FA = roll_dice(2) + player_character.skill
        monster_FA = roll_dice(2) + monster_data["habilidade"]
        
        print(f"    Sua Força de Ataque (FA): {player_FA} (Dados + {player_character.skill})")
        print(f"    FA do {monster_name}: {monster_FA} (Dados + {monster_data['habilidade']})")
        
        if player_FA > monster_FA:
            print(f"    Você atingiu o {monster_name}!")
            lt = input("    Gostaria de tentar a SORTE para causar mais dano? (s/n): ").strip().lower()
            if lt == 's':
                if luck_test(player_character):
                    # Sucesso: Causa +2 pontos extras de dano (total 4 de dano)
                    current_monster_energy -= 4
                    print(f"    Golpe Crítico! Você causou 4 pontos de dano no {monster_name}!")
                else:
                    # Falha: Causa -1 ponto de dano (total 1 de dano)
                    current_monster_energy -= 1
                    print(f"    Golpe Superficial! Você causou apenas 1 ponto de dano no {monster_name}!")
            else:
                current_monster_energy -= 2
                print(f"    Você causou 2 pontos de dano no {monster_name}!")
                
        elif player_FA < monster_FA:
            print(f"    O {monster_name} atingiu você!")
            lt = input("    Gostaria de tentar a SORTE para minimizar o ferimento? (s/n): ").strip().lower()
            if lt == 's':
                if luck_test(player_character):
                    # Sucesso: Minimiza para apenas 1 de dano
                    player_character.take_dmg(1)
                else:
                    # Falha: Aumenta para 3 de dano
                    player_character.take_dmg(3)
            else:
                player_character.take_dmg(2)
                
        else:
            print("    Ambos evitaram os golpes! Ninguém se feriu neste turno.")
            
        # Pequena pausa para legibilidade
        input("\n    Pressione Enter para continuar para o próximo turno...")
        
    if player_character.energy <= 0:
        print(f"\n    Você foi derrotado por {monster_name}!")
        player_character.combat_history.append({
            'name': monster_name,
            'hab': monster_data['habilidade'],
            'ene': monster_data['energia'],
            'resultado': 'derrota'
        })
        return False
    else:
        print(f"\n    Você derrotou {monster_name}!")
        player_character.combat_history.append({
            'name': monster_name,
            'hab': monster_data['habilidade'],
            'ene': monster_data['energia'],
            'resultado': 'vitória'
        })
        return True