######################################################################
##            INSTITUTO TECNOLÓGICO DE COSTA RICA                   ##
##                                                                  ##
##  Proyecto  :   Algoritmos Genéticos - Similud entre dos imágenes ##
##                                                                  ##
##  Profesor  :   Jose Carranza                                     ##
##                                                                  ##
##  Estudiantes :   Sebastían Salas García (2015183511)             ##
##                  Nicolas Feoli Chacón   (2016081332)             ##
##                                                                  ##
######################################################################

##Librerias
import numpy as np
from PIL import Image
from matplotlib import pyplot as plt
from math import *
import logging
import random
import time
import cv2

######################METODOS DEL GENERALES#############################
"""
Método que retorna una lista con los datos de todos
los pixeles de una imagen
Formato : (R,G,B,"")
"""
def getPixelsInArray(FileName):
    imagen = Image.open(FileName)
    listPixels = list(imagen.getdata())
    return listPixels

"""
Método que crea una imagen con las diferentes generaciones de mutaciones
"""
def createCollage(width, height, listofimages, cantImage):
        if cantImage % 2 == 0:
                cols = cantImage // 2
        else:
                cols = cantImage + 1
        rows = 2
        thumbnail_width = width//cols
        thumbnail_height = height//rows
        size = thumbnail_width, thumbnail_height
        new_im = Image.new('RGB', (width, height))
        ims = [] 
        for p in listofimages:
                im = Image.open(p)
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

  
"""
Método que crea imagenes con solamente ruido de 300 x 300
pixeles
Parametros especificos: fmt - String
                        datosImagen - Tupla(x,y,array,modo)
"""
def producirImagen(fmt,datosImagen, nombreImagen = "imagen"):
        lista = datosImagen[2]
        if datosImagen[3] == 0:     ##Aleatorio
                im = Image.new("RGBA",(datosImagen[0],datosImagen[1]),"black")
                a = np.random.rand(datosImagen[0], datosImagen[1],2)
                a *= 255
                im= Image.fromarray(a.astype("uint8")).convert("RGBA")
                
        elif datosImagen[3] == 1:   ##Color
                im = Image.new("RGB",(datosImagen[0],datosImagen[1]),"black")
                pixels = im.load()
                acum = 0
                for i in range(datosImagen[0]):
                        for y in range(datosImagen[1]):
                                pixels[y,i] = lista[acum]
                                acum += 1
        else:                       ##Blanco y Negro
                im = Image.new("L",(datosImagen[0],datosImagen[1]),"black")
                pixels = im.load()
                acum = 0
                for i in range(datosImagen[0]):
                        for y in range(datosImagen[1]):
                                pixels[y,i] = lista[acum]
                                acum += 1
        im.save(nombreImagen+'.'+fmt)

"""
    Metodo que muestra un histograma del comportamiento del blanco y negro
    de varias Imagen.
    Parametro : lista de las generaciones pixeles de la imagen.
"""
def graficoWB(listasGeneraciones):
        for n in range (len(listasGeneraciones)):
                plt.plot(listasGeneraciones[n],label = "Generacion"+ " %d" %(n+1))
        plt.xlabel("Pixeles")
        plt.ylabel("Color(L)")
        plt.title(" Comportamiento de Colores en una Imagen")
        plt.legend()
        plt.show()

"""
    Metodo que muestra un histograma del comportamiento de los colores
    de una Imagen.
    Parametro : ruta de la imagen con su extension respectiva.
"""
def graficoRGB(nombreImagen):
        img = Image.open(nombreImagen)
        imgArr = np.asarray(img)
        plt.subplot(221), plt.imshow(img)

        color = ('r','g','b')
        for i,col in enumerate(color):
                histr = cv2.calcHist([imgArr],[i],None,[256],[0,256])
                plt.subplot(222), plt.plot(histr,color = col)
                plt.xlim([0,256])
            
        plt.xlim([0,256])
        plt.show()
    

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
def algoritmoGenetico(poblacion, metodo=1):
	
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
	selected =  puntuados[(len(puntuados)-pressure):] 

	#Se mezcla el material genetico para crear nuevos individuos
	for i in range(len(poblacion)-pressure):
		punto = random.randint(1,largo-1) 
		padre = random.sample(selected, 2) 
		
		poblacion[i][:punto] = padre[0][:punto]
		poblacion[i][punto:] = padre[1][punto:]
	return poblacion

"""
Metodo que cambia de manera random el valor de un pixel para crear un nuevo individuo
"""
def mutar(poblacion):
    for i in range(len(poblacion)-pressure):
            if random.random() <= posibilidadMutacion: #Cada individuo de la poblacion menos los padres
                    #print("\tMutacion ocurrida")
                    punto = random.randint(0,largo-1) 
                    nuevo_valor = random.randint(1,255) 
                    while nuevo_valor == poblacion[i][punto]:
                            nuevo_valor = random.randint(1,255)

                    #Se aplica la mutacion
                    poblacion[i][punto] = nuevo_valor

    return poblacion

