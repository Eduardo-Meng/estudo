
import pygame
from player import Player
from mapa import Mapa
pygame.init()
LARGURA = 800
ALTURA = 600
'''
LARGURA = 1280
ALTURA = 960
'''
screen = pygame.display.set_mode((LARGURA, ALTURA))
clock = pygame.time.Clock()
player = Player(LARGURA, ALTURA)
mapa = Mapa()
rodando = True
while rodando:
    clock.tick(60)
    ataque_pressionado = False
    pulo_precionado = False

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                ataque_pressionado = True
                pulo_precionado = False
            if event.key == pygame.K_UP:
                pulo_precionado = True

    screen.fill((0, 255, 0))
    teclas = pygame.key.get_pressed()
    player.update(teclas, ataque_pressionado, pulo_precionado, mapa.plataformas)
    
    camera_y = 360  # Puxa a visão para o chão!
    mapa.desenhar(screen, camera_y)
    player.desenhar(screen, camera_y)

    pygame.display.update()

pygame.quit()