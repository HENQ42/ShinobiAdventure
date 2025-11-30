import sys
import pgzrun
import pygame
import random
from pygame import Rect

# --- CONFIGURAÇÃO DE CAMINHOS ---
sys.path.append('class')
from hero import Hero
from enemy import Enemy

# --- CONFIGURAÇÕES GLOBAIS ---
WIDTH = 800
HEIGHT = 600
TITLE = "Shinobi Adventure"
DEBUG_MODE = True  # Mude para False se quiser esconder as caixas coloridas

# --- ESTADOS DO JOGO ---
STATE_MENU = 0
STATE_GAME = 1
STATE_GAMEOVER = 2
STATE_VICTORY = 3

current_state = STATE_MENU
sound_enabled = True

# --- VARIÁVEIS GLOBAIS ---
hero = None
enemies = []
platforms = []
victory_timer = 0  # Cronômetro para a tela de vitória

# Variáveis para imagens processadas (Redimensionadas)
background_img = None
platform_img = None
btn_start_img = None
btn_exit_img = None
btn_exit_small_img = None
btn_sound_on_img = None
btn_sound_off_img = None

music_playing = False

# --- INTERFACE (UI - HITBOXES) ---

# 1. MENU PRINCIPAL (Botões centralizados)
btn_start_rect = Rect((350, 200), (100, 100)) 
btn_exit_rect = Rect((350, 320), (100, 100))

# 2. UI DE JOGO (Canto Superior Direito)
btn_sound_rect = Rect((730, 20), (50, 50))      # Botão de Som
btn_game_exit_rect = Rect((670, 20), (50, 50))  # Botão Sair (In-game)

# --- INICIALIZAÇÃO ---
def init_game():
    global background_img, platform_img, hero, enemies, platforms
    global btn_start_img, btn_exit_img, btn_exit_small_img
    global btn_sound_on_img, btn_sound_off_img
    global victory_timer
    
    victory_timer = 0
    
    # 1. Carregar e Redimensionar Imagens
    
    # Fundo (Redimensiona para 800x600)
    if hasattr(images, 'background'):
        background_img = pygame.transform.smoothscale(images.background, (WIDTH, HEIGHT))
    
    # Plataforma (Redimensiona para 32x14 pixels)
    if hasattr(images, 'platform'):
        platform_img = pygame.transform.scale(images.platform, (32, 14))
    
    # Botões do Menu (Redimensiona para 100x100 - Quadrado)
    if hasattr(images, 'btn_start'):
        btn_start_img = pygame.transform.smoothscale(images.btn_start, (100, 100))
    if hasattr(images, 'btn_exit'):
        btn_exit_img = pygame.transform.smoothscale(images.btn_exit, (100, 100))
        # Versão pequena para usar dentro do jogo (50x50)
        btn_exit_small_img = pygame.transform.smoothscale(images.btn_exit, (50, 50))

    # Botões de Som (50x50)
    if hasattr(images, 'btn_sound_on'):
        btn_sound_on_img = pygame.transform.smoothscale(images.btn_sound_on, (50, 50))
    if hasattr(images, 'btn_sound_off'):
        btn_sound_off_img = pygame.transform.smoothscale(images.btn_sound_off, (50, 50))

    # 2. Criar Mapa (Plataformas)
    platforms = []
    block_w = 32
    block_h = 14
    
    # Chão (Base)
    for i in range(0, WIDTH, block_w):
        platforms.append(Rect((i, HEIGHT - 40), (block_w, block_h)))
    
    # Ilhas Flutuantes
    platforms.append(Rect((200, 450), (block_w * 4, block_h)))
    platforms.append(Rect((450, 350), (block_w * 4, block_h)))
    platforms.append(Rect((100, 250), (block_w * 3, block_h)))
    platforms.append(Rect((600, 200), (block_w * 3, block_h))) # Ilha alta
    
    # 3. Criar Herói
    hero = Hero(50, 450)
    hero.setup_animations()
    
    # 4. Criar Inimigos (Vários espalhados)
    enemies = []
    # No Chão
    enemies.append(Enemy(300, HEIGHT - 130, patrol_distance=100))
    enemies.append(Enemy(600, HEIGHT - 130, patrol_distance=100))
    # Nas Plataformas
    enemies.append(Enemy(450, 350 - 80, patrol_distance=50))
    enemies.append(Enemy(120, 250 - 80, patrol_distance=30))
    enemies.append(Enemy(620, 200 - 80, patrol_distance=30))
    
    # Iniciar música
    if sound_enabled:
        play_music()

def play_music():
    global music_playing
    if sound_enabled and not music_playing:
        try:
            music.play('theme')
            music.set_volume(0.5)
            music_playing = True
        except: pass

def stop_music():
    global music_playing
    music.stop()
    music_playing = False

# Chama a inicialização pela primeira vez
init_game()

