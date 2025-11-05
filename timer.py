import pygame
tempo_inicial = pygame.time.get_ticks()
tempo_decorrido = pygame.time.get_ticks() - tempo_inicial
segundos = tempo_decorrido // 1000
print(f"Segundos decorridos: {segundos}")