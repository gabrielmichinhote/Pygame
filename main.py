import pygame
import sys
import random
import math
import json
from pathlib import Path
import map as map_data


#inicializacao do jogo
pygame.init()
pygame.mixer.init() 
LARG, ALT = 800, 600
clock = pygame.time.Clock()
FONT_BIG = pygame.font.SysFont("arial", 64)
FONT_MED = pygame.font.SysFont("arial", 36)
FONT_PEQ = pygame.font.SysFont("arial", 24)
MAP_WIDTH = map_data.COLS * map_data.TILE
FONT_GO = pygame.font.Font('NiseJSRF.ttf',96)
FONT_GO_MENOR = pygame.font.Font('BloomsFree.ttf', 48)
FONT_TITULO = pygame.font.Font('Westland.ttf', 125)

#cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (128, 128, 128)

camera_x = 0

tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
pygame.display.set_caption("Super Sônico")
map_data.load_tiles()
LARG, ALT = tela.get_size()  #ajusta o tamanho de acordo c o monitor
BG_MENU_PATH = "sonic_fundo.png"

try:
    bg_img = pygame.image.load(BG_MENU_PATH).convert()
    bg_img = pygame.transform.smoothscale(bg_img, (LARG, ALT))
except Exception as e:
    bg_img = None

PLAYER_PAD = "sonic_parado_d.png"
PLAYER_PAE = "sonic_parado_e.png"
PLAYER_COD  = "sonic_correndo_d.png"
PLAYER_COE  = "sonic_correndo_e.png"

def load_player_sprites(target_width=None, target_height=None):
    def _safe_load(path):
        try:
            surf = pygame.image.load(path).convert_alpha()
            return surf
        except Exception as e:
            return None

    s_pad = _safe_load(PLAYER_PAD)
    s_pae = _safe_load(PLAYER_PAE)
    s_cod  = _safe_load(PLAYER_COD)
    s_coe  = _safe_load(PLAYER_COE)

    if target_width and target_height:
        def _scale(s):
            return None if s is None else pygame.transform.smoothscale(s, (target_width, target_height))
        return (_scale(s_pad), _scale(s_pae), _scale(s_cod), _scale(s_coe))
    else:
        return (s_pad, s_pae, s_cod, s_coe)

player_sprites = (None, None, None, None)

#estado do jogo
estado = 'menu'  #'menu','regras','jogando','nome','ranking'
game_finished = False
game_start_time = None
victory_time = None

RANKING_FILE = Path("ranking.json")
MAX_RANK = 10

#sons e musica
som_pulo = pygame.mixer.Sound("jump.wav")
som_moeda = pygame.mixer.Sound("coin.wav")
pygame.mixer.music.load("Musicatema.wav")
pygame.mixer.music.set_volume(0.5)  
pygame.mixer.music.play(-1)
som_go = pygame.mixer.Sound("gameover.wav")
som_go.set_volume(0.7)
som_inimigo_morrendo = pygame.mixer.Sound("morteinimigo.wav")
som_inimigo_morrendo.set_volume(0.7)
som_player_morrendo = pygame.mixer.Sound("mortejogador.wav")
som_player_morrendo.set_volume(0.7)
som_gp = 'mario.wav'

