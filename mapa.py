import pygame
import json

class Mapa:
    def __init__(self):
        self.plataformas = []
        camera_y = 360

        # 1. Carrega a imagem linda e completa que o Tiled já desenhou
        self.imagem_mapa = pygame.image.load('assets/mapa/mapa.png').convert_alpha()
        self.largura_mapa = self.imagem_mapa.get_width()
        self.altura_mapa = self.imagem_mapa.get_height()

        # 2. Carrega as caixas de colisão do JSON
        with open('assets/mapa/mapa.json', 'r', encoding='utf-8') as arquivo:
            dados = json.load(arquivo)

        for camada in dados['layers']:
            if camada['name'] == 'colisao':
                for obj in camada['objects']:
                    retangulo = pygame.Rect(obj['x'], obj['y'], obj['width'], obj['height'])
                    self.plataformas.append(retangulo)

    def desenhar(self, tela, camera_y):
        tela.blit(self.imagem_mapa, (0, -camera_y))