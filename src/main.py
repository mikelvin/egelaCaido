import time
import platform
import subprocess as sp
import datetime

from src.controlTweepy import twittea

from datetime import date
from datetime import datetime
from src.ControlFile import ControlFile


trustServer = ""
evalServer = ""
past = ""
kontagailua = 0
booleanCounter = 0


sleepTime = 120
praOn = ControlFile("phrasesON.txt", 5)
praOff = ControlFile("phrasesOFF.txt", 5)


def setUp():
    print("\nSTART")
    global trustServer, evalServer, kontagailua, booleanCounter

    trustServer = "google.com"
    evalServer = "egela.ehu.eus"
    kontagailua = 0
    booleanCounter = 0
    recordData("Start")


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
                    if tiempoCaido < 10:
                        frase = "eGela vuelve a estar disponible. Ha estado "
                        frase += transformTime(tiempoCaido)
                        twittea(frase)
                    else:
                        print("No se ha caido el suficiente tiempo para twittear")

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
                    tiempoCaido = time.monotonic()
                    frase = praOff.getRandomNoRepLine()
                    twittea(frase)
                    # pausa de 30 segundos para que si se ha caído no tuitee cada minuto que está caída
                    # time.sleep(30)
            else:
                booleanCounter = 0
                if state == 3:
                    print("Problemas de conexion")

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

main()
