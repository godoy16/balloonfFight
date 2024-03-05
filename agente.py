# -*- encoding: utf-8 -*-

import json as js 
import math

enemigos = []	#Lista de las posiciones de cada enemigo
objetosAbiente = []	#lista de objetos que se encuentrar en el ambiente 
lista_movimientos = [] #lista de objetos movimiento
pos_player_X = 0	#posicion en x del player
pos_player_Y = 0	#posicion en y del player

class movimientos():	#clase para los movimientos que se pueden realizar en el juego
	def __init__(self, m,p):	#inicializar
		self.movimiento = m 	#nombre del movimiento  
		self.peso = p 			#peso para el movimiento

	def __cmp__(self, other):	#ordenar por peso
		if self.peso < other.peso:	#si el peso del objeto es menor que el peso del siguiente objeto
			rst = -1	#se retorna -1 por medio de la variable rst
		elif self.peso > other.peso:	#si el peso del objeto es mayo que el peso del siguiente objeto
			rst = 1		#se retorna 1 por medio de la variable rst
		else:		#sin son iguales 
			rst = 0	#retorna 0 por medio de la variable rst
		return rst	#retorno

	def __repr__(self): 	#imprime las propiedades del objeto
		return "(" + self.movimiento + ","+ str(self.peso) + ")" #se imprime en formato (nombre,peso)

class pos_enemigo():
	def __init__(self, x,y):	#inicializar
		self.x = x 	#posicion x del enemigo
		self.y = y 	#posicion y del enemigo
		self.d = 0 	#distancia del enemigo hacia el player

	def __cmp__(self, other):	#ordenar por peso
		if self.d < other.d:	#si el peso del objeto es menor que el peso del siguiente objeto
			rst = -1	#se retorna -1 por medio de la variable rst
		elif self.d > other.d:	#si el peso del objeto es mayo que el peso del siguiente objeto
			rst = 1		#se retorna 1 por medio de la variable rst
		else:		#sin son iguales 
			rst = 0	#retorna 0 por medio de la variable rst
		return rst	#retorno

	def __repr__(self): 	#imprime las propiedades del objeto
		return "(" + str(self.x) + ","+ str(self.y) + "), d=" + str(self.d)  #se imprime en formato (nombre,peso)

class AgenteInteligente:
	'''Clase AgenteInteligente, serautilizada para retornar el proximo movimiento cuando el agente este activado'''
	
	#Propiedades del Agente
		#Racional: Capaz de reaccionar de una manera racional o inteligente.
		#Autónomo Capaz de actuar de forma independiente, no sujeto a un control externo.
		#Persistente Debe ejecutarse continuamente.

		#No cumple: (Comunicativo, Cooperativo, Movil, Adaptativo)

	#Propiedades Agente - Ambiente
		#observabilidad: parcialmente observable, el agente solo tiene la posibilidad de saber que posiciones tiene el enemigo y no de los objetos
		#cambio: estático, ya que cuando el agente toma una decisión el ambiente no cambia.
		#Determinista: Estocastico hay algo de aleatoriedad al cambio del medioambiente provocado por los enemigos
		#episódico: el agente percibir el entorno y tomar una acción
		#Contínuo: el número de estados posibles es grande.
		#Multi-Agente: un único agente

	activo = False	#Almacenara True si el agente esta activo, False en caso contrario
	arriba = False	#Almacenara True si el proximo movimiento para el player es arriba, False en caso contrario
	abajo = False 	#Almacenara True si el proximo movimiento para el player es abajo, False en caso contrario
	derecha = False	#Almacenara True si el proximo movimiento para el player es derecha, False en caso contrario
	izquierda = False #Almacenara True si el proximo movimiento para el player es izquierda, False en caso contrario
	volar_der = False #Almacenara True si el proximo movimiento para el player es volar hacia la derecha, False en caso contrario
	volar_izq = False #Almacenara True si el proximo movimiento para el player es volar hacia la izquierda, False en caso contrario
	correr_der = False #Almacenara True si el proximo movimiento para el player es correr hacia la derecha, False en caso contrario
	correr_izq = False #Almacenara True si el proximo movimiento para el player es correr hacia la izquierda, False en caso contrario
	
	lista_movimientos_agente = []

	m_arriba = movimientos("Arriba",0) #instancia del objeto movimiento que tiene como nombre: Arriba y peso: 0
	m_abajo = movimientos("Abajo",0) 
	m_derecha = movimientos("Derecha",0)
	m_izquierda = movimientos("Izquierda",0)
	m_volar_der = movimientos("volar_der",0)
	m_volar_izq = movimientos("volar_izq",0)
	m_correr_der = movimientos("correr_der",0)
	m_correr_izq = movimientos("correr_izq",0)

	lista_movimientos_agente.append(m_arriba) #se agrega el objeto movimiento a la lista de movimientos que puede realizar el agente
	lista_movimientos_agente.append(m_abajo)
	lista_movimientos_agente.append(m_derecha)
	lista_movimientos_agente.append(m_izquierda)
	lista_movimientos_agente.append(m_volar_der)
	lista_movimientos_agente.append(m_volar_izq)
	lista_movimientos_agente.append(m_correr_der)
	lista_movimientos_agente.append(m_correr_izq)

	def desactivar(self):
		arriba = False
		abajo = False
		derecha = False
		izquierda = False
		volar_der = False
		volar_izq = False
		correr_der = False
		correr_izq = False 

