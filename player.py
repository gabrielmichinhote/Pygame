import pygame
pygame.init()

# Cria a tela
tela = pygame.display.set_mode((800, 600))
clock = pygame.time.Clock()

# --- CLASSE DO SPRITE ---
class Quadrado(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()  # inicializa Sprite
        self.image = pygame.Surface((50, 50))   # cria uma imagem 50x50
        self.image.fill((255, 0, 0))            # pinta de vermelho
        self.rect = self.image.get_rect()       # pega o retângulo da imagem
        self.rect.topleft = (x, y)              # define posição inicial

    def update(self):
        # movimento simples — desce 5 pixels por frame
        self.rect.y += 5
        if self.rect.top > 600:
            self.rect.bottom = 0  # volta pra cima quando sai da tela

# --- CRIAÇÃO DO SPRITE E GRUPO ---
quadrado = Quadrado(100, 100)
todos = pygame.sprite.Group(quadrado)

# --- LOOP PRINCIPAL ---
rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    # atualiza lógica dos sprites
    todos.update()

    # limpa e desenha
    tela.fill((255, 255, 255))
    todos.draw(tela)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
