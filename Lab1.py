#Juan Diego Solorzano 18151
#Labortorio 1

import struct

def char(c):
    return struct.pack('=c', c.encode('ascii'))

def word(c):
    return struct.pack('=h', c)

def dword(c):
    return struct.pack('=l', c)

def glCreateWindow(width, height):
        win = Render(width, height)
        return win

class Render(object):
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.clearC = 0
        self.color = 0
        self.xw = 0
        self.yw = 0
        self.widthw = width
        self.heightw = height
        self.framebuffer = []

    def glInit(self, width, height):
        return
    
    #Area para pintar
    def glViewPort(self, x, y, width, height):
        self.xw = x
        self.yw = y
        self.widthw = width
        self.heightw = height

    #Pintar imagen   
    def glClear(self):
        self.framebuffer = [
            [self.clearC for x in range(self.width)]
            for y in range(self.height)
        ]

    #Color para pintar imagen
    def glClearColor(self, r, g, b):
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        self.clearC = bytes([b, g, r])
        self.glClear()

    #Crear archivo de la imagen
    def glFinish(self, filename):
        f = open(filename, 'bw')

        #file header
        f.write(char('B'))
        f.write(char('M'))
        f.write(dword(14 + 40 + self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(14 + 40))

        #image header
        f.write(dword(40))
        f.write(dword(self.width))
        f.write(dword(self.height))
        f.write(word(1))
        f.write(word(24))
        f.write(dword(0))
        f.write(dword(self.width * self.height * 3))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))
        f.write(dword(0))

        #pixel data
        for x in range(self.width):
            for y in range(self.height):
                f.write(self.framebuffer[y][x])

        f.close()

    #Pintar punto
    def glVertex(self, x, y):
        xn = (x + 1)*(self.widthw/2) + self.xw
        yn = (y + 1)*(self.heightw/2) + self.yw
        xn = int(xn)
        yn = int(yn)
        self.framebuffer[yn][xn] = self.color

    #Color del punto
    def glColor(self, r, g, b):
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        self.color = bytes([b, g, r])

print("SR1: Point")
i = False
while i == False:
    
    print("Ingrese el tamanio del framebuffer")
    wid = int(input("width: "))
    hei = int(input("height: "))
    bitmap = glCreateWindow(wid, hei)

    print("Ingrese los valores r g b para el color de la imagen (valores de 0 a 1)")
    r = float(input("r: "))
    g = float(input("g: "))
    b = float(input("b: "))
    bitmap.glClearColor(r, g, b)

    print("Ingrese los valores r g b para el color del punto (valores de 0 a 1)")
    rp = float(input("r: "))
    gp = float(input("g: "))
    bp = float(input("b: "))
    bitmap.glColor(rp, gp, bp)

    print("Ingrese los valores del view port")
    x = int(input("x: "))
    y = int(input("y: "))
    width = int(input("width: "))
    height = int(input("height: "))
    bitmap.glViewPort(x, y, width, height)

    print("Ingrese las coordenadas donde se dibujara el punto (valores de -1 a 1)")
    xp = float(input("x: "))
    yp = float(input("y: "))
    bitmap.glVertex(xp, yp)
    bitmap.glFinish('resultado.bmp')
    print("Archivo creado")
    op = input("Desea crear otra imagen? (y/n)\n")
    if op == 'n':
        i = True
