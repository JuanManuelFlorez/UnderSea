#!/usr/bin/env python
# -*- coding: utf-8 -*-
 
# Módulos
import sys, pygame, random, time
from pygame.locals import *

 
# Tamaño pantalla
WIDTH = 1200
HEIGHT = 600

# --------------------------------------------------------------------- 
# Clases
# ---------------------------------------------------------------------
class Buzo(pygame.sprite.Sprite): # Clase de buzo
	def __init__(self,imagen,transp,posx,posy,velx,vely):
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image(imagen, transp)
		self.rect = self.image.get_rect()
		self.rect.centerx = posx
		self.rect.centery = posy
		self.speed = [velx, vely]

	def actualizar(self, time, buzo1, Tiburon1, puntos):
		self.rect.centerx -= self.speed[0] * time
		if self.rect.left <= 0: 			#Control de las desapariciones y apariciones aleatorias
			self.rect.centery = random.randrange(30, 580, 60)				
			self.rect.centerx = WIDTH-50
		if pygame.sprite.collide_rect(buzo1, Tiburon1): #Control de las colisiones, apariciones aleatorias y puntos
			self.rect.centerx = WIDTH-50			
			self.rect.centery = random.randrange(30, 580, 60)		
			puntos[0] += 10
		return puntos

			

class Tiburon(pygame.sprite.Sprite): #Clase Tiburon
	def __init__(self, x):           #Posicion del tiburon, velocidad y carga de la imagen
		pygame.sprite.Sprite.__init__(self)
		self.image = load_image("images/shark.png") 
		self.rect = self.image.get_rect()
		self.rect.centerx = x
		self.rect.centery = HEIGHT / 2 
		self.speed = 0.51
		
	def mover(self, time, keys, buzo1, buzo2, buzo3, buzo4, Tiburon1, sound1, boca):	
	# movimiento tiburon mediante teclas
		if self.rect.top >= 0:
			if keys[K_UP]:
				self.rect.centery -= self.speed * time
		if self.rect.bottom <= HEIGHT:
			if keys[K_DOWN]:
				self.rect.centery += self.speed * time
	# colisiones y sonido al colisionar
		if pygame.sprite.collide_rect(buzo1, Tiburon1):
			self.image = load_image("images/shark1.png")
			sound1.play()			
		if pygame.sprite.collide_rect(buzo2, Tiburon1):
			self.image = load_image("images/shark1.png")
			sound1.play()
		if pygame.sprite.collide_rect(buzo3, Tiburon1):
			self.image = load_image("images/shark1.png")
			sound1.play()
		if pygame.sprite.collide_rect(buzo4, Tiburon1):
			self.image = load_image("images/shark1.png")
			sound1.play()
		if boca > 100:
			self.image = load_image("images/shark.png")


# ---------------------------------------------------------------------
# Funciones generales
# ---------------------------------------------------------------------
def load_image(filename, transparent=False): #Carga de imagenes
        try: image = pygame.image.load(filename)
        except pygame.error, message:
                raise SystemExit, message
        #image = image.convert()
        if transparent:
                color = image.get_at((0,0))
                image.set_colorkey(color, RLEACCEL)
        return image
        
def texto(texto, posx, posy, color=(255, 255, 255)): #Fuente, tamaño y color del texto
	fuente = pygame.font.Font("images/ASMAN.TTF", 25)
	salida = pygame.font.Font.render(fuente, texto, 1, color)
	salida_rect = salida.get_rect()
	salida_rect.centerx = posx
	salida_rect.centery = posy
	return salida, salida_rect

# ---------------------------------------------------------------------
# Funciones del juego
# ---------------------------------------------------------------------

#pantalla  para pausar la partida
def pause(): 
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	intro_imag = load_image('images/intro.jpg')
	pausado = True
	
	while pausado:
		p_shark, p_shark_rect = texto(str("PAUSE"), WIDTH-110, 580)
		p_salir, p_salir_rect = texto(str("Pulsa Q p,ara salir"), WIDTH-110, 40)
		p_continuar, p_continuar_rect = texto(str("Pulsa C p,ara continuar"), WIDTH-110, 65)
		
		
		screen.blit(intro_imag, (0, 0))
		screen.blit(p_shark, p_shark_rect)
		screen.blit(p_salir, p_salir_rect)
		screen.blit(p_continuar, p_continuar_rect)
		pygame.display.flip()
		
		
		for eventos in pygame.event.get():
			if eventos.type ==pygame.QUIT:
				pygame.quit()
				quit()
			if eventos.type == pygame.KEYDOWN:
				if eventos.key == pygame.K_c:
					pausado = False	
				if eventos.key == pygame.K_q:
					pygame.quit()
					quit()

