# -*- encoding: utf-8 -*-
from agente import *
import pygame as py
import random
import sys
import json as js
#import pygame.color

from pygame.locals import *
py.init()
#Variables Globales
Ancho=1270
Alto=670
listaenemigo=[]
listavidas=[]
listaTierraAire=[]
segundo =0
numeroE=0
coor=(75,85)
#vistaDireccion=True #si esta mirando ala derecha su valor es true y esta viendo viendo ala izquierda es false
FuenteScore=py.font.Font("Fuentes/BAUHS93.ttf",40)
Score=FuenteScore.render("YO - ",1,py.Color("ghostwhite"))
TopScore=FuenteScore.render("000000",1,py.Color("ghostwhite"))
Yo=FuenteScore.render("YO",1,py.Color("brown1"))
Top=FuenteScore.render("TOP",1,py.Color("skyblue"))
Espaciado=0
ventana=py.display.set_mode((Ancho,Alto))
agentei_us = AgenteInteligente() #instancia de la clase agenteInteligente que servira para tomar las deciciones de los movimientos

class sprite_menu_pausa(py.sprite.Sprite):#crea un sprit para el menu de pausa.
	def __init__(self,posx,posy):
		py.sprite.Sprite.__init__(self)
		self.menu_resumir = py.image.load("sprites/pausa/pausa_resumir.png")
		self.menu_agente = py.image.load("sprites/pausa/pausa_activar_agente.png")
		self.menu_controles = py.image.load("sprites/pausa/pausa_controles.png")
		self.menu_salir = py.image.load("sprites/pausa/pausa_salir.png")
		self.listaMenu=[self.menu_resumir,self.menu_agente,self.menu_controles,self.menu_salir]
		self.seleccion = 0 #indica que comenzara en la primera posicion del arreglo, en este caso es la imagen pausaResumir.jpg
		self.menu_pausa=self.listaMenu[self.seleccion] 
		self.rect = self.menu_pausa.get_rect()
		self.rect.top=posy
		self.rect.left=posx

		self.resumir=True      		#variable que servira para indicar si la opcion resumir esta activa
		self.salir=False   			#variable que servira para indicar si la opcion salir esta activa
		self.agente = False 		#variable que servira para indicar si la opcion agente esta activa
		self.controles = False 	#variable que servira para indicar si la opcion controles esta activa

		self.menu_pausa.convert_alpha()  #funcion convert_alpha da la posibilidad de convertir una imagen a pixeles para dar transparencia
		self.menu_pausa.set_alpha(10) #establece la transparencia, 0-totalmente transparente, 255 totalmente opaco
		self.SonidoPausa=py.mixer.Sound("Sonidos/pausa.wav")
	def bajar(self):
		if self.seleccion < 3: #si la seleccion es menor que 3
			self.seleccion += 1 #entonces subimos una posicion para obtener la siguienteimagen en el arreglo
		else: #si la seleccion no es menor que 3
			self.seleccion = 0 #regresamos a la primera posicion del arreglo la seleccion 
		self.menu_pausa=self.listaMenu[self.seleccion] #se asigna la imagen correspondiente al sprite
		self.activar_opcion()

	def subir(self):
		if self.seleccion == 0: #si la seleccion es menor que 3
			self.seleccion = 3 #entonces subimos una posicion para obtener la siguienteimagen en el arreglo
		else: #si la seleccion no es menor que 3
			self.seleccion -= 1 #regresamos a la primera posicion del arreglo la seleccion 
		self.menu_pausa=self.listaMenu[self.seleccion] #se asigna la imagen correspondiente al sprite	
		self.activar_opcion()

	def activar_opcion(self):
		if self.seleccion == 0:			#si seleccion es 0, entonces es resumir
			self.resumir=True      		#variable resumir sera igual a true
			self.salir=False   			#variable salir sera igual a false
			self.agente = False 		#variable agente sera igual a false
			self.controles = False 	#variable controles sera igual a false

		if self.seleccion == 1:			#si seleccion es 1, entonces es activar agente
			self.resumir=False      		
			self.salir=False  			
			self.agente = True 		
			self.controles = False 	

		if self.seleccion == 2:			#si seleccion es 2, entonces es controles
			self.resumir=False      		
			self.salir=False  			
			self.agente = False 		
			self.controles = True 

		if self.seleccion == 3:			#si seleccion es 3, entonces es salir
			self.resumir=False      		
			self.salir=True  			
			self.agente = False 		
			self.controles = False 

def enviar_ambiente(player):
	'''Funcion que escribe en un archivo .json el estado del ambiente del juego'''
	contador_enemigos = 0 #variable para saber cuantos enemigos han sigo escritos en la funcion 

	posicion_player = {'Player':[{'posX':player.rect.left,'posY':player.rect.top}]} #diccionario que almacenara la posicion de la
	pos_enemigos = {} #diccionario que almacena las posiciones de los enemigos, en tuplas
	lista_enemigos = {'Enemigos':[{'posX':25,'posY':30},{'posX':40,'posY':45}]} #diccionario que almacenara la posicion de los enemigos que esten en el ambiente en formato arreglo .json
	
	posiciones_enemigos = '"Enemigos":['	#variable que almacena la lista de posiciones de los Enemigos
	print ("numero de enemigos: " + str(len(listaenemigo))) #manda a imprimir el tamaño de la lista de enemigos
	for en in listaenemigo: #recorre la lista de enemigos
		contador_enemigos+=1 #suma 1 a la variable contador de enemigos
		pos_enemigos[contador_enemigos] = {'posX':en.rect.left,'posY':en.rect.top} #inserta un nuevo enemigo al diccionario, tomando como nombre el numero de enemigo que es 

	lista_enemigos['Enemigos'] = [pos_enemigos] #al diccionario lista_enemigos se le envia las posiciones del amigos, por facilidad al momento de leer el archivo json

	posicion_player.update(lista_enemigos) #se forma un unico diccionario con las posiciones del enemigo mas las posiciones de todos los enemigos que esten presentes en el ambiente
	
	with open('medio.json', 'w') as archivo: #se abre una conexion con el archivo medio.json
  		js.dump(posicion_player, archivo)  #se manda a escribir en el archivo medio.json todas las posiciones de los objetos en el ambiente, si el archivo ya contiene datos entonces los sobre escribe

def pausa():
	py.init()
	reloj=py.time.Clock()
	imagenFondo=py.image.load("sprites/pausa/pausaCongelar.jpg")
	imagenFondo.convert_alpha()  #funcion convert_alpha da la posibilidad de convertir una imagen a pixeles para dar transparencia
	imagenFondo.set_alpha(100) #establece la transparencia, 0-totalmente transparente, 255 totalmente opaco
	
	menu_de_pausa = sprite_menu_pausa(230,120)
	ventana.blit(imagenFondo,(0,0))
	menu_de_pausa.SonidoPausa.play()
	while True:
		reloj.tick(50)
		ventana.blit(menu_de_pausa.menu_pausa,menu_de_pausa.rect)
		for evento in py.event.get():
			if evento.type==QUIT:
				py.quit()
				sys.exit(0)
			if evento.type==KEYDOWN:
				if evento.key==K_DOWN:
					menu_de_pausa.bajar()
					pass
				elif evento.key==K_UP:
					menu_de_pausa.subir()
					pass
				elif evento.key==K_RETURN:
					if menu_de_pausa.resumir == True:
						return 0
					if menu_de_pausa.agente == True:
						if agentei_us.activo == True: #si el agente esta activo, entonces
							agentei_us.activo = False #el agente se desactiva
							agentei_us.desactivar()
							print ("Agente desactivado")
						else: #en caso contrario
							agentei_us.activo = True #el agente se activa mediante la propiedad agenteinteligente.activo
							print ("Agente Activado")
						return 0
					if menu_de_pausa.controles == True:
						pass
					if menu_de_pausa.salir == True:
						pantalla_principal()
					pass
		py.display.update()
	return 0

