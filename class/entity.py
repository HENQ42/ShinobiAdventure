from pygame import Rect

class Entity:
    def __init__(self, x, y, width, height):
        # Posição e Física
        self.x = x
        self.y = y
        self.velocity_x = 0
        self.velocity_y = 0
        self.speed = 4
        self.gravity = 0.5
        self.jump_force = -12
        self.on_ground = False
        
        # Hitbox (para colisão)
        # Usamos Rect do Pygame apenas para matematica de colisão
        self.rect = Rect(x, y, width, height)
        
        # Animação (será injetada pelas classes filhas)
        self.animator = None

    def apply_gravity(self):
        self.velocity_y += self.gravity

    def move_and_collide(self, platforms):
        # Movimento X
        self.x += self.velocity_x
        self.rect.x = self.x
        
        # Movimento Y
        self.y += self.velocity_y
        self.rect.y = self.y
        
        # Colisão com Chão (Plataformas)
        self.on_ground = False
        for plat in platforms:
            if self.rect.colliderect(plat):
                # Se estamos caindo e tocamos no chão
                if self.velocity_y > 0: 
                    self.rect.bottom = plat.top
                    self.y = self.rect.y
                    self.velocity_y = 0
                    self.on_ground = True
    def draw(self, screen):
        if self.animator:
            img, area_rect = self.animator.get_render_data()
            
            # --- CORREÇÃO DE ALINHAMENTO ---
            # Pegamos o tamanho real do recorte da imagem (ex: 128x128)
            sprite_w = area_rect.width
            sprite_h = area_rect.height
            
            # Pegamos o tamanho da hitbox (ex: 40x80)
            hitbox_w = self.rect.width
            hitbox_h = self.rect.height
            
            # Calculamos a diferença para centralizar no eixo X
            offset_x = (sprite_w - hitbox_w) / 2
            
            # Calculamos a diferença para alinhar no fundo (Pés no chão) no eixo Y
            # Isso garante que se a imagem for alta, ela cresce para cima
            offset_y = (sprite_h - hitbox_h)
            
            # A posição final do desenho é a posição da hitbox MENOS a sobra
            draw_pos_x = self.x - offset_x
            draw_pos_y = self.y - offset_y
            
            # Desenhamos usando a superfície do Pygame para funcionar o recorte
            screen.surface.blit(img, (draw_pos_x, draw_pos_y), area_rect)
            