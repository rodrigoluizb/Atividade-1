import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread


class setpoint(Thread):
    def __init__(self, serialPort):
        Thread.__init__(self)
        self.serialPort = serialPort

    def run(self):
        while True:
            threshold = raw_input("Entre o valor do setpoint da temperatura \n")
            self.serialPort.write('w')
            self.serialPort.write(str(threshold))

def main():
    plt.ion()
    baudRate = 9600
    port = "/dev/tty.Bluetooth-Incoming-Port"
    arduino = serial.Serial(port, baudRate)

    a = setpoint(arduino)
    a.start();

    x = list()
    y = list()
    t = 1
    hour_list = list()
    plt.figure()
    plt.xlabel('Horario')
    plt.ylabel('Temperatura')
    while True:
        hora = time.strftime("%H:%M:%S", time.localtime())
        hour_list.append(hora)
        x.append(t)
        arduino.write('r')
        tempS = arduino.readline()
        tempF = float(tempS)
        print tempF
        y.append(tempF)
        t = t + 1
        plt.xticks(x, hour_list)
        plt.plot(x, y, "r-*")
        plt.pause(1)

if __name__ == "__main__":
    main()