def inicializar_pesos_movimientos(agente):
	for m in agente.lista_movimientos_agente:
		m.peso = 0
	agente.desactivar()

def Leer_ambiente(solicitar): 
	'''Funcion que lee los datos contenidos en un archivo js
	   Solicitar argumento que indicara que datos se necesitan del ambiente'''

	with open('medio.json') as arhivoAmbiente: #se abre el archivo medio.json, dicho archivo contiene las posiciones de los enemigos, players y objetos en el ambiente del juego
		datosAmbiente=js.load(arhivoAmbiente) #se crean los datosAmbiente objeto dentro del cual se pueden obtener datos
	
	if(solicitar == "todos"):
		print(datosAmbiente) #se imprimen los datos del ambiente
	if(solicitar == "Player"):
		print(datosAmbiente['Player']) #se imprimen los datos del player
	if(solicitar == "Enemigos"):
		print(datosAmbiente['Enemigos']) #se imprimen los datos del player
	if(solicitar == "DetalleObtejo"):
		#print datosAmbiente['Enemigos'][0]['1']['posX']
		print ("player")
		print ("Posicion en X: " + str(datosAmbiente['Player'][0]['posX']))
		print ("Posicion en X: " + str(datosAmbiente['Player'][0]['posY']))
		print ("\n")

		for fila in datosAmbiente['Enemigos'][0]:
			print ("Enemigo:" + fila)
			print ("Posicion en X: " + str(datosAmbiente['Enemigos'][0][fila]['posX']))
			print ("Posicion en Y: " + str(datosAmbiente['Enemigos'][0][fila]['posY']))
			print ("\n")
			#print datosAmbiente['Enemigos'][0][fila]['posX']

def imprimir_ambiente():
	print ("\nTodos los Datos del Ambiente\n")
	Leer_ambiente("DetalleObtejo")		#se hace el llamado a la funcion leer_ambiente pasandole como argumento "todos"

def formula_distancia(x1,y1,x2,y2): #formula que calcula la distancia entre dos puntos
	d = math.sqrt(((x2-x1) ** 2)+((y2-y1) ** 2))
	return d

def indice(lista_m,mov): #funcion que retorna el indice de la posicino de un movimiento pasandole como paramatro el nombre del movimiento
	contador = 0
	for m in lista_m:
		if m.movimiento == mov:
			break
		else:
			contador +=1	
	return contador

