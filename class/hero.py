from entity import Entity
from animator import Animator

class Hero(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, 40, 80)
        
        self.animator = Animator('idle')
        self.is_attacking = False
        self.hp = 100
        # Novo cronômetro específico para duração do ataque
        self.attack_duration_timer = 0 
        
    def setup_animations(self):
        from spritesheet import SpriteSheet
        
        # Velocidades
        self.animator.add_animation('idle', SpriteSheet('shinobi_idle'), 0.15)
        self.animator.add_animation('run', SpriteSheet('shinobi_run'), 0.1)
        self.animator.add_animation('jump', SpriteSheet('shinobi_jump'), 0.1)
        self.animator.add_animation('attack', SpriteSheet('shinobi_attack'), 0.08)

    def input(self, keyboard):
        # Se estiver atacando, ignoramos inputs de movimento
        if self.is_attacking:
            return

        moved = False
        if keyboard.left:
            self.velocity_x = -self.speed
            self.animator.facing_right = False
            moved = True
        elif keyboard.right:
            self.velocity_x = self.speed
            self.animator.facing_right = True
            moved = True
        else:
            self.velocity_x = 0
            
        if keyboard.up and self.on_ground:
            self.velocity_y = self.jump_force
            self.on_ground = False
            
        # Atacar
        if keyboard.space:
            self.attack()
            return 
            
        # Estados
        if not self.is_attacking:
            if not self.on_ground:
                self.animator.set_state('jump')
            elif moved:
                self.animator.set_state('run')
            else:
                self.animator.set_state('idle')

    def attack(self):
        if not self.is_attacking:
            self.is_attacking = True
            self.animator.set_state('attack')
            
            # Reinicia o cronômetro do Herói (não do Animator)
            self.attack_duration_timer = 0 
            
            # Reseta a animação visual para começar do quadro 0
            self.animator.frame_index = 0
            self.animator.timer = 0

    def update(self, dt):
        super().apply_gravity()
        
        # CORREÇÃO DO TRAVAMENTO:
        if self.is_attacking:
            # Somamos o tempo que passou no nosso cronômetro independente
            self.attack_duration_timer += dt
            
            # Se a animação tem 4 frames de 0.08s = 0.32s total.
            # Colocamos 0.35s para garantir que termine.
            if self.attack_duration_timer > 0.35: 
                 self.is_attacking = False
                 self.animator.set_state('idle')

        self.animator.update(dt)