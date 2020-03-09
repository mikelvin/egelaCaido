import time

import platform
import subprocess as sp
import random
import datetime

from datetime import date
from datetime import datetime

trustServer = ""
evalServer = ""
past = ""
kontagailua = 0
booleanCounter = 0

sleepTime = 120


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
        g = open("phrases.txt", "r")
        i = random.randint(0, 6)
        for z in range(i, 6):
            frase = g.readline()
        if estado == "ON":
            kontagailua = kontagailua + 1
            booleanCounter = booleanCounter + 1
            if estado == "ON" and booleanCounter == 15:
                print(frase)
                booleanCounter = 0
        else:
            booleanCounter = 0
        # if mean == "OFF" || mean == "T-OFF/V-ON" || mean == "T-OFF/V-OFF":

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


main()
