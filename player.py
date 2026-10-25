
import pygame
import math
class Player:
    def __init__(self, largura_tela, altura_tela):
        self.x = 40
        self.y = 390 
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela
        self.tempo_animacao = 0
        self.velocidade_animacao_walk = 0.3
        self.velocidade_animacao_run = 0.8
        self.velocidade_animacao_attack = 0.3
        self.velocidade_animacao_idle = 0.1
        self.velocidade_animacao_jump = 0.3
        self.velocidade = 5
        self.velocidade_walk = 5
        self.velocidade_run = 8
        self.velocidade_y = 0
        self.velocidade_jump = 5
        self.gravidade = 0.8
        self.forca_pulo = -17
        self.esta_no_chao = True
        self.animacao_terminou = False
        self.direcao = 'direita'
        self.estado = 'idle'
        self.estado_anterior = 'idle'

        self.frames_por_estado = {
            'walk': {
                'frames': [],
                'qtd_frames': 10,
                'velocidade': self.velocidade_walk,
                'animacao': self.velocidade_animacao_walk,
                'movimenta': True,
                'repetir': True,
            },

            'run': {
                'frames': [],
                'qtd_frames': 10,
                'velocidade': self.velocidade_run,
                'animacao': self.velocidade_animacao_run,
                'movimenta': True,
                'repetir': True,
            },

            'idle': {
                'frames': [],
                'qtd_frames': 10,
                'animacao': self.velocidade_animacao_idle,
                'movimenta': False,
                'repetir': True,
            },

            'attack': {
                'frames': [],
                'qtd_frames': 10,
                'animacao': self.velocidade_animacao_attack,
                'movimenta': False,
                'repetir': False,
            },

            'jump': {
                'frames': [],
                'qtd_frames': 10,
                'velocidade': self.velocidade_jump,
                'animacao': self.velocidade_animacao_jump,
                'movimenta': True,
                'repetir': False,
            }
        }

        for estado, dados in self.frames_por_estado.items():
            dados['frames'] = self.carregar_imagens(estado, dados['qtd_frames']) 
        self.frame_atual = 0       
        self.imagem = self.frames_por_estado[self.estado]['frames'][self.frame_atual]

        self.largura = self.imagem.get_width()
        self.altura = self.imagem.get_height()

    def carregar_imagens(self, nome_acao, quantidade):
        frames = []
        for i in range(1, quantidade + 1):
            imagem = pygame.image.load(f'assets/{nome_acao}{i}.png').convert_alpha()
            imagem = pygame.transform.scale(imagem,(98, 118))  #(200, 120)    #(48,64))
            frames.append(imagem)
        return frames   
        

        #deixar esta linha nesta posição para calcular a largura e altura da imagem depois 
        # de carregar os frames redimensionados

    

    def definir_estado(self, teclas, ataque_pressionado):

        if self.estado == "attack" and not self.animacao_terminou:
            return

        if ataque_pressionado:
            self.estado = "attack"
        elif not self.esta_no_chao:
            self.estado = "jump"        

        #elif teclas[pygame.K_RIGHT] or teclas[pygame.K_LEFT] or teclas[pygame.K_UP] or teclas[pygame.K_DOWN]:
        # a linha acima foi substituida oela abaixo sem os movimentos cima(UP) e baixo(DOWN) para que o personagem se mova apenas horizontalmente, mas você pode descomentar a linha acima se quiser permitir movimento vertical também.
        elif teclas[pygame.K_RIGHT] or teclas[pygame.K_LEFT]:
            if teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]:
                self.estado = "run"
            else:
                self.estado = "walk"
        else:
            self.estado = "idle"    

    def mover(self, teclas, dados_estado, plataformas):
        movimento_x = 0
        movimento_y = 0

        if teclas[pygame.K_RIGHT]:
            movimento_x = dados_estado['velocidade']
            self.direcao = 'direita'
        elif teclas[pygame.K_LEFT]:
            movimento_x = -dados_estado['velocidade']
            self.direcao = 'esquerda'
        '''
        Retirei o movimento vertical para que o personagem se mova apenas horizontalmente, mas você pode descomentar o código abaixo se quiser permitir movimento vertical também.
        if teclas[pygame.K_UP]:
            movimento_y = -dados_estado['velocidade']
        elif teclas[pygame.K_DOWN]:
            movimento_y = dados_estado['velocidade']
        '''


        if movimento_x != 0 or movimento_y != 0:
            distancia = math.sqrt(movimento_x ** 2 + movimento_y ** 2)
            movimento_x = movimento_x / distancia * dados_estado['velocidade']
            movimento_y = movimento_y / distancia * dados_estado['velocidade']

        novo_x = self.x + movimento_x
        novo_y = self.y + movimento_y

        if 0 <= novo_x <= self.largura_tela - self.largura:
            for plataforma in plataformas:
                sobrepoe_verticalmente = (
                    self.y + self.altura > plataforma.top
                    and self.y < plataforma.bottom
                )

                if sobrepoe_verticalmente:
                    if (
                        movimento_x > 0
                        and self.x + self.largura <= plataforma.left
                        and novo_x + self.largura > plataforma.left
                    ):
                        novo_x = plataforma.left - self.largura

                    elif (
                        movimento_x < 0
                        and self.x >= plataforma.right
                        and novo_x < plataforma.right
                    ):
                        novo_x = plataforma.right    
        
        
        if 0 <= novo_x <= self.largura_tela - self.largura:
            self.x = novo_x

        if 0 <= novo_y <= self.altura_tela - self.altura:
            self.y = novo_y   

    def animar(self, dados_estado):
        
        frames_atuais = dados_estado['frames']
        self.tempo_animacao += dados_estado['animacao']
        self.frame_atual = int(self.tempo_animacao)

        if self.frame_atual >= len(frames_atuais):
            if dados_estado['repetir']:
                self.frame_atual = 0
                self.tempo_animacao = 0
            else:
                self.frame_atual = len(frames_atuais) - 1
                self.animacao_terminou = True

                #self.frame_atual = 0
                #self.tempo_animacao = 0
            
        self.imagem = frames_atuais[self.frame_atual] 

    def pular(self):
        if self.esta_no_chao:
            self.velocidade_y = self.forca_pulo
            self.esta_no_chao = False


    def aplicar_gravidade(self, plataformas):
        self.velocidade_y += self.gravidade
        self.y += self.velocidade_y
        self.esta_no_chao = False

        if self.velocidade_y < 0:
            topo_anterior = self.y - self.velocidade_y

            for plataforma in plataformas:
                sobrepoe_horizontalmente = (
                    self.x + self.largura > plataforma.left
                    and self.x < plataforma.right
                )

                if (
                    sobrepoe_horizontalmente
                    and topo_anterior >= plataforma.bottom
                    and self.y <= plataforma.bottom
                ):
                    self.y = plataforma.bottom
                    self.velocidade_y = 0
                    return

                
        for plataforma in plataformas:
            base_player = self.y + self.altura
            base_anterior = base_player - self.velocidade_y

            if self.velocidade_y > 0:
                if (
                    self.x + self.largura > plataforma.left
                    and self.x < plataforma.right
                    and base_anterior <= plataforma.top
                    and base_player >= plataforma.top
                ):
                    self.y = plataforma.top - self.altura
                    self.velocidade_y = 0
                    self.esta_no_chao = True
                    return


    def update(self, teclas, ataque_pressionado, pulo_precionado, plataformas):        

        self.estado_anterior = self.estado

        if pulo_precionado:
            self.pular()

        self.definir_estado(teclas, ataque_pressionado)

        if self.estado != self.estado_anterior:
            self.animacao_terminou = False
            self.tempo_animacao = 0
            self.frame_atual = 0

        dados_estado = self.frames_por_estado[self.estado]

        if dados_estado['movimenta']:
            self.mover(teclas, dados_estado, plataformas)


        self.aplicar_gravidade(plataformas)

        self.animar(dados_estado)       
        


    def desenhar(self, tela, camera_y):
        # Descontamos a camera do Y para ele subir junto com o mapa!
        posicao_y_na_tela = self.y - camera_y

        if self.direcao == "direita":
            tela.blit(self.imagem, (self.x, posicao_y_na_tela))
        else:
            imagem = pygame.transform.flip(self.imagem, True, False)
            tela.blit(imagem, (self.x, posicao_y_na_tela))