def siguiente_movimiento(agente): #funcion que hara el siguiente movimiento del player
	movimiento_ganador = "" #movimiento que obtuvo mayor numero de activaciones
	rho = 0 #Factor de importancia
	w_atacar = 0 #peso del valor para un movimiento de ataque
	w_defender = 0 #peso del valor para un movimiento de defensa

	del enemigos[:] #se eliminan todos los elementos de la lista de enemigos

	with open('medio.json') as arhivoAmbiente: #se abre el archivo medio.json, dicho archivo contiene las posiciones de los enemigos, players y objetos en el ambiente del juego
		datosAmbiente=js.load(arhivoAmbiente) #se crean los datosAmbiente objeto dentro del cual se pueden obtener datos
	#se extraen la posicion del player del archivo medio.json
	pos_player_X = datosAmbiente['Player'][0]['posX']
	pos_player_Y = datosAmbiente['Player'][0]['posY']

	#se crea una lista con las posiciones del enemigo
	for fila in datosAmbiente['Enemigos'][0]:
		enemigo_x = pos_enemigo(datosAmbiente['Enemigos'][0][fila]['posX'],datosAmbiente['Enemigos'][0][fila]['posY']) #instacia de pos_enemigo
		enemigos.append(enemigo_x)

	#para cada enemigo de la lista se calcula la distancia del enemigo al player y se almacena en la propiedad: d, del enemigo.
	for e in enemigos:
		e.d = formula_distancia(e.x,e.y,pos_player_X,pos_player_Y)

	#se ordena la lista del enemigo, posicionando primero los enemigos que tengan una menor distancia al player
	enemigos.sort()

	#rho sera igual al tamaño de la lista de enemigos, servira para establecer la prioridad de los movimientos conforme a los enemigos, el que este mas cerca tiene mayor prioridad
	rho = len(enemigos)
	#inicializar la lista de movimientos
	inicializar_pesos_movimientos(agente)
	#Recorrer la lista de enemigos 
	for e in enemigos:
		w_atacar = 0
		w_defender = 0

		if pos_player_Y < e.y:		#Determinar si el player esta sobre el enemigo
			w_atacar = 2 				#atacar tiene un mayor peso que defender
			w_defender = 0

			if (e.y > pos_player_Y) and (abs(e.x - pos_player_X) <= 100): #Determina si el player esta a una posicion adecuada para caer sobre el enemigo
				agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"Abajo")].peso = 300 #se incrementa el peso del movimiento bajar

			if (e.y - pos_player_Y) < 200 and (abs(e.x - pos_player_X) <= 200 ): #Determina si el player esta a una posicion adecuada para caer sobre el enemigo
				agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"Abajo")].peso = 200 #se incrementa el peso del movimiento bajar
		else:
			w_atacar = 0			#si el player es abajo del enemigo
			w_defender = 3				#defender tiene un mayor peso que atacar

		if pos_player_X > e.x:        #Determinar si el enemigo esta a la izquierda
			agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"volar_izq")].peso += rho + w_atacar		#se pondera el peso de volar a la izquierda con atacar, ya que si el enemigo esta a la izquierda, el player tiene que moverse a la izquierda para seguirlo
			agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"volar_der")].peso += rho + w_defender	#se pondera el peso de volar a la derecha con defender, ya que si el enemigo esta a la izquierda, el player tiene que moverse a la derecha para esquivarlo
		else:
			agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"volar_izq")].peso += rho + w_defender	#se pondera el peso de volar a la izquierda con defender, ya que si el enemigo esta a la derecha, el player tiene que moverse a la izquierda para esquivarlo
			agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"volar_der")].peso += rho + w_atacar		#se pondera el peso de volar a la derecha con atacar, ya que si el enemigo esta a la derecha, el player tiene que moverse a la derecha para seguirlo

		if ((670-pos_player_Y)<70):
			agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"Arriba")].peso = 300 #el player volara
	if len(enemigos) == 0: #si no hay enemigos
		agente.lista_movimientos_agente[indice(agente.lista_movimientos_agente,"Arriba")].peso = 199 #el player volara

	#odenar la lista de movimientos en el agente, de tal manera que el movimiento con mayor peso quede primero
	agente.lista_movimientos_agente.sort(reverse=True)

	print (agente.lista_movimientos_agente[0])
	
	#se almacena en movimiento_ganador el movimiento con mayor numero de activaciones
	movimiento_ganador = agente.lista_movimientos_agente[0].movimiento
	
	agente.arriba = False
	agente.abajo = False
	agente.derecha = False
	agente.izquierda = False
	agente.volar_der = False
	agente.volar_izq = False
	agente.correr_der = False
	agente.correr_izq = False 
	
	if movimiento_ganador == "Arriba":
		agente.arriba = True
	if movimiento_ganador == "Abajo":
		agente.abajo = True
	if movimiento_ganador == "Derecha":
		agente.derecha = True
	if movimiento_ganador == "Izquierda":
		agente.izquierda = True
	if movimiento_ganador == "volar_der":
		agente.volar_der = True
	if movimiento_ganador == "volar_izq":
		agente.volar_izq = True
	if movimiento_ganador == "correr_der":
		agente.correr_der = True
	if movimiento_ganador == "correr_izq":
		agente.correr_izq = True

	#print "Arriba: " + str(agente.arriba)
	#print "Abajo: " + str(agente.abajo)
	#print "Derecha: " + str(agente.derecha)
	#print "Izquierda: " + str(agente.izquierda)
	#print "volar derecha: " + str(agente.volar_der)
	#print "volar izquierda: " + str(agente.volar_izq)
	#print "correr derecha: " + str(agente.correr_der)
	#print "correr izquierda" + str(agente.correr_izq)