#!/usr/bin/python

import random
import numpy
from PIL import Image
from math import *
import logging




def algoritmoGenetico(poblacion, metodo=1):
	"""
		Recibe una poblacion(arreglo bidimensional) y un metodo. El metodo 
			tiene que ser un entero entre 1 y 3, en donde cada uno significa: 
				1. Distancia Euclediana
				2. Mean squared Error
				3. Funcion de adaptabilidad propia
		Puntua todos los elementos de la poblacion (poblacion) y se queda con los mejores
		guardandolos dentro de 'selected'.
		Despues mezcla el material genetico de los elegidos para crear nuevos individuos y
		llenar la poblacion (guardando tambien una copia de los individuos seleccionados sin
		modificar).

		Por ultimo muta a los individuos.

	"""
	if(metodo == 1):
		#Distancia euclediana en gris, por lo que se necesitan los que tienen el resultado mas bajo. 
		puntuados = [(distanciaEuclediana(i), i) for i in poblacion] 
		puntuados = [i[1] for i in sorted(puntuados,reverse=True)] 
	elif(metodo == 2):
		#Mean squared Error, por lo que se necesitan los que tienen el resultado mas bajo. 
		puntuados = [(mse(i), i) for i in poblacion] 
		puntuados = [i[1] for i in sorted(puntuados,reverse=True)] 
	else:
		puntuados = [(calcularAdaptabilidad(i), i) for i in poblacion] 
		puntuados = [i[1] for i in sorted(puntuados)]
	poblacion = puntuados


	selected =  puntuados[(len(puntuados)-pressure):] #Esta linea selecciona los 'n' individuos del final, donde n viene dado por 'pressure'


	#Se mezcla el material genetico para crear nuevos individuos
	for i in range(len(poblacion)-pressure):
		punto = random.randint(1,largo-1) #Se elige un punto en el cromosoma para hacer el intercambio
		padre = random.sample(selected, 2) #Se eligen dos padres
		
		poblacion[i][:punto] = padre[0][:punto] #Se mezcla el material genetico de los padres en cada nuevo individuo
		poblacion[i][punto:] = padre[1][punto:]

	return poblacion #El array poblacion tiene ahora una nueva poblacion de individuos, que se devuelven

def mutar(poblacion):
	for i in range(len(poblacion)-pressure):
		if random.random() <= posibilidadMutacion: #Cada individuo de la poblacion (menos los padres)
			#print("\tMutacion ocurrida")
			punto = random.randint(0,largo-1) #Se elige un punto al azar
			nuevo_valor = random.randint(1,255) #y un nuevo valor para este punto
			while nuevo_valor == poblacion[i][punto]: #Si el bvalor de la mutacion es el mismo del punto busca otro
				nuevo_valor = random.randint(1,255)

			#Se aplica la mutacion
			poblacion[i][punto] = nuevo_valor

	return poblacion

#############################################El club de los incomprendidos 
#		FUNCIONES DE ADAPTABILIDAD          #
#############################################

def distanciaEuclediana(x):
	potencias = [pow(a-b,2) for a, b in zip(x, modelo)]
	return sqrt(sum(potencias))

def calcularAdaptabilidad(individual):
	fitness = 0
	for i in range(len(individual)):
		if individual[i] == modelo[i]: # MEJORAR ESTO
			fitness += 1
	return fitness

def mse(imageA):
	#entre mas bajo sea el MSE, mas similares son las imagenes
	err = numpy.sum((numpy.array(imageA) - numpy.array(modelo)) ** 2)
	err /= float(tamanoPoblacion)
	return err

def formatoLista2Array(original, ladoO=32):
	resultado = [[None for i in range(ladoO)] for i in range(ladoO)]
	for i in range(ladoO):
		for k in range(ladoO):
			resultado[i][k] = original[ladoO*i+k]
	return resultado


def producirImagenes(fmt, original, nombreImagen="imagen", color=False):
	if color:
		final = []
		temp = []
		for i in range(1, largo+1):
			temp.append(original[i-1])
			if i % 3 == 0:
				final.append(temp)
				temp = []
		final = numpy.array(formatoLista2Array(final))
	else:
		final = numpy.array(formatoLista2Array(original))
	imagen = Image.fromarray(final.astype("uint8"))
	nombreImagen += "." + fmt
	imagen.save(nombreImagen)



def createCollage(width, height, listofimages, cantImage):
	"""
	Datos a llamar
	im= Image.open('ejemplo2.jpg')
	listofimages = [] 
	for i in range(10):
		listofimages.append("ejemplo2.jpg")
	"""
	if cantImage % 2 == 0:
		cols = cantImage // 2
	else:
		cols = cantImage + 1
	rows = 2
	thumbnail_width = width//cols
	thumbnail_height = height//rows
	size = thumbnail_width, thumbnail_height
	new_im = Image.new('RGB', (width, height))
	ims = []#listofimages #[] 
	#for p in listofimages:
	#	im = Image.open(p)
	#	ims.append(im)
	for p in listofimages:
		a = numpy.array(formatoLista2Array(p))
		im = Image.fromarray(a.astype("uint8"))
		ims.append(im)
	i = 0
	x = 0
	y = 0
	for col in range(cols):
		for row in range(rows):
			new_im.paste(ims[i].resize(size), (x,y))
			i += 1
			y += thumbnail_height
		x += thumbnail_width
		y = 0
	new_im.save("Collage.jpg")
	new_im.show()

