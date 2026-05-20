import re
import json
import os

def parse_reference_book():
    book_path = "livro-referencia.txt"
    output_path = os.path.join("data", "paragraphs.json")
    
    if not os.path.exists(book_path):
        print(f"Erro: {book_path} não encontrado!")
        return
        
    with open(book_path, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Separar a história/prólogo dos parágrafos de jogo
    # Os parágrafos começam após "AGORA VIRE A PÁGINA"
    parts = content.split("AGORA VIRE A PÁGINA")
    paragraphs_text = parts[1] if len(parts) > 1 else content
    
    # Expressão regular para encontrar as linhas que contêm apenas números de 1 a 400
    # Usando ^\d+\.?$ com a flag MULTILINE (permite um ponto opcional após o número, como "239.")
    pattern = re.compile(r'^\s*([1-9][0-9]{0,2}|400)\.?\s*$', re.MULTILINE)
    
    matches = list(pattern.finditer(paragraphs_text))
    print(f"Total de parágrafos detectados: {len(matches)}")
    
    paragraphs_data = {}
    
    for i in range(len(matches)):
        num = int(matches[i].group(1))
        start = matches[i].end()
        end = matches[i+1].start() if i + 1 < len(matches) else len(paragraphs_text)
        
        text = paragraphs_text[start:end].strip()
        
        # Regex para buscar opções de caminhos
        # Ex: "Se você quiser abrir a caixa, vá para 270"
        # Ex: "Esperará pela pergunta?  Vá para 382"
        # Ex: "Se você vencer, vá para 364"
        options = []
        
        # Quebrar em sentenças ou linhas para analisar de forma independente
        sentences = re.split(r'\.|\n', text)
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
                
            # Busca padrões como "vá para X", "volte para X", "fique em X" (ou variações como "vão para X")
            opt_match = re.search(r'(.*?)(?:[vV]á\s+para|[vV]olte\s+para|[fF]ique\s+em|[iI]r\s+para|[vV]ão\s+para)\s+(\d+)', sentence)
            if opt_match:
                label_prefix = opt_match.group(1).strip()
                dest = int(opt_match.group(2))
                
                # Tratar e limpar o label da opção
                # Remover caracteres indesejados no início (ex: vírgulas, hífens)
                label_prefix = re.sub(r'^[\s\-\,\;]+', '', label_prefix)
                
                # Se sobrar texto significativo no label, usamos
                if label_prefix and len(label_prefix) > 2:
                    label = f"{label_prefix} (ir para {dest})"
                else:
                    label = f"Ir para {dest}"
                    
                # Limpar espaços duplicados
                label = " ".join(label.split())
                
                # Evitar adicionar opções duplicadas para o mesmo destino no mesmo parágrafo
                if not any(o["destino"] == dest for o in options):
                    options.append({
                        "texto_opcao": label,
                        "destino": dest
                    })
        
        # Tentar detectar combates no parágrafo
        # Procurar por monstros com habilidade e energia descritos no parágrafo
        # Ex: "MANTÉCORA HABILIDADE 11 ENERGIA 11" ou similar
        acoes = []
        monster_match = re.search(r'([A-ZÇÃÕÁÉÍÓÚ\s\-]+)\s+HABILIDADE\s+(\d+)\s+ENERGIA\s+(\d+)', text, re.IGNORECASE)
        if monster_match:
            monster_name = monster_match.group(1).strip()
            # Limpar nomes de monstros que pegam linhas extras
            monster_name = " ".join(monster_name.split())
            if len(monster_name) > 3 and "VÁ" not in monster_name and "SE" not in monster_name:
                habilidade = int(monster_match.group(2))
                energia = int(monster_match.group(3))
                
                # Tentar encontrar para onde ir se vencer
                vitoria_dest = None
                vitoria_match = re.search(r'Se\s+(?:você\s+)?vencer[^\d]*?vá\s+para\s+(\d+)', text, re.IGNORECASE)
                if vitoria_match:
                    vitoria_dest = int(vitoria_match.group(1))
                else:
                    # Se não achou na busca padrão, pega a primeira opção do parágrafo como vitória
                    if options:
                        vitoria_dest = options[0]["destino"]
                
                acoes.append({
                    "tipo": "combate",
                    "monstro": {
                        "name": monster_name,
                        "habilidade": habilidade,
                        "energia": energia
                    },
                    "vitoria": vitoria_dest
                })
        
        # Testes de Sorte específicos (se aplicável)
        if "Teste sua Sorte" in text:
            # Tentar pegar destinos de sorte e azar
            sorte_match = re.search(r'Se\s+(?:você\s+)?tiver\s+sorte[^\d]*?vá\s+para\s+(\d+)', text, re.IGNORECASE)
            azar_match = re.search(r'Se\s+(?:você\s+)?não\s+tiver\s+sorte[^\d]*?vá\s+para\s+(\d+)', text, re.IGNORECASE)
            
            if sorte_match and azar_match:
                acoes.append({
                    "tipo": "teste_sorte",
                    "sucesso": int(sorte_match.group(1)),
                    "falha": int(azar_match.group(1))
                })
        
        paragraphs_data[num] = {
            "texto": text,
            "opcoes": options,
            "acoes": acoes
        }
        
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(paragraphs_data, f, ensure_ascii=False, indent=4)
        
    print(f"Parágrafos salvos com sucesso em {output_path}!")

if __name__ == "__main__":
    parse_reference_book()
