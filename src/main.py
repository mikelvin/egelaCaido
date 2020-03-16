import os
import time
import platform
import subprocess as sp
import datetime

from src.controlTweepy import *

from datetime import date
from datetime import datetime
from src.ControlFile import ControlFile

warnToMD = True

trustServer = ""
evalServer = ""
past = ""
kontagailua = 0
booleanCounter = 0
egelaEstaCaido = False

cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
# print("Files in %r: %s" % (cwd, files))

sleepTime = 120

try:
    praOn = ControlFile(cwd + "\egelaCaido\src\phrasesON.txt", 5)
except FileNotFoundError as e:
    try:
        praOn = ControlFile(cwd + "/egelaCaido/src/phrasesON.txt", 5)
    except FileNotFoundError as e:
        praOn = ControlFile("../egelaCaido/src/phrasesON.txt", 5)


try:
    praOff = ControlFile(cwd + "\egelaCaido\src\phrasesOFF.txt", 5)
except FileNotFoundError as e:
    try:
        praOff = ControlFile(cwd + "/egelaCaido/src/phrasesOFF.txt", 5)
    except FileNotFoundError as e:
        praOff = ControlFile("../egelaCaido/src/phrasesOFF.txt", 5)



def setUp():

    print("\nSTART")
    global trustServer, evalServer, kontagailua, booleanCounter

    trustServer = "google.com"
    evalServer = "egela.ehu.eus"
    kontagailua = 0
    booleanCounter = 0
    recordData("Start")

    today = date.today()
    now = datetime.now()


    sendMdToUsers("Programa Iniciado a las "
                  + time.ctime()  + "\n Configuracion del bot: \n Tweets bloqueados: " + str(blockTwitterForTesting), notifyWhenTweetToUser)

def main():
    global kontagailua, booleanCounter
    tiempoCaido = 0
    # timer = time.monotonic()

    setUp()
    prevState = -8
    sleepTime = 60
    while True:
        # timer = time.monotonic()

        state, mean = ipcheck(evalServer, trustServer)
        prove = confirmStatus(state, 5, 0.2)

        if prove:
            mean = "Trust_" + mean
        else:
            mean = "NoTrust_" + mean

        if state == 0 and prove:
            sleepTime = 5

        elif state != 0:
            sleepTime = 60

        # abrir archivo de frases aleatorias para decir cuando eGela no ha caído

        # TODO Es Muy importante arreglar el reloj para que no twittee cada nada
        if prove:
            if state == 1:
                # Si anteriormente estaba desactivado entonces va a enviar un tweet notificando que vuelve a estar activo
                # En este mismo programa tambien se calcula cuanto tiempo esta activado
                if prevState == 0:
                    tiempoCaido = int(round(time.monotonic()-tiempoCaido))
                    if egelaEstaCaido:
                        egelaEstaCaido = False
                        frase = "eGela vuelve a estar disponible. Ha estado caido "
                        frase += transformTime(tiempoCaido)
                        twittea(frase)
                    else:
                        print("No se ha caido el suficiente tiempo como para twittear")
                        sendMdToUsers("No se ha caido el suficiente tiempo como para twittear", warnToMD)

                # kontagailua = kontagailua + 1
                booleanCounter = booleanCounter + 1
                if booleanCounter == 60:
                    frase = praOn.getRandomNoRepLine()
                    print(frase)
                    twittea(frase)
                    booleanCounter = 0
            elif state == 0:
                booleanCounter = 0
                #Solo va a twittear si anteriormente estaba activo, es decir va a twitear una sola vez cuando se caiga
                if prevState == 1:
                    egelaEstaCaido = False
                    tiempoCaido = time.monotonic()
                    sendMdToUsers("PROGRAMA: state = 0, parece que se ha caido", warnToMD)
                elif time.monotonic()-tiempoCaido > 60:
                    egelaEstaCaido = True
                    frase = praOff.getRandomNoRepLine()
                    twittea(frase)
            else:
                booleanCounter = 0
                if state == 3:
                    print("Problemas de conexion")
                    if prevState != 3:
                        sendMdToUsers("Problemas de conexion", warnToMD)

        recordData(mean)
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        print(current_time + " " + mean)
        if prove:
            prevState = state
        time.sleep(sleepTime)


def transformTime(tiempoCaido):
    tiempoCaido = int(tiempoCaido)
    frase = ""
    d = (tiempoCaido // 3600) // 24
    h = (tiempoCaido // 3600) % 24
    m = (tiempoCaido // 60) % 60
    s = tiempoCaido % 60

    if d != 0:
        frase += str(d) + " dia"
        if d != 1:
            frase += "s"
        if h != 0 or m != 0:
            frase += ", "

    if h != 0:
        frase += str(h) + " hora"
        if h != 1:
            frase += "s"
        if m != 0:
            frase += ", "

    if m != 0:
        frase += str(m) + " minuto"
        if m != 1:
            frase += "s"

    if m != 0 or h != 0 or d != 0:
        frase += " y "

    frase += str(s) + " segundo"
    if s != 1:
        frase += "s"
    return frase


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

    try:
        f = open(cwd + "\egelaCaido\src\data11.txt", "a+")
    except FileNotFoundError as e:
        f = open("../egelaCaido/src/data11.txt", "a+")

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
    stop = False
    a = []
    while times > 0 and not stop:
        # Para sincronizar bien el tiempo que queremos que tarde en calcular
        # ere = time.monotonic()
        sta, mean = ipcheck(trustServer, evalServer)
        a.append(sta)
        if sta != status:
            stop = True
        """
        delay = delay - (time.monotonic() - ere)
        if delay < 0:
            delay = 0
        """
        time.sleep(delay)
        times = times - 1
    return not stop, a


# ere = time.monotonic()
# trustServer = "google.com"
# evalServer = "egela.ehu.eus"
# print(confirmStatus(1,10,1))
# print(time.monotonic()-ere)

# print("time.monotonic()")
# time.sleep(1)
# print(time.time())
# print(time.monotonic())
# print(time.perf_counter())

# main()
# print(time.ctime())
