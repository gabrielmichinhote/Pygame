import pygame
import sys
import player
pygame.init()

class Camera:
    def __init__(self, largura, altura):
        self.largura = largura
        self.altura = altura

        self.cam_x = 0.0
        self.cam_y = 0.0

    def seguir(self, jogador, largura_jog , altura_jog):
        px = getattr(jogador, "x", getattr(jogador, "x_jog", 0.0))
        py = getattr(jogador, "y", getattr(jogador, "y_jog", 0.0))
        pw = getattr(jogador, "largura", getattr(jogador, "largura_jog", getattr(jogador, "largura", 0)))
        ph = getattr(jogador, "altura", getattr(jogador, "altura_jog", getattr(jogador, "altura", 0)))

        self.cam_x = px + pw / 2 - self.screen_width / 2
        self.cam_y = py + ph / 2 - self.screen_height / 2

        # Limita a câmera para não sair dos limites do mundo
        max_x = max(0, largura_jog - self.largura)
        max_y = max(0, altura_jog - self.altura)

        if self.cam_x < 0:
            self.cam_x = 0.0
        elif self.cam_x > max_x:
            self.cam_x = float(max_x)

        if self.cam_y < 0:
            self.cam_y = 0.0
        elif self.cam_y > max_y:
            self.cam_y = float(max_y)

    def get_view(self):
        return int(self.cam_x), (self.cam_y)


