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
        self.jewels = []
        self.potion = None
        self.potion_uses = 0
        self.combat_history = []  # Lista de dicts: {name, hab, ene, resultado}
        
        print(  f"""
                Personagem criado!
                Dados Iniciais do seu Aventureiro:
                HABILIDADE: {self.initial_skill}
                ENERGIA: {self.initial_energy}
                SORTE: {self.initial_luck}

                Boa sorte em sua jornada!
                """)
        
    def show_status(self):
        """Exibe a Folha de Aventuras no estilo do livro."""
        w = 80
        print()
        print("╔" + "═" * (w - 2) + "╗")
        print("║" + " FOLHA DE AVENTURAS ".center(w - 2) + "║")
        print("╠" + "═" * (w - 2) + "╣")
        print("║" + " " * (w - 2) + "║")
        # Linha dos 3 atributos principais
        hab_str  = f"HABILIDADE: {self.skill}/{self.initial_skill}"
        ene_str  = f"ENERGIA: {self.energy}/{self.max_energy}"
        sort_str = f"SORTE: {self.luck}/{self.initial_luck}"
        cols = f"{hab_str}  │  {ene_str}  │  {sort_str}"
        print("║" + cols.center(w - 2) + "║")
        # Sub-linha dos valores iniciais
        hab_i  = f"Inicial: {self.initial_skill}"
        ene_i  = f"Inicial: {self.initial_energy}"
        sort_i = f"Inicial: {self.initial_luck}"
        cols_i = f"{hab_i.center(len(hab_str))}  │  {ene_i.center(len(ene_str))}  │  {sort_i.center(len(sort_str))}"
        print("║" + cols_i.center(w - 2) + "║")
        print("║" + " " * (w - 2) + "║")
        print("╠" + "─" * (w - 2) + "╣")
        # Seção de equipamentos e recursos
        items_label = "ITENS / EQUIPAMENTOS"
        print("║" + items_label.center(w - 2) + "║")
        print("╠" + "─" * (w - 2) + "╣")
        if self.inventory:
            for item in self.inventory:
                line = f"  • {item}"
                print("║" + line.ljust(w - 2) + "║")
        else:
            print("║" + "  (Nenhum)".ljust(w - 2) + "║")
        print("║" + " " * (w - 2) + "║")
        print("╠" + "─" * (w - 2) + "╣")
        # Ouro e Jóias
        gold_line = f"  OURO: {self.gold} peças"
        print("║" + gold_line.ljust(w - 2) + "║")
        jewels_str = ", ".join(self.jewels) if self.jewels else "(Nenhuma)"
        jewels_line = f"  JÓIAS: {jewels_str}"
        print("║" + jewels_line.ljust(w - 2) + "║")
        print("║" + " " * (w - 2) + "║")
        print("╠" + "─" * (w - 2) + "╣")
        # Poções
        potion_name = self.potion if self.potion else "Nenhuma"
        potion_line = f"  POÇÕES: {potion_name} ({self.potion_uses} dose)"
        print("║" + potion_line.ljust(w - 2) + "║")
        print("║" + " " * (w - 2) + "║")
        print("╠" + "─" * (w - 2) + "╣")
        # Provisões
        prov_bar = "█" * self.provisions + "░" * (10 - self.provisions)
        prov_line = f"  PROVISÕES RESTANTES: {self.provisions}/10  [{prov_bar}]"
        print("║" + prov_line.ljust(w - 2) + "║")
        print("║" + " " * (w - 2) + "║")
        print("╚" + "═" * (w - 2) + "╝")
        print()

    def show_combat_history(self):
        """Exibe o Quadro de Encontros com Monstros no estilo do livro."""
        w = 80
        print()
        print("╔" + "═" * (w - 2) + "╗")
        print("║" + " QUADRO DE ENCONTROS COM MONSTROS ".center(w - 2) + "║")
        print("╠" + "═" * (w - 2) + "╣")
        
        if not self.combat_history:
            print("║" + "  Nenhum combate registrado ainda.".ljust(w - 2) + "║")
        else:
            # Cabeçalho da tabela
            header = f"  {'#':<5} {'CRIATURA':<28} {'HAB':>7}  {'ENE':>7}  {'RESULTADO':<20}"
            print("║" + header.ljust(w - 2) + "║")
            print("║" + ("  " + "─" * (w - 6)).ljust(w - 2) + "║")
            
            for i, fight in enumerate(self.combat_history, 1):
                name = fight['name'][:26]
                hab = str(fight['hab'])
                ene = str(fight['ene'])
                resultado = fight.get('resultado', '?')
                
                if resultado == 'vitória':
                    icon = '✓ VITÓRIA'
                elif resultado == 'derrota':
                    icon = '✗ DERROTA'
                elif resultado == 'fuga':
                    icon = '⇤ FUGA'
                else:
                    icon = resultado
                
                line = f"  {i:<5} {name:<28} {hab:>7}  {ene:>7}  {icon:<20}"
                print("║" + line.ljust(w - 2) + "║")
        
        print("║" + " " * (w - 2) + "║")
        # Resumo
        total = len(self.combat_history)
        vitorias = sum(1 for f in self.combat_history if f.get('resultado') == 'vitória')
        derrotas = sum(1 for f in self.combat_history if f.get('resultado') == 'derrota')
        fugas = sum(1 for f in self.combat_history if f.get('resultado') == 'fuga')
        print("╠" + "─" * (w - 2) + "╣")
        summary = f"  Total: {total}  │  Vitórias: {vitorias}  │  Derrotas: {derrotas}  │  Fugas: {fugas}"
        print("║" + summary.ljust(w - 2) + "║")
        print("╚" + "═" * (w - 2) + "╝")
        print()
        
    def take_dmg(self, amount: int):
        self.energy -= amount
        print(f"    Dano recebido: {amount}")
        print(f"    Energia atual: {self.energy}")
        if self.energy <= 0:
            print("    Sua ENERGIA chegou a zero! Você desabou, derrotado. Fim de jogo.")
            return True
        return False
    
    def heal_energy(self, amount: int):
        self.energy += amount        
        if self.energy > self.max_energy:
            self.energy = self.max_energy
            print(f"    Você se sente revigorado ao máximo! Energia atual: {self.energy}/{self.max_energy}")
        else:
            print(f"    Você recuperou {amount} de ENERGIA. Energia atual: {self.energy}/{self.max_energy}")    
            
    def remove_luck(self):
        if self.luck > 0:
            self.luck -= 1
            print(f"    Sua SORTE diminuiu para {self.luck}.")
        else:
            print(f"    Sua SORTE já está em {self.luck} e não pode diminuir mais. Você está azarado!")
        
    def increase_luck(self, amount: int):
        self.luck += amount
        if self.luck > self.initial_luck:
            self.luck = self.initial_luck
        print(f"    Sua SORTE aumentou para {self.luck}")
        
    def increase_skill(self, amount: int):
        self.skill += amount
        if self.skill > self.initial_skill:
            self.skill = self.initial_skill
        print(f"    Sua HABILIDADE aumentou para {self.skill}")

    def add_item(self, item_name: str):
        self.inventory.append(item_name)
        print(f"    Você achou um(a): {item_name}!")
    
    def remove_item(self, item_name: str):
        if item_name in self.inventory:
            self.inventory.remove(item_name)
            print(f"    Você usou/perdeu: {item_name}!")
            return True
        else:
            print(f"    Você não tem {item_name} no seu inventário.")
            return False
        
    def add_gold(self, amount: int):
        self.gold += amount
        print(f"    Você encontrou {amount} peças de OURO. Total em seu bolso: {self.gold}!")

    def spend_gold(self, amount: int):
        if self.gold >= amount:
            self.gold -= amount
            print(f"    Você gastou {amount} OURO! Total em seu bolso: {self.gold}!")
            return True
        else:
            print(f"    Você tem apenas {self.gold}, isto não é suficiente!")
            return False
        
    def use_provision(self):
        if self.provisions > 0:
            self.provisions -= 1
            self.heal_energy(4)
            print(f"    Você usou uma provisão. Restam {self.provisions} provisão(ões).")
            return True
        else:
            print("    Você não tem provisões restantes para usar.")
            return False

    def drink_potion(self):
        if not self.potion or self.potion_uses <= 0:
            print("    Você não tem nenhuma dose de poção restante!")
            return False
        
        self.potion_uses -= 1
        print(f"\n    Você bebeu a {self.potion}!")
        
        if self.potion == "Poção da Habilidade":
            self.skill = self.initial_skill
            print(f"    Sua HABILIDADE foi restaurada para o máximo ({self.skill})!")
        elif self.potion == "Poção da Força":
            self.energy = self.max_energy
            print(f"    Sua ENERGIA foi restaurada para o máximo ({self.energy})!")
        elif self.potion == "Poção da Fortuna":
            self.initial_luck += 1
            self.luck = self.initial_luck
            print(f"    Sua SORTE Inicial aumentou para {self.initial_luck} e a atual foi restaurada para o máximo ({self.luck})!")
        return True

    def to_dict(self):
        """Converte o estado do personagem em um dicionário para salvamento."""
        return {
            "initial_skill": self.initial_skill,
            "skill": self.skill,
            "initial_energy": self.initial_energy,
            "max_energy": self.max_energy,
            "energy": self.energy,
            "initial_luck": self.initial_luck,
            "luck": self.luck,
            "gold": self.gold,
            "provisions": self.provisions,
            "inventory": self.inventory,
            "jewels": self.jewels,
            "potion": self.potion,
            "potion_uses": self.potion_uses,
            "combat_history": self.combat_history
        }

    @classmethod
    def from_dict(cls, data):
        """Reconstrói uma instância de Character a partir de um dicionário."""
        player = cls.__new__(cls)
        player.initial_skill = data["initial_skill"]
        player.skill = data["skill"]
        player.initial_energy = data["initial_energy"]
        player.max_energy = data["max_energy"]
        player.energy = data["energy"]
        player.initial_luck = data["initial_luck"]
        player.luck = data["luck"]
        player.gold = data["gold"]
        player.provisions = data["provisions"]
        player.inventory = data["inventory"]
        player.jewels = data["jewels"]
        player.potion = data.get("potion")
        player.potion_uses = data.get("potion_uses", 0)
        player.combat_history = data.get("combat_history", [])
        return player