#########################METODOS/FUNCIONES DE ADAPTABILIDAD#######################
"""
Método y algoritmo de similitud entre dos vectores de pixeles de una imagen
"""
def distanciaEuclediana(x):
    print(type(x))
    print(x)
    time.sleep(10)
    potencias = [pow(a-b,2) for a, b in zip(x, listaGenesMeta)]
    return sqrt(sum(potencias))

"""
Método de y algoritmo de similitud propio
"""
def calcularAdaptabilidad(individual):
    fitness = 0
    for i in range(len(individual)):
            if individual[i] == listaGenesMeta[i]: # MEJORAR ESTO
                    fitness += 1
    return fitness

"""
Algoritmo randomizador de Kaczmarz, Error cuadrático medio (MSE)
"""
def mse(imageA):
    #entre mas bajo sea el MSE, mas similares son las imagenes
    errorMSE = np.sum((np.array(imageA) - np.array(listaGenesMeta)) ** 2)
    errorMSE /= float(tamanoPoblacion)
    return errorMSE

"""
Método que retorna lo datos de una imagen planos para ser procesados
"""
def formatoLista2Array(original, ladoO=32):
    resultado = [[None for i in range(ladoO)] for i in range(ladoO)]
    for i in range(ladoO):
            for k in range(ladoO):
                    resultado[i][k] = original[ladoO*i+k]
    return resultado

"""
Método que crea imagenes a color o en blanco y negro los
pixeles
"""
def producirImagenes(fmt, original, nombreImagen="imagen", color=False):
    if color:
            final = []
            temp = []
            for i in range(1, largo+1):
                    temp.append(original[i-1])
                    if i % 3 == 0:
                            final.append(temp)
                            temp = []
            final = np.array(formatoLista2Array(final,lado))
    else:
            final = np.array(formatoLista2Array(original,lado))
    imagen = Image.fromarray(final.astype("uint8"))
    nombreImagen += "." + fmt
    imagen.save(nombreImagen)

"""
Método que registra datos en un .log 
"""
def loggear(mensaje):
	logging.info(mensaje)
	
    
#####################################MAIN##################################################
##Declaracion de Datos
rutaImagenMeta      = "meta.jpg"
extension           = ".jpg"    ##Modo en que se guarda la imagen
listaGenesAleatorio = []        #Pixeles de imagen aleatoria
listaGenesMeta      = []        ##Pixeles de imagen meta
imagenesFinales     = []        ##Variable de tipo lista que guarda las dif. generacione																					#
color               = True																								#
lado                = 32																									#
tamanoPoblacion     = 10        #La cantidad de individuos que habra en la poblacion									
pressure            = 2         #Cuantos individuos se seleccionan para reproduccion. Necesariamente mayor que 2				
posibilidadMutacion = 0.2       #La probabilidad de que un individuo muestra 																					
numero_generaciones = 10000

if color:																									#
        largo = (lado*lado*3)   #La longitud del material genetico de cada individuos 							
        imagen2D = np.array(Image.open(rutaImagenMeta).convert("RGB"))
        imagenModelo = []																						#
        for i in imagen2D:																						#
                for j in i:																							#
                        for l in j:																						#
                                imagenModelo.append(l)																		#
else:																										#
        largo = lado * lado       #La longitud del material genetico de cada individuo 									
        imagen2D = np.array(Image.open(rutaImagenMeta).convert("L"))											
        imagenModelo = []																						#
        for i in imagen2D:																						#
                for j in i:																							#
                        imagenModelo.append(j)																			#
listaGenesMeta = list(imagenModelo)     #[1 for i in range (largo)] #Objetivo a alcanzar								

