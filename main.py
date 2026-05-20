import os
import sys as _sys

# ========================
# CORREÇÃO DE ENCODING (Windows)
# Garante que caracteres acentuados (ã, ç, õ, é, etc.) sejam exibidos corretamente
# ========================
if _sys.platform == 'win32':
    os.system('chcp 65001 >nul 2>&1')
if hasattr(_sys.stdout, 'reconfigure'):
    _sys.stdout.reconfigure(encoding='utf-8')
if hasattr(_sys.stdin, 'reconfigure'):
    _sys.stdin.reconfigure(encoding='utf-8')

import json
import random
import time
import textwrap
from character import Character
import systems as game_sys
import data.monters as m

# ========================
# CONSTANTES E CONFIGURAÇÃO
# ========================
GAME_WIDTH = 80
PARAGRAPHS_JSON = os.path.join("data", "paragraphs.json")

# ========================
# ARTE ASCII DO TÍTULO
# ========================
_title_lines = [
    " ██████╗  █████╗ ██╗      █████╗ ██████╗  ██████╗ ██╗   ██╗ ██████╗  ██████╗ ",
    "██╔════╝ ██╔══██╗██║     ██╔══██╗██╔══██╗██╔═══██╗██║   ██║██╔════╝ ██╔═══██╗",
    "██║      ███████║██║     ███████║██████╔╝██║   ██║██║   ██║██║      ██║   ██║",
    "██║      ██╔══██║██║     ██╔══██║██╔══██╗██║   ██║██║   ██║██║      ██║   ██║",
    "╚██████╗ ██║  ██║███████╗██║  ██║██████╔╝╚██████╔╝╚██████╔╝╚██████╗ ╚██████╔╝",
    " ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝  ╚═════╝ ",
    "",
    "██████╗  █████╗ ",
    "██╔══██╗██╔══██╗",
    "██║  ██║███████║",
    "██║  ██║██╔══██║",
    "██████╔╝██║  ██║",
    "╚═════╝ ╚═╝  ╚═╝",
    "",
    "███╗   ███╗ ██████╗ ██████╗ ████████╗███████╗",
    "████╗ ████║██╔═══██╗██╔══██╗╚══██╔══╝██╔════╝",
    "██╔████╔██║██║   ██║██████╔╝   ██║   █████╗  ",
    "██║╚██╔╝██║██║   ██║██╔══██╗   ██║   ██╔══╝  ",
    "██║ ╚═╝ ██║╚██████╔╝██║  ██║   ██║   ███████╗",
    "╚═╝     ╚═╝ ╚═════╝ ╚═╝  ╚═╝   ╚═╝   ╚══════╝",
    "",
    "Baseado no livro-jogo de Ian Livingstone",
    '"Deathtrap Dungeon"'
]

def _generate_title_art():
    box_width = GAME_WIDTH
    inner_width = box_width - 4
    art = []
    art.append("╔" + "═" * (box_width - 2) + "╗")
    art.append("║" + " " * (box_width - 2) + "║")
    for line in _title_lines:
        centered = line.center(inner_width)
        art.append(f"║ {centered} ║")
    art.append("║" + " " * (box_width - 2) + "║")
    art.append("╚" + "═" * (box_width - 2) + "╝")
    return "\n".join(art)

TITLE_ART = _generate_title_art()

def print_menu_box(options, title=None, box_width=50):
    """Imprime uma caixa de menu centralizada na tela, com as opções alinhadas internamente."""
    left_margin = (GAME_WIDTH - box_width) // 2
    margin_spaces = " " * left_margin
    inner_width = box_width - 4
    
    print(margin_spaces + "┌" + "─" * (box_width - 2) + "┐")
    if title:
        header = title.center(inner_width)
        print(margin_spaces + f"│ {header} │")
        print(margin_spaces + "├" + "─" * (box_width - 2) + "┤")
        
    for opt in options:
        padded = f"   {opt}".ljust(inner_width)
        print(margin_spaces + f"│ {padded} │")
    print(margin_spaces + "└" + "─" * (box_width - 2) + "┘")

SEPARATOR = "═" * GAME_WIDTH

