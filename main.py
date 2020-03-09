import time

import platform
import subprocess as sp

from datetime import date
from datetime import datetime


trustServer = ""
evalServer = ""
past = ""

sleepTime = 120

def setUp():
    global trustServer, evalServer

    trustServer = "google.com"
    evalServer = "egela.ehu.eus"
    recordData("Start")

def main():
    setUp()
    prevState = 0
    sleepTime = 60
    while True:

        state, mean = ipcheck(evalServer, trustServer)
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
        time.sleep(sleepTime)

def ipcheck(target, trust):
    statusT, resultT = sp.getstatusoutput("ping " + ("-n 1 " if platform.system().lower() == "windows" else "-c 1 ") + str(trust))
    statusH, resultH = sp.getstatusoutput("ping " + ("-n 1 " if platform.system().lower() == "windows" else "-c 1 ") + str(target))
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
    past = today.strftime("%Y/%m/%d") + " : "


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
