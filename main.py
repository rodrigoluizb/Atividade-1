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
            self.serialPort.write('\n')

def main():
    plt.ion()
    baudRate = 9600
    port = "COM4"
    arduino = serial.Serial(port, baudRate, timeout=3)
    time.sleep(1)
    arduino.write('r\n')
    a = setpoint(arduino)
    a.start();
    tempF = 0.0
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
        data = arduino.write('r\n',)
        tempS = arduino.readline()
        try:
            tempF = float(tempS)
            y.append(tempF)
            t = t + 1
            plt.xticks(x, hour_list)
            plt.plot(x, y, "r-*")
            plt.pause(5)
        except ValueError:
            print "nada"

if __name__ == "__main__":
    main()