class sprite_tierragrande(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.imagenTierraGrande = py.image.load("sprites/ambiente/tierragrande.png")
		self.rect = self.imagenTierraGrande.get_rect()
		self.rect.left=posX
		self.rect.top=posY
#clase para pintar la tierra Aire
class sprite_tierraaire(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.imagenTierraAire = py.image.load("sprites/ambiente/tierraaire.png")
		self.rect = self.imagenTierraAire.get_rect()
		self.rect.left=posX
		self.rect.top=posY
#clase Para pintar Agua
class sprite_agua(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.imagenAgua = py.image.load("sprites/ambiente/agua.png")
		self.rect = self.imagenAgua.get_rect()
		self.rect.left=posX
		self.rect.top=posY
#Clase para pintar las nubes
class sprite_nube(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.imagenNube1=py.image.load("sprites/ambiente/nube1.png")
		self.imagenNube2=py.image.load("sprites/ambiente/nube2.png")
		self.imagenNube3=py.image.load("sprites/ambiente/nube3.png")
		self.imagenNube4=py.image.load("sprites/ambiente/nube4.png")
		self.estadonube=0
		self.listanube=[self.imagenNube1,self.imagenNube2,self.imagenNube3,self.imagenNube4]
		self.activaranimacion=False
		
		self.imagenNube=self.listanube[self.estadonube]
		self.SonidoRayo=py.mixer.Sound("Sonidos/rayo.wav")

		self.rect = self.imagenNube.get_rect()
		self.rect.left=posX
		self.rect.top=posY
	def rayo(self,):
		
		if self.estadonube>=3:
			self.estadonube=0
			self.activaranimacion=False
			#self.SonidoRayo.play()
		elif self.estadonube==0:
			self.estadonube+=1
		elif self.estadonube==1:
			self.estadonube+=1
		elif self.estadonube==2:
			self.estadonube+=1
		self.imagenNube=self.listanube[self.estadonube]
class sprite_estrellas(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.estrellas1=py.image.load("sprites/estrellas/estrellas1.png")
		self.estrellas2=py.image.load("sprites/estrellas/estrellas2.png")
		self.estrellas3=py.image.load("sprites/estrellas/estrellas3.png")
		self.imgestrella=0
		self.listaestrellas=[self.estrellas1,self.estrellas2,self.estrellas1,self.estrellas3]
		
		
		self.estrellas=self.listaestrellas[self.imgestrella]
		

		self.rect = self.estrellas.get_rect()
		self.rect.left=posX
		self.rect.top=posY
	def animacion(self):
		if self.imgestrella>=3:
			self.imgestrella=0
		elif self.imgestrella==0:
			self.imgestrella+=1
		elif self.imgestrella==1:
			self.imgestrella+=1
		elif self.imgestrella==2:
			self.imgestrella+=1
		self.estrellas=self.listaestrellas[self.imgestrella]
#Clase Enemigo
class Enemigo(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.infla1=py.image.load("sprites/enemigoInflaGlobo/infla1.png")
		self.infla2=py.image.load("sprites/enemigoInflaGlobo/infla2.png")
		self.infla3=py.image.load("sprites/enemigoInflaGlobo/infla3.png")
		self.infla4=py.image.load("sprites/enemigoInflaGlobo/infla4.png")
		self.infla5=py.image.load("sprites/enemigoInflaGlobo/infla5.png")
		self.infla6=py.image.load("sprites/enemigoInflaGlobo/infla6.png")
		self.infla7=py.image.load("sprites/enemigoInflaGlobo/infla7.png")
		self.infla8=py.image.load("sprites/enemigoInflaGlobo/infla8.png")
		self.infla9=py.image.load("sprites/enemigoInflaGlobo/infla9.png")
		self.infla10=py.image.load("sprites/enemigoInflaGlobo/infla10.png")

		self.vuelo1=py.image.load("sprites/enemigoVolando/vuelo1.png")
		self.vuelo2=py.image.load("sprites/enemigoVolando/vuelo2.png")
		self.vuelo3=py.image.load("sprites/enemigoVolando/vuelo3.png")

		self.caidapara=py.image.load("sprites/paracaidas/paracaidas.png")

		self.caida1=py.image.load("sprites/caidaenemigo/caida1.png")
		self.caida2=py.image.load("sprites/caidaenemigo/caida2.png")
		self.caida3=py.image.load("sprites/caidaenemigo/caida3.png")


		self.listaInflar=[self.infla1,self.infla2,self.infla3,self.infla4,self.infla5,self.infla6,self.infla7,self.infla8,self.infla9,self.infla10]

		self.posEnemigo=0
		self.posVolar=0
		self.posCaer=0

		self.listaVolar=[self.vuelo1,self.vuelo2,self.vuelo3]

		self.listaCaer=[self.caida1,self.caida2,self.caida3]

		self.imagenEnemigo=self.listaInflar[self.posEnemigo]
		self.image=self.imagenEnemigo# Necesaria para las coloiciones

		self.rect=self.imagenEnemigo.get_rect()
		#self.imagenEnemigo=py.transform.scale(self.listaInflar[self.posEnemigo],(50,58))
		self.rect.left=posX
		self.rect.top=posY
		
		self.segundoGolpe=False # esta variable pasara a true cuando se haga la primera colision, y al segundo golpe matara al enemigo
		# OJO esta variable se tendra que cambiar a False cuando se pase ala funcion de InflarGlobo
		self.velocidad=4
		self.DireccionVista=True #Dice hacia donde se orientan las imagenes de los enemigos True para que mire hacia la derecha
		self.direcciony=1
		self.hilodireccion=1 # determinara hacia que direccion se dirigira el enemigo
		self.volando=False # variable para identificar cuando el enemigo este volando _bryant
		self.cayendo=False # variable para identificar cuando el enemigo este cayendo _bryant
		self.inflando=True #variable para identificar cuando el enemigo este inflando los globos_bryant 
		self.muriendo=False #variable para identificar cuando el enemigo este muriando al tener 2 golpes que son reseteados cuando termina de inflar el globo en cualquier ocasion _bryant
		self.golpes=0# contador los golpes que le pegas al enemigo_ bryant
		self.tiempoParaVolar=0# preguntale a marlon
		self.limite=0 # limite sirve para limitar el tiempo de vuelo del enemigo hacia una direccion
		#todas los sonidos relacionados con los enemigos
		self.ParacaidaEnemigo=py.mixer.Sound("Sonidos/ParacaidasEnemigo.wav")
		self.musicaMuere=py.mixer.Sound("Sonidos/MuerteEnemigo.wav")
		self.explosionGlobo=py.mixer.Sound("Sonidos/ExplotarGlobo.wav")
		
		
		'''metodo que cambia las imagenes de la secuencia de inflar el globo  con las respectivas imagenes de la  lista de imgs declaradas al principio dependiendo del numero de veces que es llamada_ bryant'''
	def inflarGlobo(self,PuedaInflar):
		if PuedaInflar: # esta variable no tiene un uso importante se puede quitar pero quita mucho tiempo debido ala indentacion del codigo--esto lo puso marlon
			if self.posEnemigo>=9:
				self.posEnemigo=0#esta variable se utiliza par llevar el conteo de las llamadas a este metodo al igual q en otros es importante dejarlo en 0 cuando terminamos una secuencia_bryant
				self.inflando=False# al llegar a la imagen numero diez de la lista se cambia el estado de inflar a volar_bryant
				self.volando=True
			elif self.posEnemigo==0:
				self.posEnemigo+=1
				self.segundoGolpe=True
			elif self.posEnemigo==1:
				self.posEnemigo+=1
			elif self.posEnemigo==2:
				self.posEnemigo+=1
			elif self.posEnemigo==3:
				self.posEnemigo+=1
			elif self.posEnemigo==4:
				self.posEnemigo+=1
			elif self.posEnemigo==5:
				self.posEnemigo+=1
			elif self.posEnemigo==6:
				self.posEnemigo+=1
			elif self.posEnemigo==7:
				self.posEnemigo+=1
			elif self.posEnemigo==8:
				self.posEnemigo+=1
				self.segundoGolpe=False # se pone falsa esta variable porque el enemigo empieza a volar de nuevo lo que significa que hay que volver a tocarlo

		if self.DireccionVista:
			self.imagenEnemigo=self.listaInflar[self.posEnemigo]
		else:
			self.imagenEnemigo=py.transform.flip(self.listaInflar[self.posEnemigo],True,False)
		
		
	'''cuando tiene dos colisiones los enemigos van muerindo hasta llegar al suelo 
	primer codigo hace la iteracion de la variable para el cambio de imagen  '''
	def EnemigoCaer(self):
		
		if self.posCaer>=2:
			self.posCaer=0
		elif self.posCaer==0:
			self.posCaer+=1
		elif self.posCaer==1:
			self.posCaer+=1
		self.__gravedad() # aqui se utiliza la metodo privado para que descienda el enemigo hasta el suelo

		if self.DireccionVista:
			self.imagenEnemigo=self.listaCaer[self.posCaer] #hace lo mismo se le asigna una imagen al enemigo
		else:
			self.imagenEnemigo=py.transform.flip(self.listaCaer[self.posCaer],True,False) #le da vuelta ala imagen
             #funcion para volar de enemigo que lo hace aleatoriamente por todo el ambiente del juego


	def EnemigoVuela(self):
		'''para mover las imagenes en la lista '''
		if self.posVolar>=2:
			self.posVolar=0
		elif self.posVolar==0:
			self.posVolar+=1
		elif self.posVolar==1:
			self.posVolar+=1
		if self.tiempoParaVolar==self.limite: # cuando esta igualdad se cumple se vuelve a tomar los valores aleatorios 
			self.hilodireccion=random.randint(1,4) # este variable indica hacia que direccion tiene que ir los enemigos puede ser alos lados o hacia arriba pero en diagonal
			self.limite=0 # para que se cumpla otra vez el if se iguala a cero el limite
			self.tiempoParaVolar=random.randint(60,100) # indica cuanto secuencias se movera los enemigos hacia el lado que decice la variable hilo direccion, los valores estan entre 60 y 100 secuencias
			#print self.hilodireccion
		''' las comparaciones del los if determian hacia que direccion se movera los enemigos en diagonal 
		sumandole o restandole alas coordenas dependiendo de la direccion'''

		if self.hilodireccion==1:
			self.rect.top-=2 
			self.rect.left-=5
			self.imagenEnemigo=py.transform.flip(self.listaVolar[self.posVolar],True,False) # esto es para darle vuelta ala imagen
		elif self.hilodireccion==2:
			self.rect.top-=2
			self.rect.left+=5
			self.imagenEnemigo=self.listaVolar[self.posVolar]
		elif self.hilodireccion==3:
			self.rect.top+=2
			self.rect.left-=2
			self.imagenEnemigo=py.transform.flip(self.listaVolar[1],True,False)
		else:
			self.rect.top+=2
			self.rect.left+=2
			self.imagenEnemigo=self.listaVolar[1]
		
		'''este codigo es para los limites con la ventana para que los enemigo se mantengan en el cuadro si los enemigos se pasan muy arriba 
		se modifican las variables para que se puedan tomar otra direccion y otra secuencia de movimientos '''
		if self.rect.top<=0:
			self.tiempoParaVolar=self.limite
			self.rect.top=10
			self.limite-=1
			self.hilodireccion=3 # se pone igual a tres para que tome direccion hacia abajo, aunque no sirve de mucho ya que ala siguiente iteracion se vuelve a elegir otros valores
		elif self.rect.top >= Alto-200:
			self.tiempoParaVolar=self.limite
			self.rect.top=Alto-250
			self.limite-=1
		self.__invertirEje()
		self.limite+=1 # este contador es para que se cumpla la igualdad para volver a elegir otra direccion y tiempo
		''' en esta funcion iguala a cero  las dos variables para que no cambie las imagenes del enemigo y se le asigna 
		la imagen de descenso'''
	def descensoEnemigo(self):
		self.posEnemigo=0
		self.posVolar=0
		self.__gravedad()
		self.imagenEnemigo=self.caidapara
	''' funcion gravuedad es privada porque solo se utiliza en la clase y funciona para que descienda el enemigo
	cuando colisiona con el juegador '''

	def __gravedad(self):
		self.rect.top+=5 #para que descienda los enemigos estre mas rapido mejors
	def __invertirEje(self):# cambia la posicion en el eje x del enemigo  para se mire mejor el efecto de escenario infinito no cambiar estos valores e,e!!!!
		if self.rect.right<=0:
			
			self.rect.right=Ancho+30
		elif self.rect.left>=Ancho:
			
			self.rect.left=-30
		

# lobo selector
class sprite_globoSelector(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.globo1= py.image.load("sprites/menu/globo1.png")
		self.globo2 = py.image.load("sprites/menu/globo2.png")
		self.globo3 = py.image.load("sprites/menu/globo3.png")
		self.globo4 = py.image.load("sprites/menu/globo4.png")
		self.listaGlobos=[self.globo1,self.globo2,self.globo3,self.globo4]
		self.CambioGlobo=0
		self.globoSelector=self.listaGlobos[self.CambioGlobo]
		self.rect = self.globoSelector.get_rect()
		self.rect.left=posX
		self.rect.top=posY
		self.orden=True
		self.seleccion = "A"
		self.direccion=False
		self.Mover=False

	def bajar_seleccion(self):
		if self.rect.top == 360:
			self.seleccion = "B"

			#self.rect.top += 60
		elif self.rect.top == 420:
			self.seleccion = "C"
			#self.rect.top += 60
		elif self.rect.top == 480:
			self.seleccion = "D"

			#self.rect.top += 60
		elif self.rect.top == 540:
			self.seleccion = "A"
			#self.rect.top = 360
	def movi(self):

		if self.Mover:
			
			#if self.rect.top
			if((self.rect.top!=360 and self.rect.top!=420 and self.rect.top!=480 and self.rect.top!=540)or self.Mover):

				if self.direccion: 
					if self.rect.top==360:
						self.rect.top=540
						self.Mover=False
					else:
						self.rect.top -= 5
				else:
					if self.rect.top==540:
						self.rect.top=360
						self.Mover=False
					else:
						self.rect.top += 5
			if(self.rect.top==360 or self.rect.top==420 or self.rect.top==480 or self.rect.top==540):
				self.Mover=False

		

	def subir_seleccion(self):
		if self.rect.top == 360:
			self.seleccion = "D"
			#self.rect.top = 540#480
		elif self.rect.top == 420:
			self.seleccion = "A"
			#self.rect.top = 360
		elif self.rect.top ==480:
			self.seleccion = "B"
			#self.rect.top = 420
		elif self.rect.top == 540:
			self.seleccion = "C"
			#self.rect.top = 480	
	def movimientoGlobo(self):
		if self.orden:
			self.movimientoDerecha()
		else:
			self.movimientoIzquierda()

	def movimientoDerecha(self):
		if self.CambioGlobo==3:
			self.orden=False
			self.movimientoIzquierda()
		else:
			if self.CambioGlobo==0:
				self.CambioGlobo+=1
			elif self.CambioGlobo==1:
				self.CambioGlobo+=1
			elif self.CambioGlobo==2:
				self.CambioGlobo+=1
			self.globoSelector=self.listaGlobos[self.CambioGlobo]
	def movimientoIzquierda(self):
		if self.CambioGlobo==0:
			self.orden=True
			self.movimientoDerecha()
		else:
			if self.CambioGlobo==3:
				self.CambioGlobo-=1
			elif self.CambioGlobo==2:
				self.CambioGlobo-=1
			elif self.CambioGlobo==1:
				self.CambioGlobo-=1
			self.globoSelector=self.listaGlobos[self.CambioGlobo]

#personaje Principal
class vidas(py.sprite.Sprite):#crea el sprite del dibujo de un globito en el menu que representa la vida
	def __init__(self,posx,posy):
		py.sprite.Sprite.__init__(self)
		self.vida=py.image.load("sprites/ambiente/vida.png")
		self.rect=self.vida.get_rect()
		self.rect.top=posy
		self.rect.left=posx

class personaje(py.sprite.Sprite):
	'''Propiedades '''
	def __init__(self):
		py.sprite.Sprite.__init__(self)
		self.para1 = py.image.load("sprites/usparadoder/para1.png")
		self.para2 = py.image.load("sprites/usparadoder/para2.png")
		self.para3 = py.image.load("sprites/usparadoder/para3.png")
		self.para4 = py.image.load("sprites/usparadoder/para4.png")

		self.cor1 = py.image.load("sprites/uscorriendoder/cor1.png")
		self.cor2 = py.image.load("sprites/uscorriendoder/cor2.png")
		self.cor3 = py.image.load("sprites/uscorriendoder/cor3.png")
		self.cor4 = py.image.load("sprites/uscorriendoder/cor4.png")

		self.rayo1 = py.image.load("sprites/caidaUs/caidarayo1.png")
		self.rayo2 = py.image.load("sprites/caidaUs/caidarayo2.png")
		self.rayo3 = py.image.load("sprites/caidaUs/caida3.png")
		self.rayo4 = py.image.load("sprites/caidaUs/caida4.png")

		self.vuelo1 = py.image.load("sprites/usvuelo/vuelo1.png")
		self.vuelo2 = py.image.load("sprites/usvuelo/vuelo2.png")
		self.vuelo3 = py.image.load("sprites/usvuelo/vuelo3.png")

        # jugador corre con un solo globo'''
		self.corre1g = py.image.load("sprites/imagenesUnglobo/corre1.png")
		self.corre2g = py.image.load("sprites/imagenesUnglobo/corre2.png")
		self.corre3g = py.image.load("sprites/imagenesUnglobo/corre3.png")
		self.corre4g = py.image.load("sprites/imagenesUnglobo/corre4.png")
		#'''jugador parado con un globo '''

		self.para1g = py.image.load("sprites/imagenesUnglobo/para1.png")
		self.para2g = py.image.load("sprites/imagenesUnglobo/para2.png")
		self.para3g = py.image.load("sprites/imagenesUnglobo/para2.png")

		#''' jugador volando con un solo globo'''
		self.volar1g = py.image.load("sprites/imagenesUnglobo/volar1.png")
		self.volar2g = py.image.load("sprites/imagenesUnglobo/volar2.png")
		self.volar3g = py.image.load("sprites/imagenesUnglobo/volar1.png")

		self.listaCorrer1Globo=[self.corre1g,self.corre2g,self.corre3g,self.corre4g]

		self.listaParado1Globo=[self.para1g,self.para2g,self.para3g,self.para1g]

		self.listaVolar1Globo=[self.volar1g,self.volar2g,self.volar3g]

		self.listaMuerte=[self.rayo1,self.rayo2,self.rayo3,self.rayo4]

		self.listaParado = [self.para1,self.para2,self.para3,self.para4]

		self.listaCorrer = [self.cor1,self.cor2,self.cor3,self.cor4]

		self.listaVolar = [self.vuelo1,self.vuelo2,self.vuelo3]

		self.SonidoVolar=py.mixer.Sound("Sonidos/volar.wav")
		self.SonidoChoque=py.mixer.Sound("Sonidos/choque.wav")
		self.SonidoSinGlob=py.mixer.Sound("Sonidos/SinGlobo.wav")
		self.SonidoOtroIntento=py.mixer.Sound("Sonidos/IntentardeNuevo.wav")

		self.posImagen = 0
		self.posMuerte=0 #cambio imagenes cuando muere

		self.posImagenStop=0

		self.imagenJugador = self.listaParado[self.posImagen]
		self.image=self.imagenJugador
		self.nivelJuego=1 

		self.rect=self.imagenJugador.get_rect()
		self.rect.left=50
		self.rect.top=460
		
		self.velocidad=6

		self.UnGlobo=False
		self.direccionx=1
		self.direcciony=0
		self.vidas=2# el numero de globos que se van a crear  las vidas son 3 para contar cuando muera usar <0
		
		self.frenar=0# para saber cuando frena el personaje
	
		self.volando=False# para cuando vuela
		self.muerteRayo=False # variable para identificar como morira el jugador, por rayo o por segundo golpe
		self.estaMuerto=False # nos dira si el jugador esta muerto, no importa de que forma

		
		self.descensorec=True#
		self.posimg=0# para controlar el cambio de imagen explicado en el metodo de descenso imagen
		self.cambiodesc=False#esta si no me acuerdo  pero se ocupa mientras no se topecon esta no hay pedo_bryant
		#funciones

	def cambioImagenParado(self,Direccion):
		#cambio de imagenes Cuando el jugador no se mueve
		if self.posImagenStop>2:
			self.posImagenStop=0
		elif self.posImagenStop==0:
			self.posImagenStop+=1
		elif self.posImagenStop==1:
			self.posImagenStop+=1
		elif self.posImagenStop==2:
			self.posImagenStop+=1

		if Direccion:
			if not self.UnGlobo: # solo se cambia de lista se recorre con la misma posicion
				self.imagenJugador=self.listaParado[self.posImagenStop]
			else:
				self.imagenJugador=self.listaParado1Globo[self.posImagenStop]  #OJO falta una imagen tirara error
			
		else:
			if not self.UnGlobo:
				self.imagenJugador=py.transform.flip(self.listaParado[self.posImagenStop],True,False)
			else:
				self.imagenJugador=py.transform.flip(self.listaParado1Globo[self.posImagenStop],True,False)
			
		

	def JugadorCorre(self,estadoAccion,direccion):
		#esta acccion si se aun mantiene precionado la tecla para avanzar de lo contario deja de avanzar
		if estadoAccion:
	
			if self.posImagen>1:
				self.posImagen=0
			elif self.posImagen==0:
				self.posImagen+=1
			elif self.posImagen==1:
				self.posImagen+=1
		
		if direccion:
			if not self.UnGlobo:
				self.imagenJugador=self.listaCorrer[self.posImagen]
				self.rect.left+=self.velocidad
			else:
				self.imagenJugador=self.listaCorrer1Globo[self.posImagen]
				self.rect.left+=self.velocidad
			
			
		else:
			if not self.UnGlobo:
				self.imagenJugador=py.transform.flip(self.listaCorrer[self.posImagen],True,False)
				self.rect.left-=self.velocidad
			else:
				self.imagenJugador=py.transform.flip(self.listaCorrer1Globo[self.posImagen],True,False) 
				self.rect.left-=self.velocidad
	def JugadorFrena(self,direccion):
		#esta acccion si se aun mantiene precionado la tecla para avanzar de lo contario deja de avanzar--carente de sentido e,e
		self.posImagen=3
		if direccion:
			if not self.UnGlobo:
				self.imagenJugador=self.listaCorrer[self.posImagen]
				self.rect.left+=self.velocidad 
			else:
				self.imagenJugador=self.listaCorrer1Globo[self.posImagen]
				self.rect.left+=self.velocidad 
		else:
			if not self.UnGlobo:
				self.imagenJugador=py.transform.flip(self.listaCorrer[self.posImagen],True,False)
				self.rect.left-=self.velocidad
			else:
				self.imagenJugador=py.transform.flip(self.listaCorrer1Globo[self.posImagen],True,False)
				self.rect.left-=self.velocidad
	
	def JugadorVuela(self,direccion,direccion2):
		#esta acccion si se aun mantiene precionado la tecla para avanzar de lo contario deja de avanzar--carente de sentido e,e
		if direccion2!=-2:
			if self.posImagen>1:#esta parte se encarga de cambiar las imagenes de la secuencia de volar_bryant
				self.posImagen=0
			elif self.posImagen==0:
				self.posImagen+=1
			elif self.posImagen==1:
				self.posImagen+=1
			self.rect.top-=self.velocidad
			self.direcciony=1
		else:## hasta donde se nunca va entrar aca o no me acuerdo porq puse esto  _bryant
			self.posImagen=0
			if direccion:
				if not self.UnGlobo:
					self.imagenJugador=self.listaVolar[self.posImagen]
					self.rect.top+=self.velocidad
					self.direcciony=0
				else:
					self.imagenJugador=self.listaVolar1Globo[self.posImagen]

			else:
				if not self.UnGlobo:
					self.imagenJugador=py.transform.flip(self.listaVolar[self.posImagen],True,False)
					self.rect.top+=self.velocidad
					self.direcciony=0 
				else:
					self.imagenJugador=py.transform.flip(self.listaVolar1Globo[self.posImagen],(coor),True,False)
					self.rect.top+=self.velocidad
					self.direcciony=0
   
		if direccion2==1:
			if not self.UnGlobo:
				self.imagenJugador=self.listaVolar[self.posImagen]
				self.rect.top-=self.velocidad
				self.direcciony=1
				self.rect.left+=self.velocidad

			else:
				self.imagenJugador=self.listaVolar1Globo[self.posImagen] 
				self.rect.top-=self.velocidad
				self.direcciony=1
				self.rect.left+=self.velocidad 	
		elif direccion2==0:
			if not self.UnGlobo:
				self.imagenJugador=py.transform.flip(self.listaVolar[self.posImagen],True,False)
				self.rect.top-=self.velocidad
				self.direcciony=1
				self.rect.left-=self.velocidad	
			else:
				self.imagenJugador=py.transform.flip(self.listaVolar1Globo[self.posImagen],True,False)
				self.rect.top-=self.velocidad
				self.direcciony=1
				self.rect.left-=self.velocidad   
		elif direccion2==-1:# entra aca cuando va volando sin direccion _bryant
			if direccion:
				if not self.UnGlobo:
					self.imagenJugador=self.listaVolar[self.posImagen]
					self.rect.top-=self.velocidad
					self.direcciony=1
				else:
					self.imagenJugador=self.listaVolar1Globo[self.posImagen]
					self.rect.top-=self.velocidad
					self.direcciony=1
				    
			else:
				if not self.UnGlobo:
					self.imagenJugador=py.transform.flip(self.listaVolar[self.posImagen],True,False)
					self.rect.top-=self.velocidad
					self.direcciony=1
				else:
					self.imagenJugador=py.transform.flip(self.listaVolar1Globo[self.posImagen],True,False)
					self.rect.top-=self.velocidad
					self.direcciony=1	
	def DescensoVolar(self,Direccion,Activar):# este descenso lo utilizo  para cuando choca o cuando cae con envion cuando va volando para se mire con conva! es diferente al descenso recto cuando no tiene ningun impulso _bryant
		if Activar:
			self.rect.top+=self.velocidad
			self.direcciony=0
			if self.direccionx==1:
				self.rect.left+=self.velocidad
			else:
				self.rect.left-=6


	def DescensoPersonaje(self,Activar):# es practicamente la gravedad # cuando cae recto para abajo_bryant
		
		self.rect.top+=self.velocidad
		self.direcciony=0


	def DescensoImagen(self,Direccion):# lo mando a llamar para q cuando caiga y no se aprete z para volar y se  aprete alguna direccion se cambie la mirada del enemigo ocupo la variable posimg porq se ocupa una direccion diferente a la del moviento por ejemplo cuando cae en una direccion
		if Direccion:
			if not self.UnGlobo:
				self.imagenJugador=self.listaVolar[0]
			else:
				self.imagenJugador=self.listaVolar1Globo[0]

		else:
			if not self.UnGlobo:
				self.imagenJugador=py.transform.flip(self.listaVolar[0],True,False)
			else:
				self.imagenJugador=py.transform.flip(self.listaVolar1Globo[0],True,False)
    #funcion para que muera el juegador, pero morir de tres formas esta funcion controlara dos muerte por dos colisiones o por toque de rayo
	def muerteJugador(self):
		if self.estaMuerto:
			if not self.muerteRayo:
				if self.posMuerte ==2:
					self.imagenJugador=self.listaMuerte[self.posMuerte]
					self.posMuerte=3
				else:
					self.imagenJugador=self.listaMuerte[self.posMuerte]
					self.posMuerte=2
			self.DescensoPersonaje(True)		
	def choquePersonaje(self):# se manda a llmar cuando choca con una tierra o un enemigo

		if self.direccionx==1:
			self.direccionx=0
			self.rect.left-=20
			if self.direcciony==1:
				self.rect.top+=20

			else:
				self.rect.top-=20	
		
		else:
			self.direccionx=1
			self.rect.left+=40
			if self.direcciony==1:
				self.rect.top+=20

			else:
				self.rect.top-=20

	def invertirEje(self):##lo mismo que en el de el enemigo  ---revisar_bryant
		if self.rect.right<=0:
			
			self.rect.right=Ancho+30
		elif self.rect.left>=Ancho:
			
			self.rect.left=-30
#Funciones
#Funcion para el menu
def pantalla_principal():
	py.init()	
	reloj=py.time.Clock()
	py.time.set_timer(py.USEREVENT+6,200)
	SonidoMenu=py.mixer.Sound("Sonidos/menu.wav")
	ventana=py.display.set_mode((Ancho,Alto))
	py.display.set_caption("BALLON FIGHT")
	imagenFondo=py.image.load("sprites/menu/fondodemenu.jpg")
	globo_selector = sprite_globoSelector(380,360)
	SonidoMenu.play()
	while True:
		reloj.tick(50)
		
		#print tiempo
		ventana.blit(imagenFondo,(0,0))
		ventana.blit(globo_selector.globoSelector,globo_selector.rect)
		for evento in py.event.get():
			if evento.type==QUIT:
				py.quit()
				sys.exit(0)
			if evento.type==KEYDOWN:
				if evento.key==K_DOWN:
					globo_selector.bajar_seleccion()
					globo_selector.direccion=False
					globo_selector.Mover=True;
					pass
				elif evento.key==K_UP:
					globo_selector.subir_seleccion()
					globo_selector.direccion=True
					globo_selector.Mover=True;
					pass
				elif evento.key==K_RETURN:
					SonidoMenu.stop()
					if globo_selector.seleccion=="A":
						Ambiente()
					elif globo_selector.seleccion=="B":
						pantalla_controles()
					elif globo_selector.seleccion=="C":
						pantalla_creditos()
					pass
			if evento.type==py.USEREVENT+6:
					globo_selector.movimientoGlobo()
					pass
			
		
		#globo_selector.movimientoGlobo()
		globo_selector.movi()
		py.display.update()

	return 0
def pantalla_controles():
	py.init()	
	reloj=py.time.Clock()
	#py.time.set_timer(py.USEREVENT+4,200)
	#ventana=py.display.set_mode((Ancho,Alto))

	py.display.set_caption("BALLON FIGHT")
	imagenFondo=py.image.load("sprites/menu/Controles.png")

	#globo_selector = sprite_globoSelector(380,360)
	ventana.fill((0,0,0))
	ventana.blit(imagenFondo,(0,0))
	while True:
		reloj.tick(50)
		
		#print tiempo
		
		#ventana.blit(globo_selector.globoSelector,globo_selector.rect)
		for evento in py.event.get():
			if evento.type==QUIT:
				py.quit()
				sys.exit(0)
			if evento.type==KEYDOWN:
				if evento.key==K_DOWN:
					#globo_selector.bajar_seleccion()
					pass
				elif evento.key==K_UP:
					#globo_selector.subir_seleccion()
					pass
				elif evento.key==K_RETURN:
					pantalla_principal()
					pass
			elif evento.type==py.USEREVENT+4:
					#globo_selector.movimientoGlobo()
					pass
		
		#globo_selector.movimientoGlobo()
		py.display.update()

	return 0
def pantalla_gameover():
	py.init()	
	reloj=py.time.Clock()
	#py.time.set_timer(py.USEREVENT+4,200)
	#ventana=py.display.set_mode((Ancho,Alto))

	py.display.set_caption("BALLON FIGHT")
	imagenGame=py.image.load("sprites/menu/gameover.png")
	SonidoOver=py.mixer.Sound("Sonidos/gameover.wav")
	#globo_selector = sprite_globoSelector(380,360)
	#ventana.fill((0,0,0))
	SonidoOver.play()
	imagenFondo=py.image.load("sprites/pausa/pausaCongelar.jpg")
	imagenFondo.convert_alpha()
	ventana.blit(imagenGame,(0,0))
	while True:
		reloj.tick(50)
		
		#print tiempo
		
		#ventana.blit(globo_selector.globoSelector,globo_selector.rect)
		for evento in py.event.get():
			if evento.type==QUIT:
				py.quit()
				sys.exit(0)
			if evento.type==KEYDOWN:
				if evento.key==K_DOWN:
					#globo_selector.bajar_seleccion()
					pass
				elif evento.key==K_UP:
					#globo_selector.subir_seleccion()
					pass
				elif evento.key==K_RETURN:
					SonidoOver.stop()
					pantalla_principal()
					pass
			
		
		#globo_selector.movimientoGlobo()
		py.display.update()

	return 0
def pantalla_creditos():
	py.init()	
	reloj=py.time.Clock()
	py.time.set_timer(py.USEREVENT+1,50)
	#ventana=py.display.set_mode((Ancho,Alto))
	Creditos=sprite_credito(0,0)
	py.display.set_caption("BALLON FIGHT")
	#imagenFondo=py.image.load("sprites/menu/creditos.png")

	#globo_selector = sprite_globoSelector(380,360)
	#ventana.fill((0,0,0))
	#ventana.blit(imagenFondo,(0,0))
	while True:
		reloj.tick(50)
		ventana.fill((0,0,0))
		ventana.blit(Creditos.imagenCredito,Creditos.rect)
		##ventana.blit(imagenFondo,(0,0))
		
		#print tiempo
		
		#ventana.blit(globo_selector.globoSelector,globo_selector.rect)
		for evento in py.event.get():
			if evento.type==QUIT:
				py.quit()
				sys.exit(0)
			if evento.type==KEYDOWN:
				if evento.key==K_DOWN:
					#globo_selector.bajar_seleccion()
					pass
				elif evento.key==K_UP:
					#globo_selector.subir_seleccion()
					pass
				elif evento.key==K_RETURN:
					pantalla_principal()
					pass
			if evento.type==py.USEREVENT+1:
				Creditos.mover()
		
		#globo_selector.movimientoGlobo()
		py.display.update()

	return 0
class sprite_credito(py.sprite.Sprite):
	'''Propiedades'''
	def __init__(self,posX,posY):
		py.sprite.Sprite.__init__(self)
		self.imagenCredito = py.image.load("sprites/menu/creditos.png")
		self.rect = self.imagenCredito.get_rect()
		self.rect.left=posX
		self.rect.top=posY
	def mover(self):
		self.rect.top=self.rect.top-2

#funcion para el juego en ejecucion
def Ambiente():
	py.init()
	reloj=py.time.Clock()
	#reloj=py.time.Clock()
	#ventana=py.display.set_mode((Ancho,Alto))
	py.display.set_caption("BALLON FIGHT")
	imagenFondo=py.image.load("sprites/fondoJuego.jpg")
	us = personaje()
	agua = sprite_agua(-20,620)
	tierraGrandeIzquierda = sprite_tierragrande(-90,600)
	tierraGrandeDerecha = sprite_tierragrande(850,600)
	#tierraaire = sprite_tierraaire(435,320)
	CargarTierrasAire(us.nivelJuego)
	nube = sprite_nube(570,50)
	estrellas=sprite_estrellas(0,0)

	#enemigo=Enemigo(310,250)
	'''creando fuente para cuando colisione algun enemigo que aparesca en la imagen '''
	fuentePuntos=py.font.Font(None,30)
	TextoPuntos=fuentePuntos.render('500',0,(200,0,0))
	CargarEnemigo(us.nivelJuego)# esta funcion carga los enemigos en una lista global, se elimino la instancia de un objeto enemigo
	LLenarVidas()
	MusicaIntro=py.mixer.Sound("Sonidos/primero.wav")#se crea la variable de la cancion del principio
	#SonidoRayo=py.mixer.Sound("Sonidos/rayo.wav")
	Reprodujo=False# para controlar q solo se reproduzca una vez
	Reprodujo2=False
	
	corriendo=False
	
	''' creando un envento para que se pueda inflar el globo el enemigo- este evento dice que se cambiaran la imagenes cada 230 milisegundos'''
	py.time.set_timer(py.USEREVENT+1,230)
	py.time.set_timer(py.USEREVENT+2,10000)
	py.time.set_timer(py.USEREVENT+3,30000)
	py.time.set_timer(py.USEREVENT+4,150)
	# evento que sirve para agragar un nuevo enemigo al ambiente siempre y cuando haya algun elemento en la lista
	py.time.set_timer(py.USEREVENT+5,1000)
	velocidad=8
	Puntaje=0
	NivelDos=False

	while us.vidas>=0:
		if Reprodujo==False:# para controlar que  se reprodujo una vez
			MusicaIntro.play()
			Reprodujo=True
		
		#print mitiempo
		tecla=py.key.get_pressed() # este nos ayudar para mover el jugador manteniendo presiona la tecla 

		reloj.tick(50)
		

		for evento in py.event.get():
			if evento.type==py.USEREVENT+1:	#enviar el ambiente a determinado tiempo.
				if agentei_us.activo == True: #si el agente esta activado
					enviar_ambiente(us) #llamado a la funcion enviar ambiente, para escribir el estado del ambiente en el archivo .json
					#imprimir_ambiente()
					siguiente_movimiento(agentei_us) #llamado a la funcion siguiente movimiento.

			if evento.type==QUIT:
				py.quit()
				sys.exit(0)

			if evento.type == py.KEYDOWN:
				if evento.key == py.K_SPACE:
					pausa()
					pass
				if evento.key == py.K_UP:
					pass
				if evento.key == py.K_DOWN:
					pass
				if evento.key == py.K_RIGHT:# and volando and descensorec:
					#--------------------------------------------------------------------------------------------------------------
					#--------------------------------------------------------------------------------------------------------------
					if not us.estaMuerto:
						if us.cambiodesc==False:
							us.direccionx=1
						us.posimg=1
					pass
					
				if evento.key == py.K_LEFT:
					#--------------------------------------------------------------------------------------------------------------
					#--------------------------------------------------------------------------------------------------------------
					if not us.estaMuerto:
						if us.cambiodesc==False:
							us.direccionx=0
						us.posimg=0
					pass
				if evento.key == py.K_z:
					#--------------------------------------------------------------------------------------------------------------
					#--------------------------------------------------------------------------------------------------------------
					if not us.estaMuerto:
						us.SonidoVolar.play()
					
			if evento.type == py.KEYUP:
				if evento.key == py.K_UP:
					pass
				if evento.key == py.K_DOWN:
					pass
				if evento.key == py.K_RIGHT:
					#--------------------------------------------------------------------------------------------------------------
					#--------------------------------------------------------------------------------------------------------------
					if not us.estaMuerto:
						corriendo=False
					
				if evento.key == py.K_LEFT:
					#--------------------------------------------------------------------------------------------------------------
					#--------------------------------------------------------------------------------------------------------------
					if not us.estaMuerto:
						corriendo=False
				if evento.key == py.K_z:
					#--------------------------------------------------------------------------------------------------------------
					#--------------------------------------------------------------------------------------------------------------
					if not us.estaMuerto:
						us.volando=False
			if evento.type==py.USEREVENT+4:
				if nube.activaranimacion:
					nube.rayo()
			if evento.type==py.USEREVENT+5:
				estrellas.animacion()
			if evento.type==py.USEREVENT+2:
				''' este evento se ejecuta cada 40 segundo y solo se agragara un maximo de 6 enemigos 
				pero cuando se vallan eliminando se va a poder agregar mas enemigos '''
				if us.nivelJuego==1:
					numeroE=7
				else:
					numeroE=12
				#if len(listaenemigo)<numeroE:
					#ene=Enemigo(460,345)
					#listaenemigo.append(ene)
			if evento.type==py.USEREVENT+1:
				if len(listaenemigo)>0:
					for enemigo in listaenemigo:
						if enemigo.inflando:
							enemigo.inflarGlobo(True)
			if evento.type==py.USEREVENT+3:

				nube.activaranimacion=True
				nube.SonidoRayo.play()
					
					 # este evento sirve para que las imagenes se cambien mas lento y se pueda aprecias mejor la accion
					
					
					          
		if tecla[py.K_z]==True and tecla[py.K_LEFT]==True  or (agentei_us.volar_izq == True and agentei_us.activo == True):#cuando vuela y se dirige a la izq mandomos el segundo valor de 1 para identificar como sera la caida en caso de dejar de apretar la tecla de volar
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			
			if not us.estaMuerto:
				if us.rect.top >= 0:
					us.descensorec=False
					us.volando=True
					us.cambiodesc=False
					us.direccionx=0
					us.JugadorVuela(False,0)
				else:
					us.SonidoChoque.play()

		elif tecla[py.K_z]==True and tecla[py.K_RIGHT]==True  or (agentei_us.volar_der == True and agentei_us.activo == True):# cuando vuela y se dirige a la derecha mandomos el segundo valor de 1 para identificar como sera la caida en caso de dejar de apretar la tecla de volar
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				if us.rect.top >= 0:				
					us.descensorec=False
					us.volando=True
					us.cambiodesc=False
					us.direccionx=1
					us.JugadorVuela(True,1)
				else:
					us.SonidoChoque.play()

		elif tecla[py.K_z]==True  or (agentei_us.arriba == True and agentei_us.activo == True):##cuando apreta z sin tocar una direccion vuela en linea recta para arriba se mantiene recto con el valor de -1
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				if us.rect.top >= 0:				
					us.volando=True
					us.cambiodesc=False
					if us.direccionx==1:
						us.JugadorVuela(True,-1)
					else:
						us.JugadorVuela(False,-1)
				else:
					us.SonidoChoque.play()

		elif tecla[py.K_RIGHT] and us.volando==False:
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				if us.cambiodesc==False:
					us.frenar=1
					corriendo=True
					us.JugadorCorre(True,True)
				us.direccionx=1
		elif tecla[py.K_LEFT] and us.volando==False:
			#--------------------------------------------------------------------------------------------------------------
		    #--------------------------------------------------------------------------------------------------------------

			if not us.estaMuerto:
				if us.cambiodesc==False:
					us.frenar=1
					corriendo=True
					us.JugadorCorre(True,False)
				us.direccionx=0

		elif tecla[py.K_RIGHT]==False and tecla[py.K_LEFT] ==False and us.volando==False or (agentei_us.abajo == True and agentei_us.activo) == True:
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				if us.frenar==1:
					if us.direccionx==1:
						us.JugadorFrena(True)
					else:
						us.JugadorFrena(False)
					us.frenar=0
				corriendo=False
		#pinta todas los sprites
		ventana.fill((0,0,0))
		ventana.blit(estrellas.estrellas,estrellas.rect)
		ventana.blit(nube.imagenNube,nube.rect)
		ventana.blit(us.imagenJugador,us.rect)

		ventana.blit(agua.imagenAgua,agua.rect)
		ventana.blit(tierraGrandeIzquierda.imagenTierraGrande,tierraGrandeIzquierda.rect)
		ventana.blit(tierraGrandeDerecha.imagenTierraGrande,tierraGrandeDerecha.rect)
		#ventana.blit(tierraaire.imagenTierraAire,tierraaire.rect)
		#if len(listaTierraAire)>0:
		for t in listaTierraAire:
			if us.nivelJuego==1:
				us.velocidad=4
			ventana.blit(t.imagenTierraAire,t.rect)

		
		if not corriendo and not us.volando:
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				if us.direccionx==1:
					us.cambioImagenParado(True)
				else:
					us.cambioImagenParado(False)
		''' imprimir todos los enemigos con un ciclo for el primer if no dira si hay algun enemigo en la lista para poder imprimir
		,despues se crea el ciclo for para que se impriman en la pantalla  '''
		if len(listaenemigo)>0:
			for enemigo in listaenemigo:
				ventana.blit(enemigo.imagenEnemigo,enemigo.rect)
		EliminarEnemigo() 
		'''va ir eliminando los enemigos de la lista que estan muertos'''
		#ventana.blit(enemigo.imagenEnemigo,enemigo.rect)
		Score=FuenteScore.render(str(Puntaje).zfill(6),1,py.Color("ghostwhite"))
		#Score=FuenteScore.render("YO - "+str(Puntaje).zfill(6),1,py.Color("brown1"))
		ventana.blit(Yo,(50,30))
		Espaciado=FuenteScore.size("YO ")[0]
		ventana.blit(Score,(50+Espaciado,30))
		Espaciado=FuenteScore.size("TOP ")[0]
		ventana.blit(Top,(1000,30))
		ventana.blit(TopScore,(1000+Espaciado,30))

		for vi in listavidas:
			ventana.blit(vi.vida,vi.rect)
		#if len(listaenemigo)>0:

		'''Movimientos que que puede realizar los enemigos que hasta ahorita puede realizar cuatro acciones
		inflar globos, bolar,descender y morir
		'''	
		if len(listaenemigo)>0:
			for enemigo in listaenemigo:
				
				if enemigo.volando:# aqui es activara el metodo para que vuele los enemigos
					enemigo.EnemigoVuela()
				elif enemigo.muriendo:
					enemigo.EnemigoCaer()
				elif enemigo.cayendo:
					enemigo.descensoEnemigo()

		
		
		'''coliciones del jugador con todos los objetos del ambiente '''
		var=False
		for tierraaire in listaTierraAire:
			if us.rect.colliderect(tierraaire.rect) and us.rect.bottom<=tierraaire.rect.top+velocidad:
				#us.DescensoPersonaje(False)
				#--------------------------------------------------------------------------------------------------------------
				#--------------------------------------------------------------------------------------------------------------
				if not us.estaMuerto:
					us.volando=False
					us.descensorec=True
					us.cambiodesc=False
					var=True
			elif us.rect.colliderect(tierraaire.rect) and us.rect.right>=tierraaire.rect.left and us.rect.midleft>=tierraaire.rect.top:
				#--------------------------------------------------------------------------------------------------------------
				#--------------------------------------------------------------------------------------------------------------
				if not us.estaMuerto:
					us.choquePersonaje()
					us.SonidoChoque.play()
					var=True
			elif us.rect.colliderect(tierraaire.rect) and us.rect.left<=tierraaire.rect.right and us.rect.midright>=tierraaire.rect.top:
				#--------------------------------------------------------------------------------------------------------------
				#--------------------------------------------------------------------------------------------------------------
				if not us.estaMuerto:
					us.choquePersonaje()
					us.SonidoChoque.play()
					var=True
			elif us.rect.colliderect(tierraaire.rect) and us.rect.top<=tierraaire.rect.bottom and us.rect.bottom>tierraaire.rect.bottom:
				#--------------------------------------------------------------------------------------------------------------
				#--------------------------------------------------------------------------------------------------------------
				if not us.estaMuerto:
					us.choquePersonaje()
					us.SonidoChoque.play()
					var=True
		

		if us.rect.colliderect(tierraGrandeDerecha.rect) and us.rect.bottom<=tierraGrandeDerecha.rect.top+velocidad:
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				us.volando=False
				us.descensorec=True
				us.cambiodesc=False
		elif us.rect.colliderect(tierraGrandeIzquierda.rect) and us.rect.bottom<=tierraGrandeIzquierda.rect.top+velocidad:
			#us.DescensoPersonaje(False)
			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				us.volando=False
				us.descensorec=True
				us.cambiodesc=False
		elif var:
			pass
		else:

			#--------------------------------------------------------------------------------------------------------------
			#--------------------------------------------------------------------------------------------------------------
			if not us.estaMuerto:
				us.cambiodesc=True
				if us.volando==True:
					if us.direccionx==1:
						if us.descensorec:
							us.DescensoPersonaje(True)
						else:
							us.DescensoVolar(True,True)
					else:
						if us.descensorec:
							us.DescensoPersonaje(True)
						else:
							us.DescensoVolar(False,True)
					if us.posimg==1:
						us.DescensoImagen(True)
					else:
						us.DescensoImagen(False)
				else:
					if us.direccionx==1:
						us.DescensoPersonaje(True)
						posant=us.direccionx
					else:
						us.DescensoPersonaje(False)
						posant=us.direccionx
					if us.posimg==1:
						us.DescensoImagen(True)
					else:
						us.DescensoImagen(False)
			

		'''Colisones con los enemigos esto cuando las colisiones muere los enemigos '''
					
		for enemigo in listaenemigo: # el for hace recorrer todos los enemide la lista
			if py.sprite.collide_mask(us,enemigo) and not enemigo.muriendo:# collide_mask es como si solo funcionara cuando se toca arriba del enemigo 
				us.choquePersonaje()
				enemigo.explosionGlobo.play()
				if enemigo.inflando and enemigo.segundoGolpe: # ojo se puede hacer una funcion para no estar copiando el mismo codigo
					enemigo.muriendo=False
					enemigo.cayendo=True
					enemigo.volando=False
					enemigo.inflando=False
					Puntaje+=750
					#ventana.blit(TextoPuntos,(enemigo.rect.left-5,enemigo.rect.top-50))
				if us.rect.top<enemigo.rect.top-10:
					if enemigo.segundoGolpe:
						enemigo.muriendo=True
						enemigo.cayendo=False
						enemigo.volando=False
						enemigo.limite=0
						enemigo.ParacaidaEnemigo.stop()
						enemigo.musicaMuere.play()
						
					else:

						enemigo.ParacaidaEnemigo.play()
						enemigo.cayendo=True
						enemigo.volando=False
						enemigo.muriendo=False
						enemigo.segundoGolpe=True
						Puntaje+=500
						#ventana.blit(TextoPuntos,(enemigo.rect.left-5,enemigo.rect.top-50))
				else:
					if us.UnGlobo:
						us.estaMuerto=True
						us.muerteRayo=False
						enemigo.ParacaidaEnemigo.stop()
						enemigo.musicaMuere.stop()
						us.SonidoSinGlob.play()

					else:
						us.UnGlobo=True
						us.choquePersonaje()

			

			if (enemigo.rect.colliderect(tierraGrandeIzquierda.rect)and enemigo.cayendo)or enemigo.inflando:
				enemigo.cayendo=False
				enemigo.inflando=True
				enemigo.ParacaidaEnemigo.stop()		   
			elif (enemigo.rect.colliderect(tierraGrandeDerecha.rect)and enemigo.cayendo) or enemigo.inflando:
				enemigo.cayendo=False
				enemigo.inflando=True
				enemigo.ParacaidaEnemigo.stop()
			
			for t in listaTierraAire:
				if (enemigo.rect.colliderect(t.rect)and enemigo.cayendo)or enemigo.inflando:
					enemigo.cayendo=False
					enemigo.inflando=True
					enemigo.ParacaidaEnemigo.stop()

			#elif (enemigo.rect.colliderect(tierraaire.rect)and enemigo.cayendo)or enemigo.inflando:
			#	enemigo.cayendo=False
			#	enemigo.inflando=True
			#	enemigo.ParacaidaEnemigo.stop()
			#else:
			#	pass
		#colision del jugador con el enemigo pero para cuando el pierde el juegador que seria cuando este colisione al mismo nivel o 
		#abajo de los enemigos hacer una funcion de choue para el enemigo tambien

		'''if len(listaenemigo)>0: #que no se ejecute cuando esta vacia la lista
			for enemigo in listaenemigo:
				if enemigo.rect.colliderect(us.rect):
					us.choquePersonaje()
					if enemigo.rect.top<us.rect.top:
						if us.UnGlobo:
							us.DescensoPersonaje(True)
						else:
							us.UnGlobo=True'''
		#este if sirve para reestablecer todos los parametros desactivados 
		if len(listaenemigo)==0:
			if not NivelDos:
				us.nivelJuego=2
				CargarTierrasAire(us.nivelJuego)
				CargarEnemigo(us.nivelJuego)
				us.rect.left=60
				us.rect.top=450
				NivelDos=True
			else:
				pantalla_principal()

		if us.rect.top>=Alto-50:
			us.estaMuerto=False
			us.muerteRayo=False
			us.SonidoSinGlob.stop()

			us.vidas-=1
			us.UnGlobo=False
			us.rect.left=60
			us.rect.top=450
			if len(listavidas)>0:
				listavidas.pop()
				us.SonidoOtroIntento.play()
				us.nivelJuego=1
		us.muerteJugador()
		us.invertirEje()
		#enemigo.gravedad() #es probable que no se utilize una gravedad en el enemigo
		
		py.display.update()
	pantalla_gameover()
	return 0
def CargarEnemigo(nivel):
	''' esta funcion crea varios enemigos y los carga a una lista global de enemigos
	este codigo no es el mejor se puede mejora pero es preferible cambarlo hasta que se 
	le agreguen niveles al juego falta hacer los niveles del juego para agregar mas enemigos 
	por ahora solo seran tres enemigos '''
	del listaenemigo[:]
	posicionx=430
	posiciony=345
	ene=Enemigo(posicionx,posiciony)
	ene2=Enemigo(posicionx+150,posiciony)
	ene3=Enemigo(posicionx+250,posiciony)
	ene4=Enemigo(120,160)
	ene5=Enemigo(720,160)
	ene6=Enemigo(260,160)
	ene7=Enemigo(390,160)
	ene8=Enemigo(820,160)
	ene9=Enemigo(920,160)

	#for i in range(2):
	if nivel==1:
		listaenemigo.append(ene)
		listaenemigo.append(ene2)
		listaenemigo.append(ene3)
	elif nivel==2:
		listaenemigo.append(ene)
		listaenemigo.append(ene2)
		listaenemigo.append(ene3)
		listaenemigo.append(ene4)
		listaenemigo.append(ene5)
		listaenemigo.append(ene6)
		listaenemigo.append(ene7)
		listaenemigo.append(ene8)
		listaenemigo.append(ene9)

def EliminarEnemigo():
	'''funcion para eliminar enemigos que han sido matado  por el jugador 
	como el top sobrepasa mas del suelo se da por hecho que fue tocado dos veces 
	esta funcion se hace para que se puedan agregar mas enemigos y darle mas dificultad al juego'''
	if len(listaenemigo)>0:
		for ene in listaenemigo:
			if ene.rect.top>Alto-50:
				ene.ParacaidaEnemigo.stop()
				listaenemigo.remove(ene)
def LLenarVidas():
	vida =vidas(220,70)
	vida1=vidas(190,70)
	listavidas.append(vida)
	listavidas.append(vida1)
def CargarTierrasAire(nivel):
	del listaTierraAire[:]
	tierraaire = sprite_tierraaire(435,400)
	tierraaire2 =sprite_tierraaire(100,200)
	#tierraaire2.imagenTierraAire=py.transform.scale(tierraaire2.imagenTierraAire,(150,30)) 
	tierraaire3 =sprite_tierraaire(700,200) 
	#tierraaire3.imagenTierraAire=py.transform.scale(tierraaire3.imagenTierraAire,(150,30)) 
	if nivel==1:
		listaTierraAire.append(tierraaire)
	elif nivel==2:
		listaTierraAire.append(tierraaire)
		listaTierraAire.append(tierraaire2)
		listaTierraAire.append(tierraaire3)

#Clase Pescado
class Pez(py.sprite.Sprite):
	def __init__(self,posX,posY):
		py.sprite.sprite.__init__(self)
		self.pez=py.image.load("sprites/pescado/pez1.png")
		self.pez2=py.image.load("sprites/pescado/pez2.png")
		self.pez3=py.image.load("sprites/pescado/pez3.png")
		self.pez4=py.image.load("sprites/pescado/pez4.png")
		self.listaPez=[self.Pez,self.pez2,self.pez3,self.pez4]

		self.posPez=0
		self.imagenPez=self.listaPez[self.posPez]
		self.rect=self.imagenPez.get_rect()
		self.rect.left=posX
		self.rect.top=posY
		self.puedeComer=False
	def puedeComer(self):
		if self.posPez>=3:
			self.posPez=0
		elif self.posPez==0:
			self.posp+=1
		elif self.posPez==1:
			self.posPez+=1
		elif self.posPez==2:
			self.posPez+=1

		self.imagenPez=self.listaPez[self.posPez]



pantalla_principal()