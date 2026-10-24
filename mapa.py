
import pygame
class Mapa:
    def __init__(self):
        self.plataformas = [
            pygame.Rect(0, 580, 800, 10),  #CHAO
            pygame.Rect(100, 550, 150, 30),  #PLATAFORMA INFERIOR
            pygame.Rect(200, 400, 100, 30), # PLATAFORMA DO MEIO
            pygame.Rect(300, 250, 200, 30)  #PLATAFORMA SUPERIOR
        ]

    def desenhar(self, tela):
        for plataforma in self.plataformas:
            if plataforma == self.plataformas[0]:
                pygame.draw.rect(tela, (0, 0, 255), plataforma)
            else:
                pygame.draw.rect(tela, (120, 70, 20), plataforma)       