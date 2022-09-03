
import pygame
from sys import exit
from math import floor
import random


pygame.init()
screen = pygame.display.set_mode((256,240)) #resolucion
pygame.display.set_caption("Game") #nombre
clock = pygame.time.Clock() #limitar fps

game=True #empezar con el juego immediatamente

redvel = 0 #cantidad de rojo
cactx = 0 #x de cacrus
cactvel = 6 #velocudad de cactus
truescore = 0 #Score de la pantalla

timer = 0
invtimer = 0 #timer invertido para invunerabilidad
dt = 1 #velocidad de score
score = 0 

lives = 3

surface = pygame.transform.scale(pygame.image.load("Game/Walthu.png"),(32,64)).convert_alpha() #crear personaje y meterle texturas
rect = surface.get_rect(bottomleft = (0,240-8))  #crear rectangulo al personaje
surface.set_colorkey("white") #croma key
g = 0 #gravedad
z = 2 #aumentador de score que va decayendo a 0
h = 0 #creo que no sirve para nada

font = pygame.font.Font(None, 40) #crar letra


sky = pygame.Surface((700,400)) #crear cielo
sky.fill("sky blue")

floor = pygame.Surface((256,8)) #crear suelo
floor.fill("yellow")

cactus = pygame.transform.scale(pygame.image.load("Game/Cactus.png"),(32,64)).convert_alpha() #crear cacts
cactus.set_colorkey("white") #croma key
crect = cactus.get_rect(bottomleft = (600,240-8)) #crear rectangulo

rojo = pygame.Surface((256,240)) #crear rojo encima de la pantalla ppara cuando te haces daño
rojo.fill("red") #llenarlo de rojo

life = pygame.Surface((8*3,8)) #GUI de vida
life.fill("red") # llenarlo de rojo
liferect = life.get_rect() #crar rectangulo

while True:
    
    text = font.render(str(truescore), True, "black") #cear texto con score
    
    for event in pygame.event.get(): #si pasa algo
        if event.type == pygame.QUIT: #si le das a X
            pygame.quit()# se cierra
            exit()
        if event.type == pygame.KEYDOWN: #si le das a un boton
            if event.key == pygame.K_SPACE and game: #si le das a espacio mientras que el juego va en marcha
                if rect.bottom > 232:# y el personaje esta en el suelo
                    g = -18 #salta
            elif event.key == pygame.K_SPACE and not game: #pero le das a espacio mientras que el juego no esta en marcha
                game = True #poner el juego en maercha
                redvel = 0 #reiniciar todas las variables ---
                cactx = 0
                cactvel = 6
                truescore = 0
                timer = 0
                invtimer = 0
                dt = 1
                score = 0
                lives = 3
                liferect.x = 0
                g = 0
                z = 2
                h=0
                crect.x = 700

        
    
    if game: #si el juego esta en marcha
        if rect.bottom > 240-9: #si el personaje esta por debajo del suelo
            rect.bottom = 240-9 #llevarlo arriba
        
        #enseñar todos los objetos
        screen.blit(sky,(0,0))
        screen.blit(surface,rect)
        screen.blit(cactus,crect)
        screen.blit(floor,(0,240-8))
        screen.blit(life,liferect)
        screen.blit(text, (0,8))
        screen.blit(rojo,(0,0))
        
        g += 1 #aumentar g
        rect.y += g #bajar el personaje por g
        crect.left -= cactvel #mover el cactus por su velocidad
        
        timer += 1 #aumentar el timer
        invtimer = invtimer -1 #disminur el invtimer
        
        score = score + dt #aumentar score por su velocudad

        if timer == 600: #si han pasado 10s:
            timer = 0 
            cactvel += z #aumentar la velocidad del cactus por z
            z = z - z/1.5 #disminuir z por z/1.5
            dt = dt + 0.5 #aumentar la velocidad de score por 0.5

        if timer % 30 == 0: #cada 30 tics
            truescore = int(score/30) #actualizar el score de la pantalla
        
        if crect.right < 0: #si el cactus se va de la pantalla:
            crect.left = random.randrange(300,500) #mover el cactus a una locacion random fuera de la pantalla
        
        
        if rect.bottom > crect.top and crect.left < rect.right: #si el jugador toca el cactus:
            if invtimer < 0: #y si no ha tocado cactus en los ultimos segundos
                redvel=100 #llenar la pantalla de rojo
                lives = lives - 1 #quitar una vida
                liferect.x = liferect.x - 8 #actualizar la GUI
                if lives <= 0: #y si tienes 0 vidas y menos, te mueres
                    game = False
            invtimer = 1 #reiniciar timer de invulnerabilidad
        redvel = redvel -2 #bajar la cantidad de rojo por 2 cada tick
        rojo.set_alpha(redvel) #actualizar lo rojo
    
    else: #si no estas jugando(Te has muerto)
        screen.fill("black")#llenar la pantalla de negro
        todisplay = "SCORE:" + str(truescore) #enseñar la puntuacion vvv
        text = font.render(todisplay, True, "white")
        screen.blit(text, (0,0)) #poner el texto en la pantalla
        
    pygame.display.update()#actualizar la pantalla
    clock.tick(60)#limitar fps