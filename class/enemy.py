from entity import Entity
from animator import Animator
from spritesheet import SpriteSheet

class Enemy(Entity):
    def __init__(self, x, y, patrol_distance=200):
        super().__init__(x, y, 40, 80)
        self.start_x = x
        self.patrol_distance = patrol_distance
        self.speed = 2
        self.velocity_x = self.speed
        self.alive = True
        
        self.animator = Animator('walk')
        self.setup_animations()

    def setup_animations(self):
        # Carrega sprite do Samurai
        self.animator.add_animation('walk', SpriteSheet('samurai_run'), 0.12)
        # Opcional: Adicionar 'dead' se tiver sprite de morte

    def update(self, dt):
        if not self.alive:
            return

        super().apply_gravity()
        
        # IA de Patrulha
        if self.x > self.start_x + self.patrol_distance:
            self.velocity_x = -self.speed
            self.animator.facing_right = False
        elif self.x < self.start_x - self.patrol_distance:
            self.velocity_x = self.speed
            self.animator.facing_right = True
            
        self.x += self.velocity_x
        self.rect.x = self.x
        
        self.animator.update(dt)