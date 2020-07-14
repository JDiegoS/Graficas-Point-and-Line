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
    
    def glViewPort(self, x, y, width, height):
        self.xw = x
        self.yw = y
        self.widthw = width
        self.heightw = height
        
    def glClear(self):
        self.framebuffer = [
            [self.clearC for x in range(self.width)]
            for y in range(self.height)
        ]

    def glClearColor(self, r, g, b):
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        self.clearC = bytes([b, g, r])
        self.glClear()

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

    def glVertex(self, x, y):
        xn = (x + 1)*(self.widthw/2) + self.xw
        yn = (y + 1)*(self.heightw/2) + self.yw
        xn = int(xn)
        yn = int(yn)
        self.framebuffer[yn][xn] = self.color

    def glColor(self, r, g, b):
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)
        self.color = bytes([b, g, r])

bitmap = glCreateWindow(500, 500)
bitmap.glColor(0, 0, 1)
bitmap.glClearColor(0.5, 0.5, 0.5)
bitmap.glViewPort(250, 250, 250, 250)
bitmap.glVertex(-1, -1)
bitmap.glFinish('resultado.bmp')