#Pantalla final al ganar la partida
def winner(puntos): 
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	intro_imag = load_image('images/intro.jpg')
	ganar = True
	
	while ganar:
		p_win, p_win_rect = texto(str("¡¡¡Has ganado!!!"), WIDTH-110, 15)
		p_salir, p_salir_rect = texto(str("Pulsa Q p,ara salir"), WIDTH-110, 40)
		p_continuar, p_continuar_rect = texto(str("Pulsa C p,ara reiniciar"), WIDTH-110, 65)
		you_win = load_image('images/win.png')			

		screen.blit(intro_imag, (0, 0))
		screen.blit(you_win, (0, 0))
		screen.blit(p_win, p_win_rect)
		screen.blit(p_continuar, p_continuar_rect)
		screen.blit(p_salir, p_salir_rect)
		pygame.display.flip()
		
		for eventos in pygame.event.get():
			if eventos.type ==pygame.QUIT:
				pygame.quit()
				quit()
			if eventos.type == pygame.KEYDOWN:
				if eventos.key == pygame.K_c:
					ganar = False
					gameover = True
					puntos[0] = 0	 
				if eventos.key == pygame.K_q:
					pygame.quit()
					quit()

#Pantalla final al perder la partida
def perder(puntos):
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	intro_imag = load_image('images/intro.jpg')
	perder = True
	
	while perder:
		p_loser, p_loser_rect = texto(str("¡¡¡Has perdido!!!"), WIDTH-110, 15)
		p_salir, p_salir_rect = texto(str("Pulsa Q p,ara salir"), WIDTH-110, 40)
		p_continuar, p_continuar_rect = texto(str("Pulsa C p,ara reintentar"), WIDTH-110, 65)
		you_lose = load_image('images/over.png')			

		screen.blit(intro_imag, (0, 0))
		screen.blit(you_lose, (0, 0))
		screen.blit(p_loser, p_loser_rect)
		screen.blit(p_continuar, p_continuar_rect)
		screen.blit(p_salir, p_salir_rect)
		pygame.display.flip()
		
		for eventos in pygame.event.get():
			if eventos.type ==pygame.QUIT:
				pygame.quit()
				quit()
			if eventos.type == pygame.KEYDOWN:
				if eventos.key == pygame.K_c:
					perder = False
					gameover = True
					puntos[0] = 0
	 
				if eventos.key == pygame.K_q:
					pygame.quit()
					quit()

# ---------------------------------------------------------------------
# Programa Principal
# --------------------------------------------------------------------- 

def main():
# Inicializaciones pygame
	screen = pygame.display.set_mode((WIDTH, HEIGHT))
	pygame.display.set_caption("FEED THE SHARK")
	
	background_image = load_image('images/sea4.jpg')
	intro_image = load_image('images/intro.jpg')
	buzo1 = Buzo("images/buzo.png", True, WIDTH-50, HEIGHT/2-60, 0.3, 0)
	buzo2 = Buzo("images/buzo.png", True, WIDTH-50, HEIGHT/2+60, 0.3, 0)
	buzo3 = Buzo("images/buzo.png", True, WIDTH-50, HEIGHT/2+200, 0.3, 0)
	buzo4 = Buzo("images/buzo.png", True, WIDTH-50, HEIGHT/2-200, 0.3, 0)

# Sonidos 
	sound1 = pygame.mixer.Sound('images/yumm.wav')
	pygame.mixer.music.load("images/ambiental.mp3")
	pygame.mixer.music.play(1)
	pygame.mixer.music.set_volume(0.1)
# Inicializaciones elementos de juego
	Tiburon1 = Tiburon(150)
	puntos = [0]
	clock = pygame.time.Clock()
	intro = True
	gameover = False
	timer = 0
	boca = 0

