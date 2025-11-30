class Animator:
    def __init__(self, default_state='idle'):
        self.animations = {} 
        self.current_state = default_state
        self.frame_index = 0
        self.timer = 0
        self.facing_right = True # Controle de direção
        
        # Dicionário de velocidades (segundos por frame)
        # Padrão 0.1s (10 FPS), mas Attack pode ser 0.05s
        self.speeds = {} 

    def add_animation(self, state_name, sprite_sheet_obj, speed=0.1):
        self.animations[state_name] = sprite_sheet_obj
        self.speeds[state_name] = speed

    def set_state(self, new_state):
        if self.current_state != new_state:
            # Só troca se a animação existir
            if new_state in self.animations:
                self.current_state = new_state
                self.frame_index = 0
                self.timer = 0

    def update(self, dt):
        # Atualiza o timer baseado no dt (delta time) do jogo
        speed = self.speeds.get(self.current_state, 0.1)
        
        self.timer += dt
        if self.timer >= speed:
            self.timer = 0
            self.frame_index += 1

    def get_render_data(self):
        # Retorna os dados prontos para o draw()
        sheet = self.animations[self.current_state]
        
        # CORREÇÃO: Passamos o self.facing_right para a SpriteSheet saber se inverte ou não
        image_name, rect = sheet.get_frame_data(self.frame_index, self.facing_right)
        
        return image_name, rect