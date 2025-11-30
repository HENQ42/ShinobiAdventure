from pgzero.builtins import images
from pygame import Rect, transform

class SpriteSheet:
    def __init__(self, image_name):
        self.image_name = image_name
        
        # Carrega a superfície original
        # O PgZero carrega imagens como Surfaces do Pygame internamente
        self.surface = images.load(image_name)
        
        # Cria a versão espelhada (flip horizontal=True, vertical=False)
        self.surface_flipped = transform.flip(self.surface, True, False)
        
        self.full_width = self.surface.get_width()
        self.height = self.surface.get_height()
        
        # Assume frames quadrados baseados na altura
        self.frame_width = self.height 
        
        if self.frame_width > 0:
            self.total_frames = self.full_width // self.frame_width
        else:
            self.total_frames = 1
            
        # Cache dos recortes (Rects)
        self.frames_rects = []
        # Para a imagem espelhada, a ordem dos quadros inverte visualmente,
        # mas matematicamente lemos da direita para esquerda ou invertemos a logica.
        # Simplificação: Usamos os mesmos Rects, mas aplicados na surface_flipped.
        for i in range(self.total_frames):
            rect = Rect((i * self.frame_width, 0), (self.frame_width, self.height))
            self.frames_rects.append(rect)

    def get_frame_data(self, frame_index, facing_right=True):
        safe_index = frame_index % self.total_frames
        rect = self.frames_rects[safe_index]
        
        if facing_right:
            return self.surface, rect
        else:
            # Se estiver virado para a esquerda, retornamos a imagem invertida.
            # Nota Matemática: Ao inverter a imagem inteira, o quadro 0 (que era o primeiro da esquerda)
            # vai parar no final da direita. Precisamos ajustar o X do rect.
            # O jeito mais fácil sem matemática complexa é inverter o index
            inv_index = (self.total_frames - 1) - safe_index
            inv_rect = self.frames_rects[inv_index]
            return self.surface_flipped, inv_rect