import pygame
import random
import sys


pygame.init()
pygame.mixer.init()


# Dimensiones de la ventana
ANCHO, ALTO = 800, 600
ventana = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Mi Juego en Pygame")


# Colores
BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 55)





# Fondo
fondo = pygame.image.load("assets/img/ciudad9.jpg") 
fondo2 = pygame.image.load("assets/img/ciudad8.jpeg")
fondo_game_over = pygame.image.load("assets/img/game_over3.jpg")
fondo_menu = pygame.image.load("assets/img/menu3.jpg")

# Escalar fondo de game over
fondo_game_over = pygame.transform.scale(fondo_game_over, (ANCHO, ALTO))
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO, ALTO))

# Animación de explosión
explosion_lista = []
for i in range(1, 6):
    imagen = pygame.image.load(f"assets/img/explosion{i}.png").convert_alpha() 
    explosion_lista.append(imagen)

# Sonidos
laser_sonido = pygame.mixer.Sound("assets/sound/laser.wav")
explosion_sonido = pygame.mixer.Sound("assets/sound/EXPLODE.WAV")
golpe_sonido = pygame.mixer.Sound("assets/sound/hit.wav")
intro_sonido = pygame.mixer.Sound("assets/sound/superman_sound.wav")
power_up = pygame.mixer.Sound("assets/sound/power_up.wav")
power_down = pygame.mixer.Sound("assets/sound/dolor_grito2.mp3")
Hernan_audio = pygame.mixer.Sound("assets/sound/Hernan_audio.wav")
ladrido_audio =  pygame.mixer.Sound("assets/sound/ladrido.mp3")

# Variables de juego
fps = 60
reloj = pygame.time.Clock()
puntaje = 0
vida = 100
fondo_x = 0
estado_juego = "MENU"





# --- FUNCIONES AUXILIARES ---
def mostrar_puntacion(surface, texto, tamaño, x, y):
    fuente = pygame.font.SysFont(None, tamaño, bold=True)
    texto_surface = fuente.render(texto, True, BLANCO)
    texto_rect = texto_surface.get_rect()
    texto_rect.midtop = (x, y)
    surface.blit(texto_surface, texto_rect)

def dibujar_barra_vida(surface, x, y, nivel):
    largo = 100
    alto = 20
    if nivel < 0: nivel = 0
    relleno = int((nivel / 100) * largo)
    borde = pygame.Rect(x, y, largo, alto)
    relleno_rect = pygame.Rect(x, y, relleno, alto)
    pygame.draw.rect(surface, ROJO, relleno_rect)
    pygame.draw.rect(surface, NEGRO, borde, 2)
    
    

# --- CLASES DE SPRITES ---