# --- LOOP DE DESENHO (DRAW) ---
def draw():
    screen.clear()
    
    # Desenha Fundo
    if background_img: 
        screen.blit(background_img, (0, 0))
    
    # --- TELAS ---
    if current_state == STATE_MENU:
        draw_menu()
        
    elif current_state == STATE_GAME:
        draw_game()
        # Botão de Sair (In-game)
        if btn_exit_small_img:
            screen.blit(btn_exit_small_img, (btn_game_exit_rect.x, btn_game_exit_rect.y))
        if DEBUG_MODE: screen.draw.rect(btn_game_exit_rect, "yellow")

    elif current_state == STATE_GAMEOVER:
        draw_game() # Mantém o jogo ao fundo
        screen.draw.text("GAME OVER", center=(WIDTH/2, HEIGHT/2), fontsize=60, color="red", shadow=(1,1))
        screen.draw.text("Espaço para Reiniciar", center=(WIDTH/2, HEIGHT/2 + 60), fontsize=30, color="white")
        
    elif current_state == STATE_VICTORY:
        draw_game()
        screen.draw.text("VITÓRIA!", center=(WIDTH/2, HEIGHT/2), fontsize=80, color="green", shadow=(1,1))
        screen.draw.text("Inimigos derrotados!", center=(WIDTH/2, HEIGHT/2 + 60), fontsize=30, color="white")
        
        # Só mostra a mensagem de sair depois de 3 segundos
        if victory_timer > 3.0:
            screen.draw.text("Pressione ESPAÇO para Voltar", center=(WIDTH/2, HEIGHT/2 + 120), fontsize=25, color="yellow")

    # --- UI GLOBAL ---
    # Botão de Som
    icon = btn_sound_on_img if sound_enabled else btn_sound_off_img
    if icon: 
        screen.blit(icon, (btn_sound_rect.x, btn_sound_rect.y))
    if DEBUG_MODE: screen.draw.rect(btn_sound_rect, "yellow")

def draw_menu():
    screen.draw.text("SHINOBI ADVENTURE", center=(WIDTH/2, 120), fontsize=60, color="orange", shadow=(1,1))
    
    if btn_start_img: screen.blit(btn_start_img, (btn_start_rect.x, btn_start_rect.y))
    if btn_exit_img: screen.blit(btn_exit_img, (btn_exit_rect.x, btn_exit_rect.y))
    
    if DEBUG_MODE:
        screen.draw.rect(btn_start_rect, "yellow")
        screen.draw.rect(btn_exit_rect, "yellow")

def draw_game():
    # Desenha Plataformas (Com tiling da textura)
    for plat_rect in platforms:
        if platform_img:
            tiles = int(plat_rect.width // 32)
            for i in range(tiles):
                screen.blit(platform_img, (plat_rect.x + (i * 32), plat_rect.y))
        if DEBUG_MODE: screen.draw.rect(plat_rect, "green")
    
    # Desenha Inimigos (Apenas os vivos)
    for enemy in enemies:
        if enemy.alive:
            enemy.draw(screen)
            if DEBUG_MODE: screen.draw.rect(enemy.rect, "red")
        
    # Desenha Herói
    hero.draw(screen)
    if DEBUG_MODE: screen.draw.rect(hero.rect, "blue")
    
    # HUD
    screen.draw.text(f"HP: {hero.hp}", (20, 20), fontsize=30, color="white")
    
    # Contagem de Inimigos restantes
    remaining = sum(1 for e in enemies if e.alive)
    screen.draw.text(f"Inimigos: {remaining}", (20, 50), fontsize=30, color="red")
    
    if DEBUG_MODE:
        screen.draw.text("DEBUG ON", (20, 80), fontsize=20, color="yellow")

# --- LOOP DE LÓGICA (UPDATE) ---
def update(dt):
    global current_state, victory_timer
    
    if current_state == STATE_GAME:
        hero.input(keyboard)
        hero.update(dt)
        hero.move_and_collide(platforms)
        
        # Morte por queda
        if hero.y > HEIGHT:
            hero.hp = 0
            try: sounds.hit.play()
            except: pass
        
        enemies_alive_count = 0
        
        for enemy in enemies:
            # Se morreu, pula (não atualiza física nem lógica)
            if not enemy.alive:
                continue 
            
            enemies_alive_count += 1
            enemy.update(dt)
            enemy.move_and_collide(platforms)
            
            # --- COMBATE ---
            
            # 1. Herói Ataca Inimigo (Hit Kill)
            if hero.is_attacking:
                dist_x = abs(hero.x - enemy.x)
                dist_y = abs(hero.y - enemy.y)
                # Verifica distância
                if dist_x < 100 and dist_y < 60:
                    enemy.alive = False
                    try: sounds.slash.play()
                    except: pass
            
            # 2. Inimigo Toca Herói (Dano sem knockback)
            if hero.rect.colliderect(enemy.rect):
                 if not hero.is_attacking:
                     hero.hp -= 1
                     if hero.hp <= 0:
                         current_state = STATE_GAMEOVER
                         try: sounds.hit.play()
                         except: pass

        if hero.hp <= 0:
            current_state = STATE_GAMEOVER
            
        # --- VITÓRIA ---
        if enemies_alive_count == 0:
            current_state = STATE_VICTORY
            victory_timer = 0 # Inicia contagem

    elif current_state == STATE_GAMEOVER:
        if keyboard.space:
            init_game()
            current_state = STATE_GAME

    elif current_state == STATE_VICTORY:
        # Conta tempo para ler a mensagem
        victory_timer += dt
        if victory_timer > 3.0:
            if keyboard.space:
                init_game()
                current_state = STATE_GAME

# --- EVENTOS DE MOUSE ---
def on_mouse_down(pos):
    global current_state, sound_enabled
    
    # Clique Som (Global)
    if btn_sound_rect.collidepoint(pos):
        sound_enabled = not sound_enabled
        if sound_enabled: play_music()
        else: stop_music()
            
    # Menu Principal
    if current_state == STATE_MENU:
        if btn_start_rect.collidepoint(pos):
            try: sounds.click.play()
            except: pass
            current_state = STATE_GAME
        elif btn_exit_rect.collidepoint(pos):
            sys.exit()
            
    # Jogo Rodando
    elif current_state == STATE_GAME:
        if btn_game_exit_rect.collidepoint(pos):
             current_state = STATE_MENU

# Inicia o Jogo
pgzrun.go()