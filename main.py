import pygame
import sys

# TELA COM COMEÇAR, SAIR, REGRAS, ETC.

#Inicializa o pygame
pygame.init()
LARG, ALT = 800, 600

clock = pygame.time.Clock()
FONT_BIG = pygame.font.SysFont("arial", 64)
FONT_MED = pygame.font.SysFont("arial", 36)
FONT_PEQ = pygame.font.SysFont("arial", 24)

#CORES USADAS 
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)   
VERDE = (0, 255, 0)
VERMELHO = (255, 0, 0)
AZUL = (0, 0, 255)
CINZA = (128, 128, 128)


#Gera a tela principal do jogo
tela = pygame.display.set_mode((0, 0), pygame.FULLSCREEN) #p abrir em tela cheia de acordo c o monitor
pygame.display.set_caption("Super Sônico")

LARG, ALT = tela.get_size()  #atualiza LARG e ALT p o tamanho real da tela

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
    
    #AQUI (NO LUGAR DESSA TELA DE JOGO TEMPORÁRIA) VAI ENTRAR PARALLAX, LOGICA DO JOGADOR E AFINS 
def tela_jogo_temporaria():
    tela.fill((90, 100, 90)) #verde grama
    desenho_textcent(tela, "Jogo sendo executado...", FONT_BIG, PRETO, 250)
    info = FONT_MED.render("Pressione Esc para voltar ao menu", True, PRETO)
    tela.blit(info, info.get_rect(center=(LARG // 2, 100)))

    #representaçao do jogador
    pygame.draw.rect(tela, (200, 30,30), (LARG // 2 - 20, ALT - 140, 40, 60))
    #ex de plataforma
    pygame.draw.rect(tela, (120,90,40), (0, ALT - 80, LARG, 80))

#VARIAVEIS DO JOGO
player = pygame.Rect(100, ALT - 150, 40, 60) 
velopy = 0
nochao = False
gravidade = 1
valocidade = 5
pulo = 18
vidas = 3 
pontos = 0

#plataformas (x, y, largura e altura)
plataformas = [
    pygame.Rect(0, ALT - 80, LARG, 80),  #chão
    pygame.Rect(200, ALT - 200, 200, 20),
    pygame.Rect(500, ALT - 300, 150, 20),
    pygame.Rect(800, ALT - 250, 180, 20),
]

#inimigos
inimigos = [pygame.Rect(600, ALT - 120, 40, 40)]
veloinimigo = 2

#Loop principal do jogo
while True:
    #Trata os eventos do jogo
    for event in pygame.event.get():
        #Verifica consequências do evento 
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if estado == 'menu':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_jogar.collidepoint(event.pos):
                    estado = 'jogando'
                elif btn_regras.collidepoint(event.pos):  #esse event guarda a posição X e Y do mouse
                    estado = 'regras'
                elif btn_sair.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        elif estado == 'regras':
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_voltar.collidepoint(event.pos):
                    estado = 'menu'

        elif estado == 'jogando':
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
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