# Balas que van hacia la DERECHA
class Balas(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/img/laser1.png").convert_alpha() 
        self.rect = self.image.get_rect()
        self.rect.centery = y  
        self.rect.left = x
        self.velocidad = 20

    def update(self):
        self.rect.x += self.velocidad
        if self.rect.left > ANCHO:
            self.kill()
             
# Balas que van hacia la IZQUIERDA
class Balas_V(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/img/laser1.png").convert_alpha() 
        self.image = pygame.transform.flip(self.image, True, False)
        self.rect = self.image.get_rect()
        self.rect.centery = y  
        self.rect.right = x
        self.velocidad = -20 
        
    def update(self):
        self.rect.x += self.velocidad
        if self.rect.right < 0:
            self.kill()

class Meteorito(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/img/meteorGrey_big1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1, 10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > ALTO or self.rect.left < -50 or self.rect.right > ANCHO + 50:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(1, 10)
            self.speedx = random.randrange(-5, 5)
            
class Sol(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/img/botiquin.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-2, 2)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > ALTO or self.rect.left < -50 or self.rect.right > ANCHO + 50:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 5)
            self.speedx = random.randrange(-2, 2)  
            
class kritonita(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/img/kritonita.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (50, 50))
        self.image.set_colorkey(NEGRO)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(ANCHO - self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(2, 5)
        self.speedx = random.randrange(-2, 2)
        
    def update(self):
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > ALTO or self.rect.left < -50 or self.rect.right > ANCHO + 50:
            self.rect.x = random.randrange(ANCHO - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 5)
            self.speedx = random.randrange(-2, 2)             

class Jugador(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        #tsunami_A = pygame.image.load("assets/img/tsunami-2.png")
        tsunami_A = pygame.image.load("assets/img/tsunami.png")
        tsunami_P = pygame.image.load("assets/img/tsunami.png")
        tsunami_G = pygame.image.load("assets/img/tsunami3.png")
        tsunami_V = pygame.image.load("assets/img/tsunami2.png")
        #Hernan_cameo = pygame.image.load("assets/img/Hernan_cameo3.png")

        self.tsunami_A = pygame.transform.scale(tsunami_A, (150, 100))
        self.tsunami_G = pygame.transform.scale(tsunami_G, (190, 120))
        self.tsunami_P = pygame.transform.scale(tsunami_P, (190, 120))
        self.tsunami_V = pygame.transform.scale(tsunami_V, (190, 120))
        
        
        #self.Hernan_cameo = pygame.transform.scale(Hernan_cameo, (210, 460))
         
         
        self.image = self.tsunami_A
        self.rect = self.image.get_rect()
        self.rect.center = (ANCHO // 3, ALTO - 100)
        self.velocidad = 5
        self.timer_golpe = 0
        self.direccion = "DERECHA" 

    def laser(self):
        if self.direccion == "DERECHA":
            rayo = Balas(self.rect.right - 30, self.rect.centery - 30)
        else: 
            rayo = Balas_V(self.rect.left + 30, self.rect.centery - 30)
            
        all_sprites.add(rayo)
        balas_list.add(rayo)
        laser_sonido.play()
        
    def update(self):
        if self.timer_golpe > 0:
            self.timer_golpe -= 1
            if self.timer_golpe == 0:
                if self.direccion == "IZQUIERDA":
                    self.image = self.tsunami_V
                else:
                    self.image = self.tsunami_A

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
            self.direccion = "IZQUIERDA" 
            if self.timer_golpe == 0: self.image = self.tsunami_V
            
        if keys[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad
            self.direccion = "DERECHA" 
            if self.timer_golpe == 0: self.image = self.tsunami_A
            
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.velocidad
        if keys[pygame.K_DOWN] and self.rect.bottom < ALTO:
            self.rect.y += self.velocidad    

class Explosion(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.frames = explosion_lista
        self.frame_index = 0
        self.image = self.frames[self.frame_index]
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.frame_rate = 5
        self.counter = 0

    def update(self):
        self.counter += 1
        if self.counter >= self.frame_rate:
            self.counter = 0
            self.frame_index += 1
            if self.frame_index < len(self.frames):
                self.image = self.frames[self.frame_index]
            else:
                self.kill()

def reiniciar_juego():
    global puntaje, vida, all_sprites, balas_list, meteorito_list, jugador, sol_list, kritonita_list
    puntaje = 0
    vida = 100
    all_sprites = pygame.sprite.Group()
    balas_list = pygame.sprite.Group()
    meteorito_list = pygame.sprite.Group()
    sol_list = pygame.sprite.Group()
    kritonita_list = pygame.sprite.Group()
   
    jugador = Jugador()
    all_sprites.add(jugador)
    
    for _ in range(5):
        m = Meteorito()
        all_sprites.add(m)
        meteorito_list.add(m)
        
    for _ in range(2):    
        s = Sol()
        all_sprites.add(s)
        sol_list.add(s)
        
    for _ in range(2):
        k = kritonita()
        all_sprites.add(k)
        kritonita_list.add(k)

# inicio
reiniciar_juego()


ejecutando = True
while ejecutando:
    reloj.tick(fps)

    # Captura de Eventos
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            ejecutando = False
            
        if estado_juego == "MENU":
            intro_sonido.play()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_SPACE: 
                    estado_juego = "JUGANDO"
                    intro_sonido.stop()
            
        elif estado_juego == "JUGANDO":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_n:    
                    jugador.laser()
                    
        elif estado_juego == "GAME_OVER":
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_r:
                    reiniciar_juego()
                    estado_juego = "JUGANDO"
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False    
                    
                
                    
    # Renderizar Menú si corresponde
    if estado_juego == "MENU":
        ventana.blit(fondo_menu, (0, 0))
        mostrar_puntacion(ventana, " tsunami SALVA A VENEZUELA", 55, ANCHO // 2, ALTO // 10)
        mostrar_puntacion(ventana, "Presiona ESPACIO para comenzar", 30, ANCHO // 2, ALTO // 2)
        ladrido_audio.play()
      
       
       
    elif estado_juego == "JUGANDO":
        fondo_x -= 2
        if fondo_x <= -ANCHO:
            fondo_x = 0
            
            
            
        all_sprites.update()
        
   
            
    
            
        # Colisiones: Láseres destruyen Meteoritos
        impactos = pygame.sprite.groupcollide(meteorito_list, balas_list, True, True)
        for meteorito in impactos:  
            explosion_sonido.play()
            puntaje += 10
            expl = Explosion(meteorito.rect.centerx, meteorito.rect.centery)
            all_sprites.add(expl)
            
            nuevo_meteorito = Meteorito()
            all_sprites.add(nuevo_meteorito)
            meteorito_list.add(nuevo_meteorito)


        golpes_recibidos = pygame.sprite.spritecollide(jugador, meteorito_list, True)
        for golpe in golpes_recibidos:
            jugador.image = jugador.tsunami_G
            jugador.timer_golpe = 12
            vida -= 15          
            golpe_sonido.play()   
            
            expl = Explosion(jugador.rect.centerx, jugador.rect.centery)
            all_sprites.add(expl)
            
            nuevo_meteorito = Meteorito()
            all_sprites.add(nuevo_meteorito)
            meteorito_list.add(nuevo_meteorito)

            if vida <= 0:
                vida = 0
                estado_juego = "GAME_OVER"
                
   #soles
        soles_recogidos = pygame.sprite.spritecollide(jugador, sol_list, True)
        for sol in soles_recogidos:
            vida += 20 
            #power_up.play()
            ladrido_audio.play ()
            if vida > 100: 
                vida = 100
            nuevo_sol = Sol()
            all_sprites.add(nuevo_sol)
            sol_list.add(nuevo_sol)
            
        # Kriptonita recogida
        kritonita_recogidas = pygame.sprite.spritecollide(jugador, kritonita_list, True)
        for kriton in kritonita_recogidas:
            vida -= 30 
            jugador.image = jugador.tsunami_G
            jugador.timer_golpe = 12
            power_down.play() 
            
            if vida <= 0: 
                vida = 0
                estado_juego = "GAME_OVER"
                
            nueva_kritonita = kritonita()
            all_sprites.add(nueva_kritonita)
            kritonita_list.add(nueva_kritonita)

       
        ventana.blit(fondo, (fondo_x, 0))
        ventana.blit(fondo, (fondo_x + ANCHO, 0))
        
        all_sprites.draw(ventana)
        mostrar_puntacion(ventana, f"Puntaje: {puntaje}", 25, ANCHO // 2, 10)
        dibujar_barra_vida(ventana, 10, 40, vida)
        
    elif estado_juego == "GAME_OVER":
        ventana.blit(fondo_game_over, (0, 0))
        mostrar_puntacion(ventana, "GAME OVER", 50, ANCHO // 2, ALTO // 3)
        mostrar_puntacion(ventana, f"Puntaje Final: {puntaje}", 30, ANCHO // 2, ALTO // 2)
        mostrar_puntacion(ventana, "Presiona 'R' para reiniciar o 'ESC' para salir", 25, ANCHO // 2, ALTO * 2 // 3)

    pygame.display.flip()

pygame.quit()
sys.exit()