#utilitarios
def desenho_textcent(tela, texto, fonte, cor, y):
    surf = fonte.render(texto, True, cor)
    rect = surf.get_rect(center=(LARG // 2, y))
    tela.blit(surf, rect)
    return rect

def botao(tela, rect, texto, fonte, cor_t, cor_f, houver=False):
    nova_cor = []
    for c in cor_f:
        if houver:
            valor = c * 1.5
        else:
            valor = c * 1.0
        valor = int(valor)
        if valor > 225:
            valor = 225
        nova_cor.append(valor)
    cor_display = tuple(nova_cor)
    pygame.draw.rect(tela, cor_display, rect, border_radius=8)
    pygame.draw.rect(tela, PRETO, rect, 3, border_radius=8)
    surf = fonte.render(texto, True, cor_t)
    r = surf.get_rect(center=rect.center)
    tela.blit(surf, r)

#botoes do menu
btn_larg, btn_alt = 300, 65
btn_x = (LARG - btn_larg) // 2
btn_gap = 20
btn_jogar = pygame.Rect(btn_x, 200, btn_larg, btn_alt)
btn_regras = pygame.Rect(btn_x, 200 + btn_alt + btn_gap, btn_larg, btn_alt)
btn_sair = pygame.Rect(btn_x, 200 + 2 * (btn_alt + btn_gap), btn_larg, btn_alt)
btn_voltar = pygame.Rect(30, ALT - 80, 140, 50)
btn_restart = pygame.Rect(btn_x, 500, btn_larg, btn_alt)
btn_to_menu = pygame.Rect(btn_x, 600, btn_larg, btn_alt)

#menu e regrinhas 
regras_t = ["Regras do Super Sônico:",
            "1. Use as setas do teclado para mover o personagem.",
            "2. Colete itens para ganhar pontos.",
            "3. Evite inimigos para não perder vidas.",
            "4. Se cair no abismo, perderá uma vida.",
            "5. Chegue ao fim do nível para vencer!",
            "Divirta-se jogando!"]

def tela_menu():
    if bg_img:
        tela.blit(bg_img, (0, 0))
    else:
        tela.fill((135, 206, 235))
    desenho_textcent(tela, "SUPER SONICO", FONT_TITULO, PRETO, 130)
    mx, my = pygame.mouse.get_pos()
    botao(tela, btn_jogar, "Jogar", FONT_GO_MENOR, PRETO, VERDE, btn_jogar.collidepoint((mx, my)))
    botao(tela, btn_regras, "Regras", FONT_GO_MENOR, PRETO, AZUL, btn_regras.collidepoint((mx, my)))
    botao(tela, btn_sair, "Sair", FONT_GO_MENOR, PRETO, VERMELHO, btn_sair.collidepoint((mx, my)))

def tela_regras():
    tela.fill((240,240,240))
    desenho_textcent(tela,"Regras", FONT_GO_MENOR, PRETO, 80)
    start_y = 140
    for i, linha in enumerate(regras_t):
        surf = FONT_PEQ.render(linha, True, PRETO)
        tela.blit(surf, (60, start_y + i * 30))
    mx, my = pygame.mouse.get_pos()
    botao(tela, btn_voltar, "Voltar", FONT_GO_MENOR, PRETO, CINZA, btn_voltar.collidepoint((mx, my)))

#inimigos iniciais 

inimigos = [
    pygame.Rect(600, ALT - 332, 40, 40),
    pygame.Rect(600, ALT - 170, 40, 40),
    pygame.Rect(2100, ALT - 330, 40, 40),
    pygame.Rect(2500, ALT - 300, 40, 40),
    pygame.Rect(2800, ALT - 300, 40, 40),
    pygame.Rect(3500, ALT - 170, 40, 40),
    pygame.Rect(3900, ALT - 300, 40, 40),
    pygame.Rect(4500, ALT - 400, 40, 40),
    pygame.Rect(5000, ALT - 300, 40, 40),
    pygame.Rect(5500, ALT - 170, 40, 40), 
]
for i in range(len(inimigos)):
    inimigos[i].x += random.randint(-6, 6)
inimigos_vel = [random.choice([-1, 1]) * random.uniform(0.8, 2.2) for _ in inimigos]
inimigos_lim = [(i.x - random.randint(40, 120), i.x + random.randint(40, 120)) for i in inimigos]

#coin class (ref de vídeo do YouTube)
class Coin:
    def __init__(self, x, y, sprite_path=None, size=36):
        self.x = float(x); self.y = float(y); self.base_y = float(y)
        self.sprite_path = sprite_path; self.size = int(size); self.collected = False
        self.spawn_time = pygame.time.get_ticks() / 1000.0
        self.bob_amplitude = 6.0; self.bob_speed = 2.5; self.sprite = None
        self.rect = pygame.Rect(0, 0, self.size, self.size)
        self._load_sprite()
    def _load_sprite(self):
        self.sprite = None
        if not self.sprite_path:
            self.rect = pygame.Rect(0, 0, self.size, self.size)
            self.rect.center = (int(self.x), int(self.y)); return
        p = Path(self.sprite_path)
        if p.exists():
            try:
                surf = pygame.image.load(str(p)).convert_alpha()
                w, h = surf.get_size(); scale = self.size / max(w, h)
                self.sprite = pygame.transform.smoothscale(surf, (int(w*scale), int(h*scale)))
                self.rect = self.sprite.get_rect(center=(int(self.x), int(self.y)))
            except Exception as e:
                print("Erro ao carregar sprite da moeda:", e)
                self.sprite = None
                self.rect = pygame.Rect(0, 0, self.size, self.size); self.rect.center = (int(self.x), int(self.y))
        else:
            self.sprite = None; self.rect = pygame.Rect(0, 0, self.size, self.size); self.rect.center = (int(self.x), int(self.y))
    def set_sprite(self, path):
        self.sprite_path = path; self._load_sprite()
    def update(self):
        t = pygame.time.get_ticks() / 1000.0 - self.spawn_time
        offset = math.sin(t * self.bob_speed * 2 * math.pi) * self.bob_amplitude
        self.y = self.base_y + offset; self.rect.center = (int(self.x), int(self.y))
    def draw(self, surface, camera_x):
        if self.collected: return
        screen_x = int(self.x - camera_x); screen_y = int(self.y)
        if self.sprite:
            r = self.sprite.get_rect(center=(screen_x, screen_y)); surface.blit(self.sprite, r)
        else:
            pygame.draw.circle(surface, (255,210,0), (screen_x, screen_y), self.size // 2)
            pygame.draw.circle(surface, (200,160,0), (screen_x, screen_y), self.size // 2, 3)
    def try_collect(self, player_rect):
        if self.collected: return False
        if self.rect.colliderect(player_rect):
            self.collected = True; return True
        return False

#logica princpal do jogo (já nao é mais a temporária, apesar do nome)
def tela_jogo_temporaria():
    global player, player_vel_y, no_chao, vidas, pontos
    global inimigos, inimigos_vel, inimigos_lim, plataformas, coins, camera_x
    global estado, game_finished, game_start_time, victory_time, coins, inimigo, inimigos_lim, inimigos_vel
    global player_facing, player_moving
    # desenha mapa
    map_data.draw_level(tela, map_data.LEVEL, (camera_x, 0))

    #centralizacao da cam no player
    camera_x = player.x - (LARG // 2) + (player.width // 2)
    if camera_x < 0: camera_x = 0
    max_camera = max(0, MAP_WIDTH - LARG)
    if camera_x > max_camera: camera_x = max_camera

    #movimentaçao
    teclas = pygame.key.get_pressed()
    vel_x = 0
    if teclas[pygame.K_LEFT] or teclas[pygame.K_a]:
        vel_x = -velocidade
    if teclas[pygame.K_RIGHT] or teclas[pygame.K_d]:
        vel_x = velocidade
    if (teclas[pygame.K_UP] or teclas[pygame.K_w] or teclas[pygame.K_SPACE]) and no_chao:
        som_pulo.play()
        player_vel_y = -pulo; no_chao = False

    player_moving = (vel_x != 0)
    if vel_x > 0:
        player_facing = "right"
    elif vel_x < 0:
        player_facing = "left"

    #mov horizontal e colisões X
    player.x += vel_x
    for p in plataformas:
        if player.colliderect(p):
            if vel_x > 0: player.right = p.left
            elif vel_x < 0: player.left = p.right

    #fis do mov vertical e colisoes Y
    player_vel_y += gravidade
    player.y += player_vel_y
    no_chao = False
    for p in plataformas:
        if player.colliderect(p):
            if player_vel_y > 0:
                player.bottom = p.top; player_vel_y = 0; no_chao = True
            elif player_vel_y < 0:
                player.top = p.bottom; player_vel_y = 0

    # limites horizontais
    if player.x < 0:
        player.x = 0
    if player.right > MAP_WIDTH:
        player.right = MAP_WIDTH

    if player.top > ALT:
        game_finished = True
        estado = 'game_over'
        pygame.mixer.music.stop()
        som_go.play()

    #mov dos inimigos e colisoes
    for idx in range(len(inimigos) - 1, -1, -1):
        inimigo = inimigos[idx]; vel = inimigos_vel[idx]; left_limit, right_limit = inimigos_lim[idx]
        inimigo.x += vel
        if inimigo.x < left_limit:
            inimigo.x = left_limit; inimigos_vel[idx] = -inimigos_vel[idx]
        elif inimigo.x > right_limit:
            inimigo.x = right_limit; inimigos_vel[idx] = -inimigos_vel[idx]

        if player.colliderect(inimigo):
            if player_vel_y > 0 and (player.bottom - inimigo.top) < 20:
                inimigos.pop(idx); inimigos_vel.pop(idx); inimigos_lim.pop(idx)
                som_inimigo_morrendo.play()
                pontos += 100; player_vel_y = -pulo * 0.6; no_chao = False
            else:
                som_player_morrendo.play()
                vidas -= 1
                player.x, player.y = 100, ALT - 200
                player_vel_y = 0
                no_chao = False
                if vidas <= 0:
                    pygame.time.delay(500)
                    game_finished = True
                    estado = 'game_over'
                    pygame.mixer.music.stop()
                    som_go.play()

    #att moedinhas coletadas 
    for c in coins: c.update()
    for c in coins:
        if not c.collected and c.try_collect(player):
            som_moeda.play()
            pontos += 50

    #desenha moedinhas
    for c in coins: c.draw(tela, camera_x)

    pad, pae, cod, coe = player_sprites

    sprite = None
    if player_moving:
        if player_facing == "right":
            sprite = cod or pad
        else:
            sprite = coe or pae
    else:
        sprite = pad if player_facing == "right" else pae

    screen_x = int(player.x - camera_x)
    screen_y = int(player.y)

    if sprite:
        rect_sprite = sprite.get_rect(topleft=(screen_x, screen_y))
        tela.blit(sprite, rect_sprite)
    else:
        pygame.draw.rect(tela, (255, 0, 0), (screen_x, player.y, player.width, player.height))

    for inimigo in inimigos:
        pygame.draw.rect(tela, (0, 0, 0), (inimigo.x - camera_x, inimigo.y, inimigo.width, inimigo.height))


    #HUD com vidas e pontos
    texto = FONT_MED.render(f"Vidas: {vidas}   Pontos: {pontos}", True, PRETO)
    tela.blit(texto, (20, 20))

    #CHECAGEM DE VITORIA
    if not game_finished and player.right >= MAP_WIDTH - 5:
        #grava a vitoria
        game_finished = True
        now = pygame.time.get_ticks()
        if game_start_time is None:
            elapsed_ms = 0
        else:
            elapsed_ms = now - game_start_time
        victory_time = round(elapsed_ms / 1000.0, 3)  #segundos com 3 casas
        #passa a estado de input de nome
        estado = 'nome'

#VARIAVEIS DO JOGO
player = pygame.Rect(100, ALT - 150, 30, 45)
player_sprites = load_player_sprites(player.width, player.height)
pad, pae, cod, coe = player_sprites
if pad and pae is None:
    pae = pygame.transform.flip(pad, True, False)
if cod and coe is None:
    coe = pygame.transform.flip(cod, True, False)
player_sprites = (pad, pae, cod, coe)
player_vel_y = 0
no_chao = False
gravidade = 1.0
velocidade = 5
pulo = 18
vidas = 3
pontos = 0

plataformas = map_data.get_merged_collision_rects(map_data.TILE, collide_tiles=(1,2))

coins = [
    Coin(310, ALT - 190, sprite_path=None, size=36),
    Coin(500, ALT - 170, sprite_path=None, size=30),
    Coin(620, ALT - 320, sprite_path=None, size=36),
    Coin(870, ALT - 170, sprite_path="assets/coin1.png", size=42),  
    Coin(1200, ALT - 250, sprite_path="assets/coin1.png", size=40),
    Coin(1480, ALT - 320, sprite_path="assets/coin1.png", size=42),  
    Coin(1740, ALT - 230, sprite_path="assets/coin1.png", size=40),
    Coin(2100, ALT - 320, sprite_path="assets/coin1.png", size=42),  
    Coin(2500, ALT - 170, sprite_path="assets/coin1.png", size=40),
    Coin(2700, ALT - 320, sprite_path="assets/coin1.png", size=42),  
    Coin(3000, ALT - 240, sprite_path="assets/coin1.png", size=40),
    Coin(3500, ALT - 170, sprite_path="assets/coin1.png", size=42),  
    Coin(3800, ALT - 300, sprite_path="assets/coin1.png", size=40),
    Coin(4500, ALT - 400, sprite_path="assets/coin1.png", size=42),
    Coin(5000, ALT - 300, sprite_path="assets/coin1.png", size=40),
    Coin(5500, ALT - 170, sprite_path="assets/coin1.png", size=42),
]

def reset_game():
    global player, player_vel_y, no_chao, gravidade, velocidade, pulo, vidas, pontos
    global plataformas, game_finished, game_start_time, victory_time, coins, inimigos, inimigos_vel, inimigos_lim

    player.x, player.y = 100, ALT - 150
    player_vel_y = 0
    no_chao = False
    gravidade = 1.0
    velocidade = 5
    pulo = 18
    vidas = 3
    pontos = 0
    plataformas = map_data.get_merged_collision_rects(map_data.TILE, collide_tiles=(1,2))

    inimigos[:] = [
        pygame.Rect(600, ALT - 332, 40, 40),
        pygame.Rect(600, ALT - 170, 40, 40),
        pygame.Rect(2100, ALT - 330, 40, 40),
        pygame.Rect(2500, ALT - 300, 40, 40),
        pygame.Rect(2800, ALT - 300, 40, 40),
        pygame.Rect(3500, ALT - 170, 40, 40),
        pygame.Rect(3900, ALT - 300, 40, 40),
        pygame.Rect(4500, ALT - 400, 40, 40),
        pygame.Rect(5000, ALT - 300, 40, 40),
        pygame.Rect(5500, ALT - 170, 40, 40),
    ]

    coins[:] = [
        Coin(310, ALT - 190, sprite_path=None, size=36),            
        Coin(500, ALT - 170, sprite_path=None, size=30),
        Coin(620, ALT - 320, sprite_path=None, size=36),
        Coin(870, ALT - 170, sprite_path="assets/coin1.png", size=42),
        Coin(1200, ALT - 250, sprite_path="assets/coin1.png", size=40),
        Coin(1480, ALT - 320, sprite_path="assets/coin1.png", size=42),
        Coin(1740, ALT - 230, sprite_path="assets/coin1.png", size=40),
        Coin(2100, ALT - 320, sprite_path="assets/coin1.png", size=42),
        Coin(2500, ALT - 170, sprite_path="assets/coin1.png", size=40),
        Coin(2700, ALT - 320, sprite_path="assets/coin1.png", size=42),
        Coin(3000, ALT - 240, sprite_path="assets/coin1.png", size=40),
        Coin(3500, ALT - 170, sprite_path="assets/coin1.png", size=42),
        Coin(3800, ALT - 300, sprite_path="assets/coin1.png", size=40),
        Coin(4500, ALT - 400, sprite_path="assets/coin1.png", size=42),
        Coin(5000, ALT - 300, sprite_path="assets/coin1.png", size=40),
        Coin(5500, ALT - 170, sprite_path="assets/coin1.png", size=42),
    ]
    for i in range(len(inimigos)):
        inimigos[i].x += random.randint(-6, 6)
    inimigos_vel[:] = [random.choice([-1, 1]) * random.uniform(0.8, 2.2) for _ in inimigos]
    inimigos_lim[:] = [(i.x - random.randint(40, 120), i.x + random.randint(40, 120)) for i in inimigos]
    #marca o início do tempo do nível
    game_finished = False
    victory_time = None
    game_start_time = pygame.time.get_ticks()

#ranking 
def load_ranking():
    if not RANKING_FILE.exists():
        return []
    try:
        with open(RANKING_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            #garantir formato pesquisado: lista de {"name":str,"time":float}
            return [d for d in data if "name" in d and "time" in d]
    except Exception as e:
        print("Erro ao ler ranking:", e)
        return []

def save_ranking(ranking):
    try:
        with open(RANKING_FILE, "w", encoding="utf-8") as f:
            json.dump(ranking, f, ensure_ascii=False, indent=2)
    except Exception as e:
        print("Erro ao salvar ranking:", e)

def add_ranking_entry(name, time_seconds):
    ranking = load_ranking()
    ranking.append({"name": name, "time": float(time_seconds)})
    #ordem por tempo ascendente
    ranking.sort(key=lambda x: x["time"])
    #manter top N
    ranking = ranking[:MAX_RANK]
    save_ranking(ranking)
    return ranking

#estado de input do nome
input_name = ""
name_active = False

player_facing = "right"
player_moving = False

#LOOP PRINCIPAL
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit(); sys.exit()

        #teclas globais
        if event.type == pygame.KEYDOWN:
            if estado == 'jogando' and event.key == pygame.K_ESCAPE:
                estado = 'menu'
            elif estado == 'menu' and event.key == pygame.K_ESCAPE:
                pygame.quit(); sys.exit()
            #quando estiver na tela para digitar o nome, processamos entrada de texto
            if estado == 'nome':
                if event.key == pygame.K_RETURN:
                    #se não tiver digitado nada, atribui "Jogador"
                    if input_name.strip() == "":
                        input_name = "Jogador"
                    #salva entrada e mostra ranking
                    ranking = add_ranking_entry(input_name.strip(), victory_time if victory_time is not None else 0.0)
                    estado = 'ranking'
                    input_name = ""
                elif event.key == pygame.K_BACKSPACE:
                    input_name = input_name[:-1]
                else:
                    #limita tamanho do nome
                    if len(input_name) < 20 and event.unicode.isprintable():
                        input_name += event.unicode

            #atalho na tela de ranking: R para resetar e voltar ao menu
            if estado == 'ranking' and event.key == pygame.K_r:
                estado = 'menu'

            if estado == 'game_over':
                if event.key == pygame.K_r:
                    reset_game()
                    estado = 'jogando'
                elif event.key == pygame.K_ESCAPE:
                    estado = 'menu'

        #mouse em menu/regras
        if estado == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_jogar.collidepoint(event.pos):
                    pygame.mixer.music.stop()
                    reset_game()
                    estado = 'jogando'
                    pygame.mixer.music.load(som_gp)
                    pygame.mixer.music.play(-1)
                elif btn_regras.collidepoint(event.pos):
                    estado = 'regras'
                elif btn_sair.collidepoint(event.pos):
                    pygame.quit(); sys.exit()
        elif estado == 'regras':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_voltar.collidepoint(event.pos):
                    estado = 'menu'
        if estado == 'game_over' and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if btn_restart.collidepoint(event.pos):
                reset_game()
                estado = 'jogando'
                pygame.mixer.music.load(som_gp)
                pygame.mixer.music.set_volume(0.3)
                pygame.mixer.music.play(-1)
            elif btn_to_menu.collidepoint(event.pos):
                estado = 'menu'
        

    #desenha conforme estado
    if estado == 'menu':
        if not pygame.mixer.music.get_busy():
            pygame.mixer.music.load("Musicatema.wav")
            pygame.mixer.music.play(-1)
        tela_menu()
    elif estado == 'regras':
        tela_regras()
    elif estado == 'jogando':
        tela_jogo_temporaria()
    elif estado == 'nome':
        #tela de vitória e instrução para digitar o nome
        tela.fill((20, 40, 60))
        desenho_textcent(tela, "Você venceu!!", FONT_BIG, (255, 220, 100), ALT // 2 - 80)
        if victory_time is not None:
            ttxt = f"Tempo: {victory_time:.3f} s"
            desenho_textcent(tela, ttxt, FONT_MED, BRANCO, ALT // 2 - 10)
        desenho_textcent(tela, "Pressione ENTER para confirmar e digitar seu nome", FONT_PEQ, (200,200,200), ALT // 2 + 40)
        box_w = 500; box_h = 48
        box_x = (LARG - box_w) // 2; box_y = ALT // 2 + 100
        pygame.draw.rect(tela, (255,255,255), (box_x, box_y, box_w, box_h), border_radius=8)
        txtsurf = FONT_MED.render(input_name or "Digite seu nome...", True, (0,0,0))
        tela.blit(txtsurf, (box_x + 10, box_y + (box_h - txtsurf.get_height())//2))
    elif estado == 'ranking':
        tela.fill((10, 10, 30))
        desenho_textcent(tela, "Ranking - Melhores Tempos", FONT_BIG, (255, 220, 180), 80)
        ranking = load_ranking()
        start_y = 150
        for i, entry in enumerate(ranking):
            name = entry.get("name", "Jogador")
            time_s = float(entry.get("time", 0.0))
            txt = f"{i+1:2d}. {name:20s} - {time_s:.3f} s"
            surf = FONT_PEQ.render(txt, True, (220,220,220))
            tela.blit(surf, (LARG//2 - 220, start_y + i * 32))
        #instruções
        desenho_textcent(tela, "Pressione R para voltar ao menu", FONT_PEQ, (180,180,180), ALT - 60)
    #tela de game over
    elif estado == 'game_over':
        tela.fill((20, 20, 30))
        desenho_textcent(tela, "GAME OVER", FONT_GO, (255, 60, 60), ALT // 2 - 80)
        desenho_textcent(tela, "Você morreu!", FONT_GO_MENOR, (200,200,200), 450)

        # desenha os botões
        mx, my = pygame.mouse.get_pos()
        botao(tela, btn_restart, "Recomeçar", FONT_MED, PRETO, VERDE, btn_restart.collidepoint((mx, my)))
        botao(tela, btn_to_menu, "Voltar ao menu", FONT_MED, PRETO, CINZA, btn_to_menu.collidepoint((mx, my)))

        # dica de teclado
        desenho_textcent(tela, "Pressione R para recomeçar ou ESC para voltar ao menu", FONT_PEQ, (180,180,180), ALT - 60)

    pygame.display.flip()
    clock.tick(60)

    #atualiza display
    pygame.display.update()
