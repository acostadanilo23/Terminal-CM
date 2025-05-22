# data/monsters.py

# A lista de monstros do Calabouço da Morte com seus atributos base.
# Consideramos Habilidade (SKILL) e Energia (STAMINA) como os atributos principais.
# Outras notas (como imunidades ou efeitos especiais) serão processadas na lógica do combate
# ou em outras ações de parágrafo, não diretamente aqui nos atributos base.

MONSTERS_DATA = {
    "Vulto": {
        "habilidade": 6,
        "energia": 6,
        "notas": "Invisível."
    },
    "Aranha Gigante": { # Para as duas aranhas, você invocaria este tipo duas vezes
        "habilidade": 7,
        "energia": 6,
        "notas": "Em combate com duas delas, combata uma de cada vez."
    },
    "Orc": {
        "habilidade": 5,
        "energia": 5,
        "notas": ""
    },
    "Esqueleto": {
        "habilidade": 7,
        "energia": 5,
        "notas": ""
    },
    "Guerreiro Zumbi": {
        "habilidade": 7,
        "energia": 7,
        "notas": ""
    },
    "Goblin": {
        "habilidade": 5,
        "energia": 4,
        "notas": ""
    },
    "Morcego Gigante": {
        "habilidade": 6,
        "energia": 4,
        "notas": ""
    },
    "Vampiro": {
        "habilidade": 8,
        "energia": 8,
        "notas": "Se Energia < 4, tenta se transformar em Morcego para fugir (Parágrafo 159)."
    },
    "Verme da Lama": {
        "habilidade": 7,
        "energia": 7,
        "notas": ""
    },
    "Fantasma": {
        "habilidade": 8,
        "energia": 8,
        "notas": "Se falhar num Teste de Sorte quando atacado, perde 1 Sorte. Se passar, Fantasma é destruído."
    },
    "Guerreiro Esqueleto": {
        "habilidade": 8,
        "energia": 6,
        "notas": ""
    },
    "Homem-Lagarto": {
        "habilidade": 6,
        "energia": 7,
        "notas": ""
    },
    "Ogro": { # Para os dois ogros, você invocaria este tipo duas vezes
        "habilidade": 7,
        "energia": 8,
        "notas": "Em combate com dois, combata um de cada vez."
    },
    "Gárgula": {
        "habilidade": 8,
        "energia": 8,
        "notas": ""
    },
    "Gigante": {
        "habilidade": 9,
        "energia": 10,
        "notas": ""
    },
    "Homem-Porco": {
        "habilidade": 7,
        "energia": 6,
        "notas": ""
    },
    "Orc-Chefe": {
        "habilidade": 7,
        "energia": 6,
        "notas": ""
    },
    "Guerreiro Orc": {
        "habilidade": 6,
        "energia": 5,
        "notas": ""
    },
    "Vaporizador": {
        "habilidade": 8,
        "energia": 7,
        "notas": "Se atingido, perde 1 ENERGIA extra por estar atordoado."
    },
    "Centopeia Gigante": {
        "habilidade": 6,
        "energia": 6,
        "notas": ""
    },
    "Escorpião Gigante": {
        "habilidade": 8,
        "energia": 7,
        "notas": ""
    },
    "Criatura das Profundezas": {
        "habilidade": 9,
        "energia": 9,
        "notas": ""
    },
    "Monstro Espectro": {
        "habilidade": 9,
        "energia": 10,
        "notas": "Se perder um Teste de Sorte quando atacado, perde 2 Sorte. Se passar, apenas 1."
    },
    "Demônio da Cripta": {
        "habilidade": 10,
        "energia": 10,
        "notas": ""
    },
    "Morcego": { # Diferente do Morcego Gigante, são morcegos normais em bandos
        "habilidade": 5,
        "energia": 4,
        "notas": "Aparece em bandos, mas o combate é com um por vez (Parágrafo 303)."
    },
    "Lobisomem": {
        "habilidade": 8,
        "energia": 9,
        "notas": "Imune a ataques normais. Precisa de espada de prata para dano total."
    },
    "Minotauro": {
        "habilidade": 9,
        "energia": 9,
        "notas": ""
    },
    "Vigia-Chefe": { # Goblinoide
        "habilidade": 7,
        "energia": 7,
        "notas": ""
    },
    "Vigia": { # Goblinoide
        "habilidade": 6,
        "energia": 6,
        "notas": ""
    },
    "Demônio Alado": {
        "habilidade": 9,
        "energia": 8,
        "notas": ""
    },
    "Barão Sukumvit": {
        "habilidade": 12,
        "energia": 12,
        "notas": "Chefe final."
    }
}