def loggear(mensaje):
	logging.info(mensaje)


#############################################################################################################
#############################################################################################################
#############################################################################################################
###												MAIN:													  ###
#############################################################################################################
#############################################################################################################
#############################################################################################################

#############################################################################################################
# Declaracion de datos 																						#
																											#
rutaImagenMeta = "meta.png"																					#
color = True
#color = False																								#
lado = 32																									#
tamanoPoblacion = 10 #La cantidad de individuos que habra en la poblacion									#
pressure = 2 #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2				#
posibilidadMutacion = 0.2 #La probabilidad de que un individuo muestra 										#
																											
																											
#Generaciones de la Poblacion 																				#
numero_generaciones = int(raw_input("Numero de generaciones:\t"))											#

if color:																									#
	largo = (lado*lado*3) #La longitud del material genetico de cada individuos 							#
	imagen2D = numpy.array(Image.open(rutaImagenMeta))#.convert("RGB"))		 								#
	#print(imagen2D)
	imagenModelo = []																						#
	for i in imagen2D:																						#
		for j in i:																							#
			for l in j:																						#
				imagenModelo.append(l)																		#
else:																										#
	largo = lado*lado #La longitud del material genetico de cada individuo 									#
	imagen2D = numpy.array(Image.open(rutaImagenMeta).convert("L"))											#
	imagenModelo = []																						#
	for i in imagen2D:																						#
		for j in i:																							#
			imagenModelo.append(j)																			#
modelo = list(imagenModelo) #[1 for i in range (largo)] #Objetivo a alcanzar								#

#############################################################################################################



#############################################################################################################
#INICIALIZACION DEL LOGGER:																					#
logging.basicConfig(filename='evoluciones.log',level=logging.DEBUG, format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
loggear('Ejecutando una evolucion.')																		#

for handler in logging.root.handlers[:]:																	#
    logging.root.removeHandler(handler)																		#

logging.basicConfig(filename='evoluciones.log',level=logging.DEBUG, format='%(message)s')					#

loggear('\tNumero de individuos = '+ str(tamanoPoblacion))												#
loggear("\tImagen meta: " + rutaImagenMeta)															#
loggear("\tCantidad de evoluciones: " + str(numero_generaciones))										#

for handler in logging.root.handlers[:]:																	#
    logging.root.removeHandler(handler)																		#

logging.basicConfig(filename='evoluciones.log',level=logging.DEBUG, format='%(levelname)s:%(message)s')		#

loggear("Empezando la simulacion \n\n\n\n")															#

print("Modelo: %s\n"%(modelo), len(modelo))																				#
loggear("Modelo: %s\n"%(modelo))																		#
#############################################################################################################


poblacion = [[random.randint(0, 255) for i in range(largo)] for i in range(tamanoPoblacion)]
#Producir un ejemplar Aleatorio de la poblacion inicial
#producirImagenes("png", poblacion[random.randint(0, tamanoPoblacion-1)], "original", color) 
producirImagenes("png", imagenModelo, "finalPruebaColor", color)


print("Poblacion Inicial:\n%s"%(poblacion[random.randint(0, tamanoPoblacion-1)])) #Se muestra un especimen aleatorio de la poblacion inicial
loggear("Poblacion Inicial:\n%s\n"%(poblacion[random.randint(0, tamanoPoblacion-1)]))
print("Fitness poblacion inicial: %s"%[mse(poblacion[d]) for d in range(tamanoPoblacion)])
loggear("Fitness poblacion inicial: %s\n"%[mse(poblacion[d]) for d in range(tamanoPoblacion)])


for i in range(numero_generaciones):
	print("Generacion %d"%i)
	#logging.info("Generacion %d"%i)
	#print(poblacion)
	poblacion = algoritmoGenetico(poblacion,2)
	poblacion = mutar(poblacion)
	#producirImagenes("png", poblacion[0], "gen"+str(i))
	if(i % 1000 == 0):
		print("MSE poblacion: %s"%[mse(poblacion[d]) for d in range(tamanoPoblacion)])
		loggear("MSE poblacion: %s\n"%[mse(poblacion[d]) for d in range(tamanoPoblacion)])
		[producirImagenes("png", poblacion[m], "generacion"+str(i), color) for m,n in enumerate(poblacion)]


print("\nPoblacion Final:\n%s"%(poblacion)) #Se muestra la poblacion evolucionada
loggear("\nPoblacion Final:\n%s"%(poblacion))

print("Fitness poblacion final: %s"%[mse(poblacion[d]) for d in range(tamanoPoblacion)])
loggear("Fitness poblacion final: %s"%[mse(poblacion[d]) for d in range(tamanoPoblacion)])

print("\n\n")
print(poblacion[3] == poblacion[2])

[producirImagenes("png", poblacion[i], "final"+str(i), color) for i,j in enumerate(poblacion)]
loggear("Simulacion terminada\n\n"+"#"*50 )

#for i in range(poblacion):
#	poblacion[i] = 

#createCollage(1500, 1500, list(poblacion), 10)

#print(numpy.array(Image.open("pruebaColor.jpg").convert("L")))