# ========================
# UTILITÁRIOS DE EXIBIÇÃO
# ========================
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def slow_print(text, delay=0.02):
    """Imprime texto caractere por caractere para efeito dramático."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def print_wrapped(text, width=GAME_WIDTH, indent="    "):
    """Imprime um bloco de texto formatado com quebra de linha e indentação esquerda."""
    text_clean = " ".join(text.strip().split())
    wrap_width = width - len(indent)
    wrapped = textwrap.fill(text_clean, width=wrap_width)
    for line in wrapped.split('\n'):
        print(indent + line)
    print()

def clean_option_text(text):
    import re
    # Remove "(ir para X)", "(volte para X)", "(fique em X)", "(vão para X)"
    text = re.sub(r'\s*\((?:ir|volte|fique|vão)\s+para\s+\d+\)', '', text, flags=re.IGNORECASE)
    # Remove "ir/volte/vá para X" at the end of the text
    text = re.sub(r'\s*(?:vá|volte|fique|vão|ir)\s+para\s+\d+\.?$', '', text, flags=re.IGNORECASE)
    text = text.strip()
    
    if not text or text.lower() in ["ir para", "volte para", "fique em", "avançar", "continuar"]:
        return "Continuar"
        
    if text.endswith(','):
        text = text[:-1].strip()
        
    return text

def clean_paragraph_text(text):
    import re
    if not text:
        return ""
    
    # Padroniza quebras de linha e espaços múltiplos
    text_normalized = text.replace('\r\n', '\n').replace('\r', '\n')
    
    # Regex abrangente para remover referências como "vá para 123", "volte ao parágrafo 50", "fique em 16", etc.
    pattern = r'(?:,\s*|;\s*|:\s*|-\s*|\s+)?\b(?:[vV]á|[vV]olte|[iI]r|[fF]ique|[fF]iquem|[vV]ão|[rR]etorne|[dD]irija-se)\s+(?:para\s+o\s+parágrafo\s+|para\s+o\s+número\s+|para\s+o\s+|para\s+o\s+|para\s+a\s+|para\s+|ao\s+|no\s+|em\s+|a\s+|o\s+)?\d+\b'
    
    cleaned = re.sub(pattern, "", text_normalized)
    
    # Limpa pontuações repetidas e espaços residuais antes de pontos
    cleaned = re.sub(r'\s*\.{2,}', '.', cleaned)
    cleaned = re.sub(r'\s+\.', '.', cleaned)
    cleaned = re.sub(r'\s+,', ',', cleaned)
    
    return cleaned

# ========================
# SISTEMA DE SALVAMENTO (SAVE & LOAD)
# ========================
def get_save_path(slot):
    """Retorna o caminho absoluto para o arquivo de save do slot fornecido."""
    import os
    base_dir = os.path.dirname(os.path.abspath(__file__))
    saves_dir = os.path.join(base_dir, "saves")
    if not os.path.exists(saves_dir):
        os.makedirs(saves_dir)
    return os.path.join(saves_dir, f"save_slot_{slot}.json")

def list_saves():
    """Retorna metadados das gravações existentes para exibição nos slots."""
    import os
    import json
    metadata = {}
    for slot in [1, 2, 3]:
        path = get_save_path(slot)
        if os.path.exists(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    data = json.load(f)
                metadata[slot] = {
                    "exists": True,
                    "paragraph": data.get("current_paragraph"),
                    "date": data.get("date", "Data desconhecida"),
                    "energy": data.get("player", {}).get("energy", "?"),
                    "max_energy": data.get("player", {}).get("max_energy", "?")
                }
            except Exception:
                metadata[slot] = {"exists": False}
        else:
            metadata[slot] = {"exists": False}
    return metadata

def save_game_state(player, current_paragraph, slot):
    """Salva o progresso do jogo (personagem e parágrafo atual) no slot fornecido."""
    import json
    from datetime import datetime
    try:
        path = get_save_path(slot)
        save_data = {
            "current_paragraph": current_paragraph,
            "date": datetime.now().strftime("%d/%m/%Y %H:%M"),
            "player": player.to_dict()
        }
        with open(path, "w", encoding="utf-8") as f:
            json.dump(save_data, f, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"    ⚠️ Erro ao salvar jogo: {e}")
        return False

def load_game_state(slot):
    """Carrega o progresso salvo no slot fornecido."""
    import json
    path = get_save_path(slot)
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        player = Character.from_dict(data["player"])
        current_paragraph = data["current_paragraph"]
        return player, current_paragraph
    except Exception as e:
        print(f"    ⚠️ Erro ao carregar jogo: {e}")
        return None

def dramatic_dice_roll(label, num_dice=1, bonus=0):
    """Simula uma rolagem dramática de dados com animação."""
    print(f"\n  Rolando {'dado' if num_dice == 1 else 'dados'} para {label}...", end='', flush=True)
    
    # Animação de dados rolando
    final_rolls = []
    for _ in range(num_dice):
        roll = 0
        for i in range(8):
            roll = random.randint(1, 6)
            print(f"\r  Rolando {'dado' if num_dice == 1 else 'dados'} para {label}... [ ", end='', flush=True)
            for j, r in enumerate(final_rolls):
                print(f"{r} ", end='', flush=True)
            print(f"{roll} ", end='', flush=True)
            # Preencher espaços restantes
            for _ in range(num_dice - len(final_rolls) - 1):
                print("? ", end='', flush=True)
            print("]", end='', flush=True)
            time.sleep(0.08 + i * 0.03)
        final_rolls.append(roll)
    
    total = sum(final_rolls) + bonus
    bonus_str = f" + {bonus}" if bonus else ""
    print(f"\r  Rolando {'dado' if num_dice == 1 else 'dados'} para {label}... [ {' '.join(str(r) for r in final_rolls)} ]{bonus_str} = {total}    ")
    time.sleep(0.5)
    return total

def print_box(text, width=GAME_WIDTH):
    """Imprime texto dentro de uma caixa decorativa."""
    lines = text.split('\n')
    inner_width = width - 4
    print("╔" + "═" * (width - 2) + "╗")
    for line in lines:
        padded = line.center(inner_width)
        print(f"║ {padded} ║")
    print("╚" + "═" * (width - 2) + "╝")

# ========================
# CARREGAMENTO DE DADOS
# ========================
def load_paragraphs():
    """Carrega os parágrafos do arquivo JSON gerado pelo parser."""
    if not os.path.exists(PARAGRAPHS_JSON):
        print(f"ERRO: Arquivo {PARAGRAPHS_JSON} não encontrado!")
        print("Execute 'python parse_book.py' primeiro para gerar os dados do livro.")
        return None
    
    with open(PARAGRAPHS_JSON, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

# ========================
# CRIAÇÃO DE PERSONAGEM
# ========================
def create_character():
    """Cria o personagem com rolagem dramática de dados e escolha de poção."""
    clear_screen()
    print_box("CRIAÇÃO DO AVENTUREIRO")
    print()
    slow_print("    Antes de embarcar na sua aventura, você deve determinar suas forças e fraquezas.", 0.015)
    slow_print("    Você possui uma espada e uma mochila contendo provisões para a viagem.", 0.015)
    print()
    input("    Pressione Enter para rolar seus atributos...")
    
    # Criar personagem (a classe Character já rola os dados internamente,
    # mas nós queremos a animação dramática. Vamos criar e sobrescrever.)
    player = Character.__new__(Character)
    
    # Rolar HABILIDADE
    skill_roll = dramatic_dice_roll("HABILIDADE", num_dice=1, bonus=6)
    player.initial_skill = skill_roll
    player.skill = skill_roll
    
    # Rolar ENERGIA
    energy_roll = dramatic_dice_roll("ENERGIA", num_dice=2, bonus=12)
    player.initial_energy = energy_roll
    player.max_energy = energy_roll
    player.energy = energy_roll
    
    # Rolar SORTE
    luck_roll = dramatic_dice_roll("SORTE", num_dice=1, bonus=6)
    player.initial_luck = luck_roll
    player.luck = luck_roll
    
    # Inicializar os outros atributos
    player.gold = 0
    player.provisions = 10
    player.inventory = []
    player.jewels = []
    player.potion = None
    player.potion_uses = 0
    player.combat_history = []
    
    print(f"\n{SEPARATOR}")
    print_box(f"HABILIDADE: {player.skill}\nENERGIA: {player.energy}\nSORTE: {player.luck}")
    
    # Escolha de Poção
    print()
    slow_print("    Além disso, você poderá levar uma garrafa com uma poção mágica.", 0.015)
    slow_print("    Cada garrafa contém o bastante para uma dose. Escolha com sabedoria!", 0.015)
    print()
    
    potion_options = [
        "[1] Poção da Habilidade - Repõe a HABILIDADE",
        "[2] Poção da Força      - Repõe a ENERGIA",
        "[3] Poção da Fortuna    - Repõe a SORTE (+1 Inicial)"
    ]
    print_menu_box(potion_options, box_width=60)
    
    while True:
        choice = input("\n" + " " * 10 + "Escolha sua poção (1/2/3): ").strip()
        if choice == '1':
            player.potion = "Poção da Habilidade"
            player.potion_uses = 1
            print("\n    Você escolheu a Poção da Habilidade! Guarde-a bem.")
            break
        elif choice == '2':
            player.potion = "Poção da Força"
            player.potion_uses = 1
            print("\n    Você escolheu a Poção da Força! Ela pode salvar sua vida.")
            break
        elif choice == '3':
            player.potion = "Poção da Fortuna"
            player.potion_uses = 1
            print("\n    Você escolheu a Poção da Fortuna! Que a sorte lhe sorria.")
            break
        else:
            print("    Opção inválida. Escolha 1, 2 ou 3.")
    
    input("\n    Pressione Enter para iniciar sua aventura...")
    return player

# ========================
# PRÓLOGO / INTRODUÇÃO
# ========================
def show_prologue():
    """Exibe a história introdutória do livro."""
    clear_screen()
    
    prologue_texts = [
        """Fang era uma cidade pequena e comum na província setentrional de Chiang Mai. 
        Situada às margens do rio Kok, constituía-se num ponto de parada conveniente 
        para os comerciantes e passageiros que se deslocavam pelo rio durante a maior 
        parte do ano.""",
        
        """Todo ano, no dia 10 de maio, guerreiros e heróis vêm para Fang, a fim de 
        enfrentar a prova mais importante de suas vidas. A sobrevivência é improvável, 
        todavia muitos correm o risco, pois o prêmio é excelente – uma bolsa de 10 mil 
        Peças de Ouro e a libertação de Chiang Mai.""",
        
        """Tendo visto um dos comunicados de Sukumvit pregado em uma árvore, você resolve 
        que este ano tentará "A Caminhada". Reunindo uns poucos pertences, você parte 
        imediatamente rumo a Fang.""",
        
        """Segurando o lenço roxo bem alto, você enche os pulmões de ar fresco e puro uma 
        última vez antes de se virar para passar entre os pilares de pedra e penetrar no 
        labirinto do poderoso Barão Sukumvit, a fim de enfrentar perigos desconhecidos 
        na "Caminhada" pelo Calabouço da Morte."""
    ]
    
    print_box("O CALABOUÇO DA MORTE\nUma aventura de Ian Livingstone")
    print()
    
    for i, text in enumerate(prologue_texts):
        print_wrapped(text)
        if i < len(prologue_texts) - 1:
            input("    [Pressione Enter para continuar...]")
            print()
    
    print(f"\n{SEPARATOR}")
    input("\n    A aventura começa agora! Pressione Enter...\n")

# ========================
# MENU DA MOCHILA
# ========================
def show_save_screen(player, current_paragraph):
    """Exibe o menu interativo para salvar o progresso em um dos slots."""
    while True:
        clear_screen()
        saves = list_saves()
        
        options = []
        for slot in [1, 2, 3]:
            meta = saves[slot]
            if meta["exists"]:
                label = f"Slot {slot} - Parágrafo {meta['paragraph']} ({meta['date']}) [Vida: {meta['energy']}/{meta['max_energy']}]"
            else:
                label = f"Slot {slot} - Vazio"
            options.append(label)
        options.append("[0] Voltar")
        
        print_menu_box(options, title="ESCOLHA UM SLOT PARA SALVAR", box_width=65)
        choice = input("\n" + " " * 15 + "Escolha: ").strip()
        
        if choice in ['1', '2', '3']:
            slot_num = int(choice)
            clear_screen()
            print()
            print_box(f"Salvando no Slot {slot_num}...")
            if save_game_state(player, current_paragraph, slot_num):
                print("\n    ✅ Jogo salvo com sucesso!")
            else:
                print("\n    ❌ Falha ao salvar o jogo.")
            time.sleep(1.5)
            break
        elif choice == '0':
            break
        else:
            print("    Opção inválida.")
            time.sleep(0.5)

def show_load_screen():
    """Exibe o menu interativo para carregar um progresso salvo. Retorna (player, current_paragraph) ou None."""
    while True:
        clear_screen()
        saves = list_saves()
        
        options = []
        for slot in [1, 2, 3]:
            meta = saves[slot]
            if meta["exists"]:
                label = f"Slot {slot} - Parágrafo {meta['paragraph']} ({meta['date']}) [Vida: {meta['energy']}/{meta['max_energy']}]"
            else:
                label = f"Slot {slot} - Vazio"
            options.append(label)
        options.append("[0] Voltar")
        
        print_menu_box(options, title="ESCOLHA UM SLOT PARA CARREGAR", box_width=65)
        choice = input("\n" + " " * 15 + "Escolha: ").strip()
        
        if choice in ['1', '2', '3']:
            slot_num = int(choice)
            if not saves[slot_num]["exists"]:
                print("    ⚠️ Este slot está vazio!")
                time.sleep(1.0)
                continue
            
            clear_screen()
            print()
            print_box(f"Carregando Slot {slot_num}...")
            loaded = load_game_state(slot_num)
            if loaded:
                print("\n    ✅ Jogo carregado com sucesso!")
                time.sleep(1.5)
                return loaded
            else:
                print("\n    ❌ Falha ao carregar o jogo.")
                time.sleep(1.5)
        elif choice == '0':
            return None
        else:
            print("    Opção inválida.")
            time.sleep(0.5)

def backpack_menu(player, current_paragraph):
    """Menu interativo para gerenciar inventário, provisões e poções."""
    while True:
        clear_screen()
        options = [
            "[1] Folha de Aventuras (Ficha)",
            "[2] Quadro de Encontros (Combates)",
            "[3] Usar Provisão (+4 Energia)",
            "[4] Beber Poção",
            "[5] Salvar Jogo",
            "[0] Voltar à aventura"
        ]
        print_menu_box(options, title="MOCHILA DO AVENTUREIRO", box_width=50)
        
        choice = input("\n" + " " * 15 + "Escolha: ").strip()
        
        if choice == '1':
            clear_screen()
            player.show_status()
            input("    Pressione Enter para voltar...")
        elif choice == '2':
            clear_screen()
            player.show_combat_history()
            input("    Pressione Enter para voltar...")
        elif choice == '3':
            player.use_provision()
            input("\n    Pressione Enter para continuar...")
        elif choice == '4':
            player.drink_potion()
            input("\n    Pressione Enter para continuar...")
        elif choice == '5':
            show_save_screen(player, current_paragraph)
        elif choice == '0':
            break
        else:
            print("    Opção inválida.")
            time.sleep(0.5)

# ========================
# PROCESSAMENTO DE AÇÕES
# ========================
def process_actions(player, paragraph_data):
    """Processa as ações automáticas de um parágrafo (combates, testes de sorte, etc.)."""
    acoes = paragraph_data.get("acoes", [])
    
    for acao in acoes:
        if isinstance(acao, dict):
            tipo = acao.get("tipo", "")
            
            if tipo == "combate":
                monster_info = acao.get("monstro", {})
                vitoria_dest = acao.get("vitoria")
                
                print(f"\n{SEPARATOR}")
                print(f"  ⚔️  COMBATE! Você enfrenta: {monster_info.get('name', 'Criatura Desconhecida')}!")
                print(f"{SEPARATOR}")
                input("  Pressione Enter para iniciar o combate...")
                
                result = game_sys.start_combat(player, monster_info)
                
                if not result:
                    # Jogador morreu
                    return "morte"
                elif vitoria_dest:
                    return vitoria_dest
            
            elif tipo == "teste_sorte":
                print(f"\n{SEPARATOR}")
                print("  🎲 Teste sua Sorte!")
                print(f"{SEPARATOR}")
                input("  Pressione Enter para testar sua sorte...")
                
                result = game_sys.luck_test(player)
                if result:
                    dest = acao.get("sucesso")
                    if dest:
                        print(f"\n  Você teve sorte! Seguindo para o parágrafo {dest}...")
                        input("  Pressione Enter...")
                        return dest
                else:
                    dest = acao.get("falha")
                    if dest:
                        print(f"\n  Você não teve sorte... Seguindo para o parágrafo {dest}...")
                        input("  Pressione Enter...")
                        return dest
    
    return None

# ========================
# LOOP PRINCIPAL DO JOGO
# ========================
def game_loop(player, paragraphs, start_paragraph=1):
    """Loop principal do jogo: exibe parágrafos, processa escolhas e ações."""
    current_paragraph = start_paragraph
    game_over = False
    
    while not game_over:
        clear_screen()
        
        para_key = str(current_paragraph)
        
        if para_key not in paragraphs:
            print(f"\n    ⚠️  Erro: Conteúdo não disponível para prosseguir.")
            input("\n    Pressione Enter para voltar ao menu principal...")
            return False
        
        para_data = paragraphs[para_key]
        
        # Exibir cabeçalho decorativo limpo (sem revelar o número do parágrafo)
        print(f"╔{'═' * (GAME_WIDTH - 2)}╗")
        print(f"║ {'O CALABOUÇO DA MORTE'.center(GAME_WIDTH - 4)} ║")
        print(f"╚{'═' * (GAME_WIDTH - 2)}╝")
        print()
        
        # Exibir o texto do parágrafo limpo de números de parágrafos
        print_wrapped(clean_paragraph_text(para_data.get("texto", "")))
        
        # Processar ações automáticas (combates, testes de sorte)
        action_result = process_actions(player, para_data)
        
        if action_result == "morte":
            print(f"\n{SEPARATOR}")
            print_box("GAME OVER\nSua aventura termina aqui...")
            print(f"{SEPARATOR}")
            input("\n    Pressione Enter para voltar ao menu principal...")
            return False
        elif action_result is not None:
            # Ação retornou um destino (ex: vitória em combate, teste de sorte)
            current_paragraph = int(action_result)
            continue
        
        # Verificar vitória (parágrafo 400)
        if current_paragraph == 400:
            print(f"\n{SEPARATOR}")
            print_box("VITÓRIA!\nVocê é o Campeão do Calabouço da Morte!")
            print(f"{SEPARATOR}")
            input("\n    Pressione Enter para voltar ao menu principal...")
            return True
        
        # Exibir opções disponíveis
        opcoes = para_data.get("opcoes", [])
        
        print(f"{'─' * GAME_WIDTH}")
        print()
        
        if opcoes:
            print("    Suas opções:")
            for i, opcao in enumerate(opcoes, 1):
                texto = opcao.get("texto_opcao", "Avançar")
                # Limpa qualquer menção a números de parágrafos nas opções
                texto_limpo = clean_option_text(texto)
                print(f"      [{i}] {texto_limpo}")
        
        print()
        print("    Comandos: [mochila / m] Mochila | [salvar] Salvar | [sair / q] Sair")
        print()
        
        # Receber entrada do jogador
        choice = input("    ➤ Sua escolha: ").strip().lower()
        
        if choice in ['mochila', 'm']:
            backpack_menu(player, current_paragraph)
            continue
        elif choice in ['salvar', 'save']:
            show_save_screen(player, current_paragraph)
            continue
        elif choice in ['status', 's']:
            clear_screen()
            player.show_status()
            input("    Pressione Enter para voltar...")
            continue
        elif choice in ['sair', 'q']:
            confirm = input("    Tem certeza que deseja sair? (s/n): ").strip().lower()
            if confirm == 's':
                game_over = True
            continue
        
        # Verificar se é uma opção numérica das listadas
        try:
            choice_num = int(choice)
            
            # Verificar se é um índice de opção listada
            if opcoes and 1 <= choice_num <= len(opcoes):
                dest = opcoes[choice_num - 1].get("destino")
                if dest:
                    current_paragraph = dest
                    continue
            
            print("    Opção inválida. Escolha um dos números listados.")
            time.sleep(1.5)
        except ValueError:
            print("    Entrada inválida. Digite o número de uma das opções acima.")
            time.sleep(1.5)

# ========================
# MENU PRINCIPAL
# ========================
def main_menu():
    """Menu principal do jogo."""
    paragraphs = load_paragraphs()
    if not paragraphs:
        return
    
    while True:
        clear_screen()
        print(TITLE_ART)
        print()
        options = [
            "[1] Iniciar Nova Aventura",
            "[2] Carregar Jogo",
            "[3] Como Jogar",
            "[4] Sair"
        ]
        print_menu_box(options, box_width=50)
        
        choice = input("\n" + " " * 15 + "Escolha: ").strip()
        
        if choice == '1':
            show_prologue()
            player = create_character()
            game_loop(player, paragraphs)
        elif choice == '2':
            loaded = show_load_screen()
            if loaded:
                player, start_paragraph = loaded
                game_loop(player, paragraphs, start_paragraph)
        elif choice == '3':
            clear_screen()
            print_box("COMO JOGAR - INSTRUÇÕES")
            print()
            print("    O QUE É O JOGO?")
            print_wrapped(
                "Este é um RPG de terminal baseado no livro-jogo clássico 'O Calabouço da Morte' "
                "(Deathtrap Dungeon) de Ian Livingstone. Você guiará seu aventureiro por um labirinto "
                "subterrâneo mortal repleto de monstros, armadilhas e enigmas. Seu objetivo é navegar "
                "pelas escolhas e perigos para alcançar o final (parágrafo 400) com vida!",
                indent="    "
            )
            
            print("    COMO JOGAR & ATRIBUTOS")
            print_wrapped(
                "No início, seus atributos serão gerados rolando dados:\n"
                "• HABILIDADE (1d6 + 6): Determina sua força física e destreza em combate.\n"
                "• ENERGIA (2d6 + 12): Representa sua vida e resistência. Se chegar a 0, você morre!\n"
                "• SORTE (1d6 + 6): Mede quão sortudo você é. Usada para testes e para alterar danos.\n\n"
                "Você também escolhe uma Poção Mágica (Habilidade, Força ou Fortuna) que pode ser "
                "consumida uma vez durante sua jornada para restaurar completamente o atributo correspondente.",
                indent="    "
            )
            
            print("    MECÂNICAS & COMBATE")
            print_wrapped(
                "• Teste de Sorte: Role 2d6. Se o resultado for menor ou igual à sua SORTE atual, você teve sorte! "
                "Independentemente do resultado, sua SORTE é reduzida em 1 ponto logo em seguida.\n"
                "• Combate por Turnos: Você e seu oponente rolam 2d6 e somam à Habilidade correspondente. "
                "Quem tiver a maior Força de Ataque (FA) vence o turno e causa 2 pontos de dano na Energia do outro.\n"
                "• Usar Sorte no Combate: Após o resultado de um turno, você pode arriscar sua Sorte:\n"
                "  - Ao Atingir: Sucesso causa +2 de dano (total 4). Falha causa -1 de dano (total 1).\n"
                "  - Ao Ser Atingido: Sucesso absorve 1 de dano (sofre 1). Falha aumenta +1 de dano (sofre 3).",
                indent="    "
            )
            
            print("    CONTROLES E COMANDOS DURANTE A JORNADA:")
            print()
            controls_options = [
                "[número]  - Digite o número correspondente à opção",
                "mochila   - Abre a Mochila (Ficha, Histórico, Poções, Salvar)",
                "salvar    - Abre menu de salvamento rápido",
                "status    - Exibe seus atributos rapidamente no console",
                "sair / q  - Abandona a aventura e volta ao menu"
            ]
            print_menu_box(controls_options, box_width=60)
            print()
            input("    Pressione Enter para voltar ao menu principal...")
        elif choice == '4':
            clear_screen()
            print("\n    Que a sorte dos deuses esteja com você, aventureiro!")
            print("    Até a próxima...\n")
            break
        else:
            print("    Opção inválida.")
            time.sleep(0.5)

# ========================
# PONTO DE ENTRADA
# ========================
if __name__ == "__main__":
    main_menu()
