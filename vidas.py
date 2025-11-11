import pygame
import os
import sys


# -------------------- Classe HUD (copiada + simplificada) --------------------
class HUD:
    def __init__(self, total_lives=3, heart_path="HEART.png", heart_size=(30,30),
                 start_pos=(20,20), spacing=40, anim_duration_ms=500, invuln_ms=1000):
        self.total = total_lives
        self.lives = total_lives
        self.heart_size = heart_size
        self.start_x, self.start_y = start_pos
        self.spacing = spacing
        self.anim_duration = anim_duration_ms
        self.invuln_ms = invuln_ms
        self._anim = None
        self._invulnerable_until = 0

        # Carrega imagem com fallback
        if os.path.exists(heart_path):
            try:
                img = pygame.image.load(heart_path).convert_alpha()
                self.heart_img = pygame.transform.smoothscale(img, heart_size)
            except Exception as e:
                print("Erro carregando HEART.png:", e)
                self.heart_img = self._make_fallback()
        else:
            self.heart_img = self._make_fallback()

        self.hearts_pos = [(self.start_x + i * self.spacing, self.start_y) for i in range(self.total)]
        self.font = pygame.font.SysFont(None, 36)

    def _make_fallback(self):
        w, h = self.heart_size
        surf = pygame.Surface((w,h), pygame.SRCALPHA)
        cx, cy = w//2, h//2
        pygame.draw.polygon(surf, (220,20,60), [
            (cx, cy + int(h*0.25)),
            (cx - int(w*0.4), cy - int(h*0.05)),
            (cx - int(w*0.2), cy - int(h*0.4)),
            (cx, cy - int(h*0.2)),
            (cx + int(w*0.2), cy - int(h*0.4)),
            (cx + int(w*0.4), cy - int(h*0.05)),
        ])
        pygame.draw.circle(surf, (220,20,60), (cx - int(w*0.2), cy - int(h*0.2)), int(w*0.2))
        pygame.draw.circle(surf, (220,20,60), (cx + int(w*0.2), cy - int(h*0.2)), int(w*0.2))
        return surf

    def hit(self):
        now = pygame.time.get_ticks()
        if self.lives <= 0 or now < self._invulnerable_until:
            return False
        idx = self.lives - 1
        self._anim = {"index": idx, "start": now}
        self.lives -= 1
        self._invulnerable_until = now + self.invuln_ms
        return True

    def update(self):
        if self._anim is None:
            return
        now = pygame.time.get_ticks()
        if now - self._anim["start"] >= self.anim_duration:
            self._anim = None

    def draw(self, surface):
        now = pygame.time.get_ticks()
        for i in range(self.total):
            x, y = self.hearts_pos[i]
            if i < self.lives:
                surface.blit(self.heart_img, (x, y))
                continue
            if self._anim is not None and i == self._anim["index"]:
                t = now - self._anim["start"]
                progress = min(max(t / self.anim_duration, 0.0), 1.0)
                scale = max(0.01, 1.0 - progress)
                sw = max(1, int(self.heart_size[0] * scale))
                sh = max(1, int(self.heart_size[1] * scale))
                temp = pygame.transform.smoothscale(self.heart_img, (sw, sh))
                alpha = max(0, int(255 * (1.0 - progress)))
                temp.set_alpha(alpha)
                xx = x + (self.heart_size[0] - sw) // 2
                yy = y + (self.heart_size[1] - sh) // 2 - int(20 * progress)
                surface.blit(temp, (xx, yy))

    def reset(self):
        self.lives = self.total
        self._anim = None
        self._invulnerable_until = 0

    def is_game_over(self):
        return self.lives <= 0

# -------------------- Teste mínimo executável --------------------
def main():
    pygame.init()

    # Use janela pequena para testar; troque por FULLSCREEN só depois
    WIDTH, HEIGHT = 800, 560
    tela = pygame.display.set_mode((WIDTH, HEIGHT))  # evite fullscreen até testar
    pygame.display.set_caption("HUD Teste - Pressione H para dano")

    clock = pygame.time.Clock()
    hud = HUD(total_lives=3, heart_path='HEART.png', start_pos=(20,20))

    running = True
    while running:
        dt = clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_h:  # simula dano
                    ok = hud.hit()
                    print("hit() chamado. Decrementou?", ok, "vidas agora:", hud.lives)
                elif event.key == pygame.K_r:  # reinicia vidas
                    hud.reset()
                    print("HUD resetado")

        # Atualiza HUD
        hud.update()

        # Desenha cena simples
        tela.fill((30, 30, 40))
        hud.draw(tela)

        if hud.is_game_over():
            font = pygame.font.SysFont(None, 48)
            txt = font.render("GAME OVER - Pressione R para reiniciar", True, (255, 100, 100))
            tela.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT//2 - txt.get_height()//2))

        pygame.display.flip()

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()

