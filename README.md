**Pygame desenvolvido por: Gabriel Michinhote, Henrique Melo, Juliana Pires**

**Inspirado em uma junção de clássicos como "Super Mário Bros", "Sônic" e "Halo", contendo referências a jogos mais contemporâneos também como "Roblox". É um jogo 2D de plataformas cujo objetivo é matar inimigos, coletar moedas e, acima de tudo, chegar ao final no menor tempo possível.**

**Nos baseamos principalmente em vídeos no YouTube (https://www.youtube.com/watch?v=nCk4zEL15dM) e precisamos também de algumas instruções de IA (o que seriam "tuplas" e como usá-las, além de pedir instruções de como agregar sons ao jogo, não só isso, como também o modo correto de utilizar "Houver").** 

**O jogo precisa dos seguintes arquivos no mesmo diretório:**

* Musicatema.wav
* mario.wav
* jump.wav, coin.wav, gameover.wav, morteinimigo.wav, mortejogador.way (sons)
*  sonic_parado_d.png, sonic_parado.e.png, sonic_corrend0_d.png, sonic_correndo_e.png
* img dos inimigos: inimigo2.png
* fundo do menu: sonic_fundo.png
* pastas/arquivos usados pelo map.py (tilemap, imagens das tiles, etc.)
* fontes TTF usadas no código: NiseJSRF.ttf, BloomsFree.ttf, Westland.ttf (se não existirem, o jogo tentará usar fontes do sistema)
* imagens de moedas opcionais: assets/coin1.png
* ranking.json (criado automaticamente para salvar os melhores tempos)


**MODO DE EXECUÇÃO**

1. Clone ou baixe o repositório
2. Instale: pip install pygame
3. Execute o script principal (main.py)


**CONTROLES** 

* Seta esquerda / A: mover para a esquerda
* Seta direita / D: mover para a direita
* Seta para cima / W / SPACE: pular (apenas quando estiver no chão)
* ESC: volta ao menu / fecha o jogo dependendo do estado
* R (na tela de ranking ou game over): voltar / reiniciar dependendo do estado


**COMO JOGAR**

* Ao clicar em 'Jogar', o jogo inicia e a dinâmica é simples, completar a fase no menor tempo possível, coletando as moedas e/ou eliminando os inimigos pulando em cima deles. Evite cair nos buracos ou bater de frente com os monstros. 


**ESTRUTURA**

* main.py -- loop principal, tela inicial, regras, inputs e HUD.
* map.py -- tiles e funções auxiliares para o funcionamento do jogo.
* assets/ -- imagens, sprites, sons, músicas, fontes.
----> assets: https://www.myinstants.com/pt/search/?name=sonic , https://www.dafont.com/pt/new.php , as imagens são autorais.

**PROBLEMAS E SOLUÇÕES**

* Tela preta ou erro na imagem -- verifique o caminho das imagens e sprites, se batem com o código principal.
* Fontes -- caso as fontes não estejam disponíveis, copie as TTF para o diretório.
* Erro de som -- verifique o caminho dos arquivos .wav.


**CRÉDITOS**

* Criado com Python e pygame.
* Professor Filipe Resina e Ninja Davi.


