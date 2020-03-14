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


def setUp():
    global trustServer, evalServer, kontagailua, booleanCounter

    trustServer = "google.com"
    evalServer = "egela.ehu.eus"
    kontagailua = 0
    booleanCounter = 0
    recordData("Start")


def howManyPhrasesON():
    i = 0
    g = open("phrasesON.txt", "r")
    return len(g.readlines()) - 1


def howManyPhrasesOFF():
    i = 0
    g = open("phrasesOFF.txt", "r")
    return len(g.readlines()) - 1


def main():
    global kontagailua, booleanCounter
    setUp()
    howManyOn = howManyPhrasesON()
    howManyOFF = howManyPhrasesOFF()
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
        g = open("phrasesON.txt", "r")
        f = open("phrasesOFF.txt", "r")
        i = random.randint(0, howManyOn)
        for z in range(i, howManyOn):
            fraseON = g.readline()
        if estado == "ON":
            kontagailua = kontagailua + 1
            booleanCounter = booleanCounter + 1
            if estado == "ON" and booleanCounter == 60:
                print(fraseON)
                api.update_status(fraseON)
                booleanCounter = 0
        else:
            booleanCounter = 0
            j = random.randint(0, howManyOFF)
            for z in range(j, howManyOFF):
                fraseOFF = f.readline()
            if mean == "OFF":
                api.update_status(fraseOFF)
                # pausa de 30 segundos para que si se ha caído no tuitee cada minuto que está caída
                time.sleep(1800)

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
