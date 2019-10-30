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
import numpy
from PIL import Image
import time

"""
Método que muestra una imagen abriendo el mostrador de imagines.
"""
def mostrarImagen(FileName):
    imagenMeta = Image.open(FileName)
    imagenMeta.show() ##Mostrar la imagen

"""
Método que retorna un pixel especifico de una foto
"""
def getPixel(FileName,posx,posy):
    imagen = Image.open(FileName)
    coordenada = x , y = posx, posy
    return imagen.getpixel(coordenada)

"""
Método que retorna una lista con los datos de todos
los pixeles de una imagen
Formato : (R,G,B,"")
"""
def getPixelsInArray(FileName):
    imagen = Image.open(FileName)
    listPixels = list(imagen.getdata())
    imagen.tobytes()
    return listPixels
  
"""
Método que crea imagenes con solamente ruido de 300 x 300
pixeles
Parametros especificos: n   - int
                        fmt - String
"""
def producirImagenAleatoria(n, fmt,tamx,tamy, nombreImagen = "imagen"):
    #produce n imagenes del formato fmt
    #n es un int y fmt es un string
    tamanoX = tamx
    tamanoY = tamy
    a = numpy.random.rand(tamanoX, tamanoY,2)
    a *= 255
    imagen= Image.fromarray(a.astype("uint8")).convert("RGBA")
    imagen.save(nombreImagen+'.'+fmt)
    

"""
Método que crea una imagen con las diferentes generaciones de mutaciones
"""
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

"""
def algoritmoGenetico(genesMeta, genesAle):
    pass


"""
Método principal del programa
"""
def main():
    nombreImagenAle     = "aleatoria"
    nombreImagenMeta    = "meta"
    extension           = ".jpg"    ##Modo en que se guarda la imagen
    listaGenesAleatorio = []        #Pixeles de imagen aleatoria
    listaGenesMeta      = []        ##Pixeles de imagen meta
    imagenesFinales     = []        ##Variable de tipo lista que guarda las dif. generaciones
    ##Generar la población random de una imagen
    producirImagenAleatoria(1, extension, 32,32, nombreImagenAle)
    ##Recuperar datos imagen meta y aleatoria
    listaGenesMeta = getPixelsInArray(nombreImagenMeta + extension)
    listaGenesAleatoria = getPixelsInArray(nombreImagenAle + extension)
    algoritmoGenetico(listaGenesMeta,listaGenesAleatoria)
##    for x in range(len(listaGenesAleatoria)): OJOOOO ESTAN DANDO DIFERENTE LARGO... DEBERIAN DE DAR AMBAS 1024 PARA 32X32
##        print(listaGenesAleatoria[x])
    
    
    
main()

###########################################################
##    Notas:
##
##    Si las imagenes van a ser jpg:
##    el arreglo tiene que tener (x, y, 3) el 3por ser RGB
##
##    Cada elemento es el color del pixel. El elemento
##    tiene que ser un entero del tamano de un byte
###########################################################
