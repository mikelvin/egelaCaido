import time
import platform
import subprocess as sp
import random
import datetime

from controlTweepy import *

from datetime import date
from datetime import datetime
from ControlFile import ControlFile

blockTwitterForTesting = True


trustServer = ""
evalServer = ""
past = ""
kontagailua = 0
booleanCounter = 0
# phrasesON = 0
# phrasesOFF = 0
timer = 0

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
    global kontagailua, booleanCounter, timer
    setUp()
    prevState = 0
    sleepTime = 60
    while True:

        state, mean = ipcheck(evalServer, trustServer)
        prove = confirmStatus(state, 5, 0.2)

        if prove:
            mean = "Trust_" + mean
        else:
            mean = "NoTrust_" + mean

        if state == 0:
            sleepTime = 5

        elif state != 0:
            sleepTime = 60

        # abrir archivo de frases aleatorias para decir cuando eGela no ha caído

        #TODO Es Muy importante arreglar el reloj para que no twittee cada nada
        if state == 1 and prove:
            kontagailua = kontagailua + 1
            booleanCounter = booleanCounter + 1
            if booleanCounter == 60:
                frase = praOn.getRandomNoRepLine
                print(frase)
                twitea(frase)
                booleanCounter = 0
        else:
            booleanCounter = 0
            if prove and state == 0 and prevState == 1:
                frase = praOff.getRandomNoRepLine
                twitea(frase)
                # pausa de 30 segundos para que si se ha caído no tuitee cada minuto que está caída
                time.sleep(30)


        recordData(mean)
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time + " " + mean)

        prevState = state
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




print(api)

print(time.monotonic())
print("time.monotonic()")
time.sleep(1)
print(time.time())
print(time.monotonic())
print(time.perf_counter())
#main()
