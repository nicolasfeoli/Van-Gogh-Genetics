#!/usr/bin/python

import random
import numpy
from PIL import Image
from math import *
import logging

def mse(imagen):
    #entre mas bajo sea el MSE, mas similares son las imagenes
    err = numpy.sum((numpy.array(imagen) - numpy.array(modelo)) ** 2)
    err /= float(largo)
    return err

def mse2(imagen):
    sumaArrays = int(0)
    for i in range(len(imagen)):
        sumaArrays += (imagen[i] + modelo[i])**2
    err = sumaArrays/float(largo)
    return err

rutaImagenMeta = "meta.png"

imagenTmp = Image.open(rutaImagenMeta)
imagen2D = numpy.array(imagenTmp.convert("L"))                                          #
lado, ancho = imagenTmp.size
largo = lado*lado #La longitud del material genetico de cada individuo                                  #

imagenModelo = []                                                                                       #
for i in imagen2D:                                                                                      #
    for j in i:                                                                                         #
        imagenModelo.append(j)                                                                          #
modelo = list(imagenModelo) #[1 for i in range (largo)] #Objetivo a alcanzar



poblacion = Image.open("final18.png")
imagen2D = numpy.array(poblacion.convert("L"))

imagenModelo = []                                                                                       #
for i in imagen2D:                                                                                      #
    for j in i:                                                                                         #
        imagenModelo.append(j)                                                                          #
poblacion = list(imagenModelo) #[1 for i in range (largo)] #Objetivo a alcanzar



print("Fitness: %s"%mse(poblacion))
print("Fitness2: %s"%mse2(poblacion))
