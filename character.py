import random

class Character:
    
    #declarando o metodo __init__ (método dunder)
    def __init__(self):
        #Atributo Skill
        self.initial_skill = random.randint(1,6) + 6
        self.skill = self.initial_skill
        
        #Atributo energia
        self.initial_energy = (random.randint(1,6) + random.randint(1,6)) + 12
        self.max_energy = self.initial_energy
        self.energy = self.initial_energy
        
        #Atributo sorte
        self.initial_luck = random.randint(1,6) + 6
        self.luck = self.initial_luck
        
        #outros atributos
        self.gold = 0
        self.provisions = 10
        self.inventory = []
        
        print(  f"""
                Personagem criado!
                Dados Iniciais do seu Aventureiro:
                HABILIDADE: {self.initial_skill}
                ENERGIA: {self.initial_energy}
                SORTE: {self.initial_luck}

                Boa sorte em sua jornada!
                """)
        
    def get_status(self):
        print(  f"""
                ==========STATUS==========
                Energia: {self.energy}/{self.initial_energy}
                Habilidade: {self.skill}/{self.initial_skill}
                Sorte: {self.luck}/{self.initial_luck}
                Ouro: {self.gold}
                Provisões: {self.provisions}
                Itens: {', '.join(self.inventory) if self.inventory else 'Nenhum'}
                ==========================
                """)
        
    def take_dmg(self, amount: int):
        self.energy -= amount
        print(f"""
                Dano recebido: {amount}
                Energia atual: {self.energy}
                """)
        if self.energy <= 0:
            print("Sua ENERGIA chegou a zero! Você desabou, derrotado. Fim de jogo.")
            return True
        return False
    
    def heal_energy(self, amount: int):
        self.energy += amount        
        if self.energy > self.max_energy:
            self.energy = self.max_energy
        print("Após comer, sua energia foi recuperada! Você se sente revigorado.")
    
    def remove_luck(self):
        if self.luck > 0:
            self.luck -= 1
            print(f"Sua SORTE diminuiu para {self.luck}.")
        else:
            print(f"Sua SORTE já está em {self.luck} e não pode diminuir mais. Você está azarado!")
        
    def increase_luck(self, amount: int):
        self.luck += amount
        if self.luck > self.initial_luck:
            self.luck = self.initial_luck
        print(f"Sua SORTE aumentou para {self.luck}")
        
    def increase_skill(self, amount: int):
        self.skill += amount
        if self.skill > self.initial_skill:
            self.skill = self.initial_skill
        print(f"Sua HABILIDADE aumentou para {self.skill}")

    def add_item(self, item_name: str):
        self.inventory.append(item_name)
        print(f"Você achou um(a): {item_name}!")
    
    def remove_item(self, item_name: str):
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            print(f"Você usou/perdeu: {item_name}!")
            return True
        else:
            print(f"Você não tem {item_name} no seu inventário.")
            return False
        
    def add_gold(self, amount: int):
        self.gold += amount
        print(f"você guardou {amount} OURO em seu bolso!")

    def spend_gold(self, amount: int):
        if self.gold >= amount:
            self.gold -= amount
            print(f"Você gastou {self.gold} OURO!")
        
        pass
