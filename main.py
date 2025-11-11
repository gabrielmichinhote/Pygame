import pygame
import sys
import random

# TELA COM COMEÇAR, SAIR, REGRAS, ETC.

#Inicializa o pygame
pygame.init()
LARG, ALT = 800, 600

clock = pygame.time.Clock()
FONT_BIG = pygame.font.SysFont("arial", 64)
FONT_MED = pygame.font.SysFont("arial", 36)
FONT_PEQ = pygame.font.SysFont("arial", 24)
MAP_WIDTH = 5000
#CORES USADAS 
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)   
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (128, 128, 128)

camera_x = 0

# Começamos com fullscreen no monitor
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Super Sônico")
LARG, ALT = tela.get_size()  # atualiza LARG e ALT p o tamanho real da tela

#Estrutura inicial dos dados
game = True

# Pode ser 'menu', 'jogando', 'regras', 'sair'
estado = 'menu'  

# SURF (surface) refere-se a tela
def desenho_textcent(tela, texto, fonte, cor, y):
    surf = fonte.render(texto, True, cor)
    rect = surf.get_rect(center=(LARG // 2, y))
    tela.blit(surf, rect) #desenha o blit usando o rect como referencia p posição
    return rect

# Função para criar botões
def botao(tela, rect, texto, fonte, cor_t, cor_f, houver = False):
    nova_cor = []
    for c in cor_f:
        if houver:
            valor = c * 1.1
        else:
            valor = c * 1.0
        valor = int(valor)
        if valor > 225:
            valor = 225
        nova_cor.append(valor)
    cor_display = tuple(nova_cor) #pesquisei sobre tuplas

    pygame.draw.rect(tela, cor_display, rect, border_radius=8)
    pygame.draw.rect(tela, PRETO, rect, 3, border_radius=8)
    surf = fonte.render(texto, True, cor_t)
    r = surf.get_rect(center=rect.center)
    tela.blit(surf, r)

#TAMANHO DOS BOTÕES
btn_larg, btn_alt = 300, 65
btn_x = (LARG - btn_larg) // 2 #p centralizar horizontalmente
btn_gap = 20

#RETANGULOS DOS BOTOES D MENU
btn_jogar = pygame.Rect(btn_x, 200, btn_larg, btn_alt)
btn_regras = pygame.Rect(btn_x, 200 + btn_alt + btn_gap, btn_larg, btn_alt)
btn_sair = pygame.Rect(btn_x, 200 + 2 * (btn_alt + btn_gap), btn_larg, btn_alt)

#RECT DOS BOTOES DAS REGRAS
btn_voltar = pygame.Rect(30, ALT - 80, 140, 50)

#REGRAS DO JOGO (parecida com as de Mario ????? sla)
regras_t = ["Regras do Super Sônico:",
            "1. Use as setas do teclado para mover o personagem.",
            "2. Colete itens para ganhar pontos.",
            "3. Evite inimigos para não perder vidas.",
            "4. Se cair no abismo, perderá uma vida.",
            "5. Chegue ao fim do nível para vencer!",
            "Divirta-se jogando!"]

def tela_menu():
    tela.fill((135, 206, 235))  # Fundo cor céu
    desenho_textcent(tela, "Super Sônico", FONT_BIG, PRETO, 100)
    mx, my = pygame.mouse.get_pos()
    #desenhat os botoes com o houver caso o mouse passe por cima
    botao(tela, btn_jogar, "Jogar", FONT_MED, PRETO, VERDE, btn_jogar.collidepoint((mx, my)))
    botao(tela, btn_regras, "Regras", FONT_MED, PRETO, AZUL, btn_regras.collidepoint((mx, my)))
    botao(tela, btn_sair, "Sair", FONT_MED, PRETO, VERMELHO, btn_sair.collidepoint((mx, my)))

def tela_regras():
    tela.fill((240,240,240)) #cinca claro
    desenho_textcent(tela,"Regras", FONT_BIG, PRETO, 60)

    #bloco de texto das regras
    start_y = 140
    for i, linha in enumerate(regras_t):
        surf = FONT_PEQ.render(linha, True, PRETO)
        tela.blit(surf, (60, start_y + i * 30))

    #botão de voltar
    mx, my = pygame.mouse.get_pos()
    botao(tela, btn_voltar, "Voltar", FONT_MED, PRETO, CINZA, btn_voltar.collidepoint((mx, my)))

# inimigos (cada inimigo tem rect, velocidade e limites de patrulha)
# coords iniciais
# inimigos: posições iniciais (pode ajustar)
inimigos = [
    pygame.Rect(600, ALT - 120, 40, 40),
    pygame.Rect(1300, ALT - 120, 40, 40),
    pygame.Rect(2000, ALT - 120, 40, 40),
]

# pequenas variações de posição para evitar fase exatamente igual
for i in range(len(inimigos)):
    inimigos[i].x += random.randint(-6, 6)  # deslocamento inicial aleatório (−6..6 px)

# velocidade inicial aleatória (float) — direções e magnitudes variadas
inimigos_vel = [random.choice([-1, 1]) * random.uniform(0.8, 2.2) for _ in inimigos]

# limites de patrulha diferentes por inimigo (40..120 px de cada lado)
inimigos_lim = [
    (i.x - random.randint(40, 120), i.x + random.randint(40, 120)) for i in inimigos
]

    #AQUI (NO LUGAR DESSA TELA DE JOGO TEMPORÁRIA) VAI ENTRAR PARALLAX, LOGICA DO JOGADOR E AFINS 
def tela_jogo_temporaria():
    global player, player_vel_y, no_chao, vidas, pontos, inimigos_vel, camera_x

    # fundo
    tela.fill((135, 206, 235))  # azul céu

    # centraliza o jogador na tela; limita para não sair dos limites do mapa
    camera_x = player.x - (LARG // 2) + (player.width // 2)
    if camera_x < 0:
        camera_x = 0
    max_camera = max(0, MAP_WIDTH - LARG)
    if camera_x > max_camera:
        camera_x = max_camera

    # MOVIMENTO DO PLAYER
    # -----------------------
    # MOVIMENTO DO PLAYER (resolução por eixo para colisões sólidas)
    # -----------------------
    teclas = pygame.key.get_pressed()

    # velocidade horizontal desejada
    vel_x = 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        vel_x = -velocidade
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        vel_x = velocidade
    if (teclas[pygame.K_UP] or teclas[pygame.K_w] or teclas[pygame.K_SPACE]) and no_chao:
        player_vel_y = -pulo
        no_chao = False
        
    # Aplica movimento horizontal e resolve colisões X
    player.x += vel_x
    for p in plataformas:
        if player.colliderect(p):
            if vel_x > 0:
                # vinha da esquerda -> encostar na lateral esquerda da plataforma
                player.right = p.left
            elif vel_x < 0:
                # vinha da direita -> encostar na lateral direita da plataforma
                player.left = p.right

    # Aplica gravidade (com dt fixo estilo seu código) e movimento vertical
    player_vel_y += gravidade
    player.y += player_vel_y

    # reset do estado de chão
    no_chao = False

    # Resolve colisões verticais
    for p in plataformas:
        if player.colliderect(p):
            if player_vel_y > 0:
                # caindo -> pousou em cima da plataforma
                player.bottom = p.top
                player_vel_y = 0
                no_chao = True
            elif player_vel_y < 0:
                # subindo -> bateu no teto da plataforma
                player.top = p.bottom
                player_vel_y = 0

    # Impede o jogador de sair do mapa (limites X/Y)
    if player.x < 0:
        player.x = 0
    if player.right > MAP_WIDTH:
        player.right = MAP_WIDTH
    if player.bottom > ALT:
        player.bottom = ALT
        player_vel_y = 0
        no_chao = True

    # INIMIGOS (movimento e colisão)
    # cada inimigo usa a mesma inimigos_vel global (você pode trocar depois)
    # INIMIGOS (movimento e colisão) — agora com limites por inimigo
    for idx in range(len(inimigos) - 1, -1, -1):  # iterar de trás pra frente para poder remover
        inimigo = inimigos[idx]
        vel = inimigos_vel[idx]
        left_limit, right_limit = inimigos_lim[idx]

        # move inimigo (x como float precisa ser garantido via atributo .x int; usamos + vel e depois aplicamos int quando desenhar)
        inimigo.x += vel

        # se passou dos limites, coloca no limite e inverte sinal da velocidade
        if inimigo.x < left_limit:
            inimigo.x = left_limit
            inimigos_vel[idx] = -inimigos_vel[idx]
        elif inimigo.x > right_limit:
            inimigo.x = right_limit
            inimigos_vel[idx] = -inimigos_vel[idx]

        # colisão com o jogador
        if player.colliderect(inimigo):
            # stomp (vindo de cima)
            if player_vel_y > 0 and (player.bottom - inimigo.top) < 20:
                inimigos.pop(idx)         # remove inimigo
                inimigos_vel.pop(idx)
                inimigos_lim.pop(idx)
                pontos += 100
                player_vel_y = -pulo * 0.6
                no_chao = False
            else:
                vidas -= 1
                player.x, player.y = 100, ALT - 150
                player_vel_y = 0
                no_chao = False
                if vidas <= 0:
                    pygame.time.delay(800)
                    player.x, player.y = 100, ALT - 150
                    player_vel_y = 0
                    vidas = 3
                    pontos = 0

    # Plataformas
    for p in plataformas:
        draw_rect = (p.x - camera_x, p.y, p.width, p.height)
        pygame.draw.rect(tela, (120, 90, 40), draw_rect)

    # Player (desenha na posição relativa à câmera)
    pygame.draw.rect(tela, (255, 0, 0), (player.x - camera_x, player.y, player.width, player.height))

    # Inimigos
    for inimigo in inimigos:
        pygame.draw.rect(tela, (0, 0, 0), (inimigo.x - camera_x, inimigo.y, inimigo.width, inimigo.height))

    # HUD (vidas e pontos) - permanece fixa na tela (não desloca com a câmera)
    texto = FONT_MED.render(f"Vidas: {vidas}   Pontos: {pontos}", True, PRETO)
    tela.blit(texto, (20, 20))


# VARIÁVEIS DO JOGO (nomes corrigidos e iniciais)
player = pygame.Rect(100, ALT - 150, 40, 60)
player_vel_y = 0
no_chao = False
gravidade = 1.0
velocidade = 5  # velocidade horizontal do jogador
pulo = 18
vidas = 3
pontos = 0

# plataformas (x, y, largura e altura)  — adicione/extrapole sua lista atual
plataformas = [
    pygame.Rect(0, ALT - 80, MAP_WIDTH, 100),  # chão amplo
    pygame.Rect(200, ALT - 200, 200, 20),
    pygame.Rect(500, ALT - 300, 150, 20),
    pygame.Rect(800, ALT - 250, 180, 20),

    # plataformas aéreas (novas)
    pygame.Rect(1100, ALT - 320, 160, 20),
    pygame.Rect(1400, ALT - 380, 120, 20),
    pygame.Rect(1750, ALT - 260, 220, 20),
    pygame.Rect(2100, ALT - 300, 150, 20),
]

def reset_game():
    global player, player_vel_y, no_chao, gravidade, velocidade, pulo, vidas, pontos
    global plataformas, inimigos, inimigos_vel, inimigos_lim

    # jogador
    player.x, player.y = 100, ALT - 150
    player_vel_y = 0
    no_chao = False

    # física / movimento (mantive valores já usados)
    gravidade = 1.0
    velocidade = 5
    pulo = 18

    # HUD
    vidas = 3
    pontos = 0

    # plataformas (se quiser recriar/reinicializar)
    plataformas = [
        pygame.Rect(0, ALT - 80, int(MAP_WIDTH), 80),  # chão
        pygame.Rect(200, ALT - 200, 200, 20),
        pygame.Rect(500, ALT - 300, 150, 20),
        pygame.Rect(800, ALT - 250, 180, 20),
    ]

    # inimigos: recria lista e dados paralelos (velocidades e limites) — agora aleatórios
    inimigos = [
        pygame.Rect(600, ALT - 120, 40, 40),
        pygame.Rect(1300, ALT - 120, 40, 40),
        pygame.Rect(2000, ALT - 120, 40, 40),
    ]
    for i in range(len(inimigos)):
        inimigos[i].x += random.randint(-6, 6)

    inimigos_vel = [random.choice([-1, 1]) * random.uniform(0.8, 2.2) for _ in inimigos]
    inimigos_lim = [(i.x - random.randint(40, 120), i.x + random.randint(40, 120)) for i in inimigos]

#Loop principal do jogo
while True:
    #Trata os eventos do jogo
    for event in pygame.event.get():
    # Verifica consequências do evento
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            # ESC volta ao menu a partir do jogo
            if estado == 'jogando' and event.key == pygame.K_ESCAPE:
                estado = 'menu'
            # Permitir ESC no menu para fechar (opcional)
            elif estado == 'menu' and event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()

        if estado == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_jogar.collidepoint(event.pos):
                    reset_game()
                    estado = 'jogando'
                elif btn_regras.collidepoint(event.pos):
                    estado = 'regras'
                elif btn_sair.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        elif estado == 'regras':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_voltar.collidepoint(event.pos):
                    estado = 'menu'

    #Desenha a tela conforme o estado atual
    if estado == 'menu':
        tela_menu()
    elif estado == 'regras':
        tela_regras()
    elif estado == 'jogando':
        tela_jogo_temporaria()

    pygame.display.flip()
    clock.tick(60)

    #Atualiza estado do jogo
    pygame.display.update()

#Finaliza o pygame
pygame.quit()