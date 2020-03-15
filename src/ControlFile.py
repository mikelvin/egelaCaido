import random
from controlTweepy import prevTweets

class ControlFile:


    def __init__(self, archivo, dif):
        self.file = archivo
        self.lines = self.howManyPhrasesON()
        # Puede ser que no se escriban tantas lineas como posiciones en self.prevLista, En este caso ocurriria un error
        # ya que una vez todas las frases esten dentro de self.prevLista, el programa dejara de imprimir mas
        if self.lines <= dif:
            dif = self.lines - 1

        self.prevLista = self.updatePrevLista(dif)


    # Coje una frase aleatoria y despues de haber comprobado que no se ha seleccionado aun, la devuelve.
    # Si se ha seleccionado entonces elige otra

    def getRandomNoRepLine(self):
        frase = ""
        g = open(self.file, "r")
        i = random.randint(1, self.lines)
        while i in self.prevLista:
            i = random.randint(1, self.lines)
        self.desplazaLista(i)
        for z in range(0, i):
            frase = g.readline()
        return frase

    #Se encarga en desplazar a la derecha los numeros de su array (contiene el nuemero de linea de las frases inpresas)
    # y añade un nuevo valor a la primera posicion
    def desplazaLista(self, valor):
        i = len(self.prevLista)-1
        while i > 0:
            self.prevLista[i] = self.prevLista[i-1]
            i -= 1
        self.prevLista[0] = valor

    #Esta funcion cuenta cuantas lineas/frases tiene el docuemento asignado al objeto (self.file)
    def howManyPhrasesON(self):
        i = 0
        g = open(self.file, "r")
        l = len(g.readlines())
        g.close()
        return l

    # Se encarga de buscar una frase en el archivo devolviendo la ubicacion de su linea
    def findFraseLine(self, frase):
        g = open(self.file, "r")
        frase += '\n'
        i = 0
        f = False
        for line in g.readlines():
            i += 1
            if line == frase:
                f = True
                break
        if not f:
            i = 0
        return i

    #Obtiene los tweets recientes y usando la busqueda de frase añade esas frases a la lista de frases previas
    def updatePrevLista(self, cont):
        a = [0]*cont
        f = prevTweets(cont + 10)
        i = 0
        for frases in f:
            h = self.findFraseLine(frases)
            if h != 0 and i < cont:
                a[i] = h
                i += 1
            elif i >= cont:
                break
        return a