#Pantalla de intro
	while intro:
		for eventos in pygame.event.get():
			if eventos.type ==pygame.QUIT:
				pygame.quit()
				quit()
			if eventos.type == pygame.KEYDOWN:
				if eventos.key == pygame.K_c:
					intro = False	
				if eventos.key == pygame.K_q:
					pygame.quit()
					quit()

					
		p_salir, p_salir_rect = texto(str("Pulsa Q p,ara salir"), WIDTH-110, 40)
		p_continuar, p_continuar_rect = texto(str("Pulsa C p,ara iniciar"), WIDTH-110, 65)
		p_pausar, p_pausar_rect = texto(str("Pulsa P p,ara p,ausar"), WIDTH-110, 90)
		p_shark, p_shark_rect = texto(str("FEED THE SHARK"), WIDTH-110, 580)
		p_points, p_points_rect = texto(str("Consigue 700 puntos en 30 segundos"), WIDTH-200, 300)
		p_sing, p_sing_rect = texto(str("by JM"), WIDTH-1050, 300)
		
		screen.blit(intro_image, (0, 0))
		screen.blit(p_salir, p_salir_rect)
		screen.blit(p_continuar, p_continuar_rect)
		screen.blit(p_pausar, p_pausar_rect)
		screen.blit(p_shark, p_shark_rect)
		screen.blit(p_points, p_points_rect)
		screen.blit(p_sing, p_sing_rect)
		pygame.display.flip()

#Bucle del juego 
	while not gameover:
		time = clock.tick(60)
		keys = pygame.key.get_pressed()
		timer += 1
		boca += 1
		
		for eventos in pygame.event.get():
			if eventos.type == QUIT:
				sys.exit(0)		
			elif eventos.type == pygame.KEYDOWN:
				if eventos.key == pygame.K_q:
					pygame.quit()
					quit()			
				elif eventos.key == pygame.K_p:
					pause()
		
# Procesamos jugador
		puntos = buzo1.actualizar(time, buzo1, Tiburon1, puntos)
		puntos = buzo2.actualizar(time, buzo2, Tiburon1, puntos)
		puntos = buzo3.actualizar(time, buzo3, Tiburon1, puntos)
		puntos = buzo4.actualizar(time, buzo4, Tiburon1, puntos)
		p_jug, p_jug_rect = texto(str(puntos[0]), WIDTH-50, 40)
		p_timer, p_timer_rect = texto(str(timer/60), WIDTH-1100, 40)
		p_tiempo1, p_tiempo1_rect = texto(str("time:"), WIDTH-1150, 40)
		p_score, p_score_rect = texto(str("score:"), WIDTH-110, 40)
		p_shark, p_shark_rect = texto(str("Feed the shark"), WIDTH-110, 580)
		Tiburon1.mover(time, keys, buzo1, buzo2, buzo3, buzo4, Tiburon1, sound1, boca)
		buzo1.actualizar(time, buzo1, Tiburon1, puntos)
		buzo2.actualizar(time, buzo2, Tiburon1, puntos)
		buzo3.actualizar(time, buzo3, Tiburon1, puntos)
		buzo4.actualizar(time, buzo4, Tiburon1, puntos)
		
		if puntos[0]>= 700:
			winner(puntos)
			timer = 0
		if timer > 1800: # 1800 equivale a 30 segundos 
			perder(puntos)
			timer = 0
		if boca > 100:
			boca = 0
# Renderizamos
		screen.blit(background_image, (0, 0))
		screen.blit(p_jug, p_jug_rect)
		screen.blit(p_score, p_score_rect)
		screen.blit(p_timer, p_timer_rect)
		screen.blit(p_tiempo1, p_tiempo1_rect)
		screen.blit(p_shark, p_shark_rect)
		screen.blit(Tiburon1.image, Tiburon1.rect)
		screen.blit(buzo1.image, buzo1.rect)
		screen.blit(buzo2.image, buzo2.rect)
		screen.blit(buzo3.image, buzo3.rect)
		screen.blit(buzo4.image, buzo4.rect)
		pygame.display.flip()
				
	return 0

if __name__ == '__main__':
	pygame.init()
	main()

