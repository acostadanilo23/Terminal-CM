# Terminal-CM: O Calabouço da Morte

Uma réplica interativa baseada em texto para terminal do aclamado livro-jogo **"O Calabouço da Morte" (Deathtrap Dungeon)** de Ian Livingstone, parte da série *Fighting Fantasy* (Aventuras Fantásticas).

---

## 📖 Sobre o Jogo

O Baron Sukumvit construiu um labirinto letal sob a cidade de Fang, conhecido como o **Calabouço da Morte**. Repleto de armadilhas mortais, monstros horrendos e mistérios indecifráveis, o calabouço desafia anualmente os guerreiros mais bravos em uma caminhada rumo à sobrevivência. Apenas aquele que conseguir superar todos os desafios e sair do labirinto conquistará a recompensa de 10.000 peças de Ouro e a glória eterna.

Este projeto reconstrói toda a experiência no console de comandos do Windows (ou Linux/macOS), integrando rolagens de dados, combates ativos, testes de Sorte, mochila de itens/provisões, e as fichas clássicas do livro físico.

---

## 🛠️ Arquitetura do Projeto

O código está estruturado em módulos independentes organizados da seguinte forma:

*   **`main.py`**: O motor central do jogo. Gerencia os menus, a introdução narrativa, a criação de personagem, a mochila de itens e a navegação entre os 400 parágrafos.
*   **`character.py`**: Define o aventureiro (`Character`), seus atributos (Habilidade, Energia, Sorte), inventário de itens/jóias, o uso de provisões, o consumo de poções, e as telas visuais (Folha de Aventuras e Quadro de Encontros).
*   **`systems.py`**: Implementa as regras fundamentais do livro, como rolagens de dados com animação, o combate por turnos contra inimigos, e o teste de Sorte dinâmico.
*   **`parse_book.py`**: Um script utilitário inteligente. Lê o texto do livro de referência e extrai de forma estruturada todos os parágrafos, conexões de escolha, combates com monstros e eventos de sorte, salvando-os em formato JSON.
*   **`data/`**:
    *   `paragraphs.json`: A base estruturada gerada pelo parser contendo o texto e opções de cada parágrafo.
    *   `monters.py`: Banco de dados auxiliar com estatísticas de monstros comuns.
    *   `paragraphs.py` / `ascii_art.py`: Arquivos de arte estática e dados legados.

---

## 🚀 Como Jogar

### Pré-requisitos
Certifique-se de ter o Python 3 instalado no seu computador.

### Executando o Jogo
Abra o terminal na pasta do projeto e execute:
```bash
python main.py
# Ou no Windows:
py main.py
```

### (Opcional) Re-gerar Base do Livro
Caso altere o arquivo `livro-referencia.txt`, você pode rodar o parser para re-gerar a base estruturada:
```bash
py parse_book.py
```

---

## ⚔️ Mecânicas & Regras de Jogo

### Atributos do Aventureiro
*   **HABILIDADE** (Perícia com armas): Rola-se `1d6 + 6` ao criar o personagem. Usado principalmente no combate.
*   **ENERGIA** (Vitalidade/Vida): Rola-se `2d6 + 12` ao criar o personagem. Se cair para `0`, fim de jogo!
*   **SORTE** (Fortuna/Destino): Rola-se `1d6 + 6` ao criar o personagem. Usado para escapar de armadilhas e alterar dano no combate.

### Poções Iniciais
Ao começar o jogo, você escolhe **uma** poção mágica com uma dose única que restaura atributos:
1.  **Poção da Habilidade**: Restaura a HABILIDADE atual ao valor Inicial.
2.  **Poção da Força**: Restaura a ENERGIA atual ao valor Inicial (máximo).
3.  **Poção da Fortuna**: Restaura a SORTE atual ao novo valor Inicial e soma permanentemente +1 à sua SORTE Inicial.

### O Combate
1.  Você e a criatura rolam 2 dados (2d6).
2.  Sua **Força de Ataque (FA)** é igual a: `Resultado dos Dados + HABILIDADE`.
3.  A FA da criatura é igual a: `Resultado dos Dados + HABILIDADE dela`.
4.  O valor maior atinge o oponente e causa **2 de dano** na ENERGIA.

#### Testando a Sorte no Combate
Você pode escolher arriscar sua Sorte após os dados rolarem para tentar modificar o dano:
*   **Ao Atingir o Inimigo**:
    *   *Sucesso no teste:* Você causa um golpe crítico (4 de dano).
    *   *Falha no teste:* Você raspa no inimigo (causa apenas 1 de dano).
*   **Ao Ser Atingido**:
    *   *Sucesso no teste:* Você absorve o golpe (sofre apenas 1 de dano).
    *   *Falha no teste:* O golpe te pega em cheio (sofre 3 de dano).

> *Importante:* Cada teste de sorte consome 1 ponto do seu atributo SORTE atual, tornando testes subsequentes mais difíceis.

---

## 💾 Sistema de Salvamento (Save & Load)

O jogo oferece suporte a 3 slots de salvamento separados para que você não perca seu progresso no calabouço. Os arquivos de salvamento são persistidos na pasta `saves/` em formato JSON.

*   **Salvar o Jogo:** Pode ser feito digitando `salvar` (ou `save`) no prompt do parágrafo, ou acessando a Mochila (`mochila`) e escolhendo a opção **[5] Salvar Jogo**.
*   **Carregar o Jogo:** No Menu Principal, selecione a opção **[2] Carregar Jogo** para listar os slots disponíveis e carregar o progresso do parágrafo exato onde salvou.

---

## ⌨️ Controles do Jogo

Durante as leituras de parágrafos, você pode digitar os seguintes comandos especiais:

*   **`[número da opção]`**: Avança escolhendo o índice da opção correspondente listada no rodapé (ex: `1`, `2`).
*   **`mochila`** (ou **`m`**): Abre a tela com a Folha de Aventuras (ficha), Quadro de Encontros (combates), Provisões, Poções e a opção de salvar progresso.
*   **`salvar`** (ou **`save`**): Abre o menu rápido de seleção de slot para gravar o progresso atual.
*   **`status`** (ou **`s`**): Imprime no console seus atributos de forma compacta.
*   **`sair`** (ou **`q`**): Abandona o labirinto e volta ao menu principal.
