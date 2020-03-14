import time
import platform
import subprocess as sp
import random
import datetime
import tweepy

from datetime import date
from datetime import datetime

consumer_key = "hr8ClRl4AniT2jdRHSTfkKuWu"
consumer_secret = "MHQpKBQCPFoRztKi4Z4MIKkCccgDtwTFQrXb4bLO2Xev5Mr5Yv"
access_token = "1235232986909601793-YORkwEC1S6879MssIlsWnpYsgxtYgR"
access_token_secret = "BboF9MdYCZ8kgFDAQkSTXkSK5nOpVh23juDhqHba6vQGv"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)

trustServer = ""
evalServer = ""
past = ""
kontagailua = 0
booleanCounter = 0
phrasesON = 0
phrasesOFF = 0

sleepTime = 120
praOn = ControlFile("phrasesON.txt", 5)
praOff = ControlFile("phrasesOFF.txt", 5)


def setUp():
    global trustServer, evalServer, kontagailua, booleanCounter

    trustServer = "google.com"
    evalServer = "egela.ehu.eus"
    kontagailua = 0
    booleanCounter = 0
    recordData("Start")

def main():
    global kontagailua, booleanCounter
    setUp()
    prevState = 0
    sleepTime = 60
    while True:

        state, mean = ipcheck(evalServer, trustServer)
        estado = mean
        if state == 0 and prevState != 0:
            if confirmStatus(state, 5, 0.2):
                mean = "IS_Trust_" + mean
            else:
                mean = "IS_NTrust_" + mean

            sleepTime = 5

        elif state != 0:
            if confirmStatus(state, 5, 0.2):
                mean = "Trust_" + mean
            else:
                mean = "NoTrust_" + mean
            sleepTime = 60

        prevState = state
        recordData(mean)
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time + " " + mean)
        # abrir archivo de frases aleatorias para decir cuando eGela no ha caído

        if estado == "ON":
            kontagailua = kontagailua + 1
            booleanCounter = booleanCounter + 1
            if booleanCounter == 60:
                frase = praOn.getRandomNoRepLine()
                print(fraseON)
                api.update_status(frase)
                booleanCounter = 0
        else:
            booleanCounter = 0
            if mean == "OFF":
                frase = praOff.getRandomNoRepLine()
                api.update_status(fraseOFF)
                # pausa de 30 segundos para que si se ha caído no tuitee cada minuto que está caída
                time.sleep(30)

        time.sleep(sleepTime)


def ipcheck(target, trust):
    statusT, resultT = sp.getstatusoutput(
        "ping " + ("-n 1 " if platform.system().lower() == "windows" else "-c 1 ") + str(trust))
    statusH, resultH = sp.getstatusoutput(
        "ping " + ("-n 1 " if platform.system().lower() == "windows" else "-c 1 ") + str(target))
    if statusT == 0:
        if statusH == 0:
            # print("System " + str(target) + " is UP !")
            meaning = "ON"
            ema = 1
        else:
            # print("System " + str(target) + " is DOWN !")
            meaning = "OFF"
            ema = 0
    else:
        if statusH == 0:
            meaning = "T-OFF/V-ON"
            ema = 2
        else:
            meaning = "T-OFF/V-OFF"
            ema = 3
        # print("System can't connect to reference host: " + str(trust))

    return ema, meaning

def recordData(data):
    global past

    f = open("data11.txt", "a+")

    today = date.today()
    now = datetime.now()

    current_time = now.strftime("%H:%M")
    d1 = today.strftime("%m/%d")
    d1 = d1 + " : "
    if past == d1:
        d1 = " * "

    f.write(d1 + current_time + " --> " + str(data) + " \n")

    f.close()
    past = today.strftime("%m/%d") + " : "

def confirmStatus(status, times, delay):
    global trustServer, evalServer
    e = True
    sta, mean = ipcheck(trustServer, evalServer)
    while times > 0 and e:
        if sta != status:
            e = False

        times = times - 1
        time.sleep(delay)

    return e

class ControlFile:

    def __init__(self, archivo, dif):
        self.file = archivo
        self.prevLista = [0]*dif
        self.lines = self.howManyPhrasesON()

    def getRandomNoRepLine(self):
        g = open(self.file, "r")
        i = random.randint(1, self.lines)
        while i in self.prevLista:
            i = random.randint(1, self.lines)
        self.desplazaLista(i)
        for z in range(0, i):
            frase = g.readline()
        return frase

    def desplazaLista(self,valor):
        i = len(self.prevLista)-1
        while i > 0:
            self.prevLista[i] = self.prevLista[i-1]
            i -= 1
        self.prevLista[0] = valor

    def howManyPhrasesON(self):
        i = 0
        g = open(self.file, "r")
        l = len(g.readlines())
        g.close()
        return l



main()
