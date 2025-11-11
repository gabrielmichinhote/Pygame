import pygame
import sys
import math
from pathlib import Path

pygame.init()

# --------- Configurações ----------
WIDTH, HEIGHT = 900, 600
FPS = 60
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moedinhas - Exemplo")
CLOCK = pygame.time.Clock()

# cores
BG = (120, 180, 255)
PLAYER_COLOR = (200, 30, 30)

# --------- Classe Coin ----------
class Coin:
    """
    Representa uma moeda colecionável.
    - pos: (x, y) posição base da moeda (centro)
    - sprite_path: caminho da imagem (opcional). Se não existir, desenha círculo.
    - size: tamanho em pixels (largura/altura) quando usar sprite ou fallback.
    """
    def __init__(self, pos, sprite_path: str = None, size: int = 40):
        self.x, self.y = float(pos[0]), float(pos[1])
        self.base_y = float(self.y)         # posição base para bobbing
        self.sprite_path = sprite_path
        self.size = size
        self.collected = False
        self._load_sprite()
        # parâmetros de animação bobbing
        self.bob_amplitude = 6.0    # pixels
        self.bob_speed = 3.0        # ciclos por segundo
        self.spawn_time = pygame.time.get_ticks() / 1000.0

    def _load_sprite(self):
        """Tenta carregar a sprite; se falhar, seta sprite = None e usará fallback draw."""
        self.sprite = None
        if not self.sprite_path:
            return
        p = Path(self.sprite_path)
        if p.exists():
            try:
                surf = pygame.image.load(str(p)).convert_alpha()
                # escala para size mantendo proporção
                w, h = surf.get_size()
                scale = self.size / max(w, h)
                new_surf = pygame.transform.smoothscale(surf, (int(w*scale), int(h*scale)))
                self.sprite = new_surf
                # calcular rect para colisão mais tarde
                self.rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
            except Exception as e:
                print(f"Erro ao carregar sprite {self.sprite_path}: {e}")
                self.sprite = None
        else:
            # não existe arquivo
            self.sprite = None

        # se sprite não foi carregada, cria rect de fallback (círculo)
        if self.sprite is None:
            self.rect = pygame.Rect(0, 0, self.size, self.size)
            self.rect.center = (int(self.x), int(self.y))

    def set_sprite(self, new_path: str):
        """Permite trocar a sprite em tempo de execução."""
        self.sprite_path = new_path
        self._load_sprite()

    def update(self, dt):
        """Atualiza a animação (bobbing). dt em segundos."""
        t = pygame.time.get_ticks() / 1000.0 - self.spawn_time
        offset = math.sin(t * self.bob_speed * 2 * math.pi) * self.bob_amplitude
        self.y = self.base_y + offset
        # atualiza rect conforme posição
        self.rect.center = (int(self.x), int(self.y))

    def draw(self, surface):
        if self.collected:
            return
        if self.sprite:
            r = self.sprite.get_rect(center=(int(self.x), int(self.y)))
            surface.blit(self.sprite, r)
        else:
            # fallback: desenha um círculo amarelo com contorno
            pygame.draw.circle(surface, (255, 210, 0), (int(self.x), int(self.y)), self.size // 2)
            pygame.draw.circle(surface, (200,160,0), (int(self.x), int(self.y)), self.size // 2, 3)

    def collide_with_rect(self, other_rect):
        """Verifica colisão simples entre rects (usado para coleta)."""
        if self.collected:
            return False
        return self.rect.colliderect(other_rect)

# --------- Funções utilitárias ----------
def criar_moedas_exemplo():
    """
    Exemplo de criação de várias moedas com e sem sprite.
    - Substitua os caminhos por suas imagens quando quiser.
    """
    coins = []
    # Moedas sem sprite (usar fallback)
    coins.append(Coin((300, 350), sprite_path=None, size=36))
    coins.append(Coin((380, 320), sprite_path=None, size=30))
    # Moedas com sprite (ex: assets/moeda1.png) - troque pelo seu arquivo
    coins.append(Coin((500, 300), sprite_path="assets/moeda1.png", size=48))
    coins.append(Coin((580, 340), sprite_path="assets/moeda2.png", size=42))
    # você pode adicionar quantas quiser e definir um sprite individualmente
    return coins

# --------- Player simples (apenas para testar coleta) ----------
player_w, player_h = 40, 60
player_x, player_y = 100, HEIGHT - 120
player_speed = 260  # px/s
player_rect = pygame.Rect(player_x, player_y, player_w, player_h)

# --------- Inicialização ----------
coins = criar_moedas_exemplo()
score = 0

# dica: caso não tenha imagens, coloque arquivos teste em assets/ ou remova as coins com sprite
print("Iniciando: coloque imagens em assets/moeda1.png etc. se quiser sprites nas moedas.")

# --------- Loop principal ----------
running = True
while running:
    dt_ms = CLOCK.tick(FPS)
    dt = dt_ms / 1000.0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # movimento do jogador (teclas) — movimento suave por dt
    keys = pygame.key.get_pressed()
    vx = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        vx -= player_speed
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        vx += player_speed

    player_rect.x += int(vx * dt)
    # limitar aos limites da tela
    if player_rect.left < 0:
        player_rect.left = 0
    if player_rect.right > WIDTH:
        player_rect.right = WIDTH

    # Atualiza moedas
    for c in coins:
        c.update(dt)

    # Verifica colisões e coleta
    for c in coins:
        if not c.collected and c.collide_with_rect(player_rect):
            c.collected = True
            score += 1
            # aqui você pode tocar som, spawnar partícula etc.
            print(f"Moeda coletada! Score = {score}")

    # Desenho
    SCREEN.fill(BG)

    # desenha moedas (antes do jogador, para ficar embaixo)
    for c in coins:
        c.draw(SCREEN)

    # desenha jogador
    pygame.draw.rect(SCREEN, PLAYER_COLOR, player_rect)

    # HUD simples
    font = pygame.font.Font(None, 36)
    texto = font.render(f"Moedas: {score}", True, (0,0,0))
    SCREEN.blit(texto, (10, 10))

    pygame.display.flip()

pygame.quit()
sys.exit()
