import serial
import time
import matplotlib.pyplot as plt
import numpy as np
from threading import Thread
from scipy.optimize import curve_fit

"""
Function to convert the voltage read by the ADC to Temperature in Celsius
"""


def convertToTemp(VoutF, calValues):
    V2 = VoutF / 2.13 + calValues[0]
    Rt = (10e3 * (V2)) / (3.3 - V2)
    tempF = float(func(Rt, calValues[1], calValues[2]))

    return tempF


"""
    create a function to fit with your data. A  and B are the coefficients that curve_fit will calculate for you. 
    In this part you need to guess and/or use mathematical knowledge to find
    a function that resembles your data
    """


def func(R, A, B):
    return A + B * np.log(R)


# Function that checks for a calibration file for creating interpolating curve (T(R))
# if there is no file, enter calibration routine and creates it.
def cal(serialPort):
    """
    Try to open cal.values file. Otherwise, create it
    """
    calValues = []

    try:
        file = open('cal.values', 'r')
        print "Abriu arquivo de calibracao corretamente"
        read = file.readlines()
        for value in read:
            calValues.append(float(value))
    except IOError:
        print "Arquivo nao existente. Entrando no modo de calibracao:"
        file = open('cal.values', 'w')
        T = np.array([])  # y-axis
        R = np.array([])  # x-axis
        string = raw_input("Entre com o valor de temperatura (em float).\nOu qualquer letra para sair da calibracao\n")
        while True:
            try:
                stringF = float(string)
            except:
                break

            data = serialPort.write('r\n')  # send read data command
            tempS = serialPort.readline()  # read data sent back by the arduino
            try:  # try;except statement to bypass any error during communication
                tempF = float(tempS)  # Convert string to float
                T = np.append(T, [stringF])
                R = np.append(R, [tempF])
            except ValueError:
                print "Nenhum valor foi recebido do Arduino"  # Write on terminal if an exception was thrown
            string = raw_input(
                "Entre com o novo valor de temperatura (em float).\nOu qualquer letra para sair da calibracao\n")
        vOffset = raw_input("Entre com o valor do offset da tensao de calibracao\n")
        print str(T)
        print str(R)

        y = np.array(T, dtype=float)  # transform your data in a numpy array of floats
        x = np.array(R, dtype=float)  # so the curve_fit can work

        """
        make the curve_fit
        """
        popt, pcov = curve_fit(func, x, y, p0=(1, 1))

        """
        The result is:
        popt[0] = A , popt[1] = B of the function, so T = f(R) = popt[0] + popt[1]*log(R).
        """
        file.writelines(str(vOffset) + '\n' + str(popt[0]) + '\n' + str(popt[1]) + '\n')
        calValues.append(vOffset)
        calValues.append(popt[0])
        calValues.append(popt[1])

    print "T(R) = %s + %s*log(T)\n" % (calValues[1], calValues[2])
    file.close()

    return calValues

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
    port = raw_input("Entre com o nome da porta serial do arduino\n")
    arduino = serial.Serial(port, baudRate)
    time.sleep(1)
    arduino.write('r\n')
    calValues = cal(arduino)
    a = setpoint(arduino)
    a.start()
    voutF = 0.0
    x = list()
    y = list()
    t = 1
    hour_list = list()
    plt.figure()
    plt.xlabel('Horario')
    plt.ylabel('Temperatura')
    while True:
        data = arduino.write('r\n',)
        voutS = arduino.readline()
        try:
            voutF = float(voutS)
            tempF = convertToTemp(voutF, calValues)
            y.append(tempF)
            hora = time.strftime("%H:%M:%S", time.localtime())
            hour_list.append(hora)
            x.append(t)
            t = t + 1
            plt.xticks(x, hour_list)
            plt.plot(x, y, "r-*")
            plt.pause(1)
        except ValueError:
            print "No concrete value was received"

if __name__ == "__main__":
    main()