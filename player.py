import pygame
import sys
import timer
pygame.init()

altura = 800
largura = 800
altura_jog = 60
largura_jog = 40
cor_jog = (200, 30, 30)

x_jog = 200
base_chao = 170
altura_chao = altura - base_chao - altura_jog  # posição y do topo do jogador quando estiver no chão
chao = altura_chao                                # chao agora é numérico (y do chão)
y_jog = chao                                      # começar no chão

velocidade_jog = 4
velocidade_y_jog = 0

gravidade = 1
pulo_jog = 18
terminal_vel = 25
no_chao = True

tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
jogador_surf = pygame.Surface((largura_jog, altura_jog))
jogador_surf.fill(cor_jog)

clock = pygame.time.Clock()
while True:
    dt = clock.tick(60)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.quit()
                sys.exit()
            if event.key == pygame.K_UP and no_chao:
                velocidade_y_jog = -pulo_jog
                no_chao = False
            if event.key == pygame.K_c:   # teleporte para o chão
                y_jog = chao
                velocidade_y_jog = 0
                no_chao = True

    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        x_jog -= velocidade_jog
    if teclas[pygame.K_RIGHT]:
        x_jog += velocidade_jog

    velocidade_y_jog += gravidade
    y_jog += velocidade_y_jog

    if y_jog >= chao:
        y_jog = chao
        velocidade_y_jog = 0
        no_chao = True

    # impedir sair da tela horizontal
    if x_jog < 0:
        x_jog = 0
    if x_jog + largura_jog > largura:
        x_jog = largura - largura_jog

    tela.fill((135, 206, 235))  # fundo céu
    tela.blit(jogador_surf, (int(x_jog), int(y_jog)))
    pygame.display.flip()