############################INICIALIZACION DEL LOGGER#######################################																					#
logging.basicConfig(filename='evoluciones.log',level=logging.DEBUG,format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
loggear('Ejecutando una evolucion.')																		

for handler in logging.root.handlers[:]:																	
    logging.root.removeHandler(handler)																		

logging.basicConfig(filename='evoluciones.log',level=logging.DEBUG,format='%(message)s')					

loggear('\tNumero de individuos = '+ str(tamanoPoblacion))												
loggear("\tImagen meta: " + rutaImagenMeta)															
loggear("\tCantidad de evoluciones: " + str(numero_generaciones))										

for handler in logging.root.handlers[:]:																	
    logging.root.removeHandler(handler)																		

logging.basicConfig(filename='evoluciones.log',level=logging.DEBUG,format='%(levelname)s:%(message)s')		
loggear("Empezando la simulacion \n\n\n\n")																																		#
loggear("Modelo: %s\n"%(listaGenesMeta))																		
########################################################################################
poblacion = [[random.randint(0, 255) for i in range(largo)] for i in range(tamanoPoblacion)]
loggear("Poblacion Inicial:\n%s\n"%(poblacion[random.randint(0, tamanoPoblacion-1)]))           #Se muestra un especimen aleatorio de la poblacion inicial
loggear("Fitness poblacion inicial: %s\n"%[distanciaEuclediana(poblacion[d]) for d in range(tamanoPoblacion)])

aux =  numero_generaciones // 10
for i in range(numero_generaciones + 1):
        poblacion = algoritmoGenetico(poblacion,2)
        poblacion = mutar(poblacion)
        
        if(aux == i):
                imagenesFinales.append("generacion"+str(i)+extension)
                loggear("Euclediana: %s\n"%[distanciaEuclediana(poblacion[d]) for d in range(tamanoPoblacion)])
                [producirImagenes("jpg", poblacion[m], "generacion"+str(i), color) for m,n in enumerate(poblacion)]
                aux += numero_generaciones // 10
                
createCollage(1500, 1500, imagenesFinales, 10)
loggear("\nPoblacion Final:\n%s"%(poblacion))#Se muestra la poblacion evolucionada

loggear("Fitness poblacion final: %s"%[distanciaEuclediana(poblacion[d]) for d in range(tamanoPoblacion)])
loggear("Simulacion terminada\n\n"+"#"*50 )

###################################PRUEBAS##############################################

#Modo  : Blanco y negro
#Imagen : Luigi 32 x 32
#Cantidad Generaciones : 20000
#Metodo : MSE
##listasGeneraciones = []
##listasGeneraciones.append(getPixelsInArray(imagenesFinales[9]))
##listasGeneraciones.append(getPixelsInArray("LuigiBW5.jpg"))
##graficoWB(listasGeneraciones)

#Modo  : Color
#Imagen : Luigi 32 x 32
#Cantidad Generaciones : 20000
#Metodo : MSE
##graficoRGB("generacion2000.jpg")
##graficoRGB("generacion10000.jpg")
##graficoRGB("generacion20000.jpg")

#Modo  : Color
#Imagen : Luigi 32 x 32
#Cantidad Generaciones : 10000
#Metodo : MSE
##graficoRGB("generacion1000.jpg")
##graficoRGB("generacion5000.jpg")
##graficoRGB("generacion10000.jpg")

#Modo  : Color
#Imagen : Zelda 50 x 50
#Cantidad Generaciones : 20000
#Metodo : MSE
##graficoRGB("generacion2000.jpg")
##graficoRGB("generacion10000.jpg")
##graficoRGB("generacion20000.jpg")

#Modo  : Color
#Imagen : Zelda 50 x 50
#Cantidad Generaciones : 10000
#Metodo : MSE
##graficoRGB("generacion1000.jpg")
##graficoRGB("generacion5000.jpg")
##graficoRGB("generacion10000.jpg")
##graficoRGB("zelda.jpg")

#Modo  : Color Imagen :
#Zelda 50 x 50
#Cantidad Generaciones : 20000
#Metodo : MSE
##listasGeneraciones = []
##listasGeneraciones.append(getPixelsInArray("generacion20000.jpg"))
##listasGeneraciones.append(getPixelsInArray("zeldaWB.jpg"))
##graficoWB(listasGeneraciones)

#Modo  : Blanco y negro
#Imagen : estrella 32 x 32
#Cantidad Generaciones : 20000
#Metodo : Euclideana
##listasGeneraciones = []
##listasGeneraciones.append(getPixelsInArray("generacion2000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion10000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion20000.jpg"))
##listasGeneraciones.append(getPixelsInArray("estrella.jpg"))
##graficoWB(listasGeneraciones)

#Modo  : Blanco y negro
#Imagen : estrella 32 x 32
#Cantidad Generaciones : 10000
#Metodo : Euclideana
##listasGeneraciones = []
##listasGeneraciones.append(getPixelsInArray("generacion1000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion5000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion10000.jpg"))
##listasGeneraciones.append(getPixelsInArray("estrella.jpg"))
##graficoWB(listasGeneraciones)

#Modo  : Color
#Imagen : estrella 32 x 32
#Cantidad Generaciones : 20000
#Metodo : Euclideana
##graficoRGB("generacion2000.jpg")
##graficoRGB("generacion10000.jpg")
##graficoRGB("generacion20000.jpg")
##graficoRGB("estrella.jpg")

#Modo  : Color
#Imagen : print 32 x 32
#Cantidad Generaciones : 20000
#Metodo : Propia
##graficoRGB("generacion2000.jpg")
##graficoRGB("generacion10000.jpg")
##graficoRGB("generacion20000.jpg")
##graficoRGB("print.jpg")

#Modo  : Blanco y negro
#Imagen : print 32 x 32
#Cantidad Generaciones : 20000
#Metodo : Propia
##listasGeneraciones = []
##listasGeneraciones.append(getPixelsInArray("generacion2000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion10000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion20000.jpg"))
##listasGeneraciones.append(getPixelsInArray("printWB.jpg"))
##graficoWB(listasGeneraciones)

#Modo  : Blanco y negro
#Imagen : print 32 x 32
#Cantidad Generaciones : 10000
#Metodo : Propia
##listasGeneraciones = []
##listasGeneraciones.append(getPixelsInArray("generacion1000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion5000.jpg"))
##listasGeneraciones.append(getPixelsInArray("generacion10000.jpg"))
##listasGeneraciones.append(getPixelsInArray("printWB.jpg"))
##graficoWB(listasGeneraciones)

