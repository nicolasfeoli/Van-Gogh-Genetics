#Codigo que corre en Python 2.7


##from PIL import Image
##
##img = Image.new('RGB', (100, 200))
##img.putdata(my_list)
##img.save('image.png')


##Notas:
##
##    Si las imagenes van a ser jpg:
##        el arreglo tiene que tener (x, y, 3) el 3por ser RGB
##
##        Cada elemento es el color del pixel. El elemento tiene que ser un entero del tamano de un byte

import numpy
from PIL import Image

def producirImagenes(n, fmt, tamanoX, tamanoY, nombreImagen = "imagen"):
    #produce n imagenes del formato fmt
    #n es un int y fmt es un string
    for i in range(n):
        #produce n imagenes
        a = numpy.random.rand(tamanoX, tamanoY, 3)
        print type(a)
        a *= 255
        imagen= Image.fromarray(a.astype("uint8")).convert("RGBA")
        nombreImagen += "%000d." % i + fmt #reemplaza lo que hay en %000d por el entero i y agrega el formato
        imagen.save(nombreImagen)

def abrirImagen(nombre):
    im = Image.open(nombre)
    im.show()

def imprimirPixeles(nombre):
    im = Image.open(nombre)
    cargada = im.load()
    #for i in range(cargada.):
    #   print i
    print cargada[0,0]

def copiarImagen():
    tamanoX = 32
    tamanoY = 32
    a = list(list(list(0 for i in range(3) )\
                         for i in range(tamanoX)) \
                         for i in range(tamanoY))
    for i in range(tamanoY):
        for j in range(tamanoX):
            a[i][j][0] = 0
            a[i][j][1] = 0
            a[i][j][2] = 0
    #print a
    imagen = Image.fromarray(numpy.asarray(a).astype("uint8")).convert("RGB")
    imagen.save("negro.png")



#a = numpy.random.rand(10, 5, 3)
#print a
copiarImagen()
#abrirImagen("prueba1.bmp")
#imprimirPixeles("prueba1.bmp")
#producirImagenes(1, "png", 300, 300, "hola")

############################################################333

