
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
#camera_y = 360  # Puxa a visão para o chão!
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
    if player.y > 800:
        player.x = 40
        player.y = 390
        player.velocidade_y = 0
    camera_alvo_x = player.x - (LARGURA // 2)
    camera_alvo_y = player.y - (ALTURA // 2)
    camera_x = max(0, min(mapa.largura_mapa - LARGURA, camera_alvo_x))   
    camera_y = max(0, min(mapa.altura_mapa - ALTURA, camera_alvo_y)) 
    #camera_y = 360  # Continua puxando a visão para o chão por enquanto
    

    
    
    mapa.desenhar(screen, camera_x, camera_y)
    for plat in mapa.plataformas:
        pygame.draw.rect(screen, (255, 0, 0), (plat.x - camera_x, plat.y - camera_y, plat.width, plat.height), 2)
    
    # Desenha a caixa de colisão do guerreiro em VERDE:
    pygame.draw.rect(screen, (0, 255, 0), (player.x - camera_x, player.y - camera_y, player.largura, player.altura), 2)
    player.desenhar(screen, camera_x, camera_y)

    pygame.display.update()

pygame.quit()