import serial                   # Library for serial comm
import time                     # Library for real time and timing functions (sleep())
import matplotlib.pyplot as plt # Library for plotting data
from threading import Thread    # Library for creating threads

# Thread that writes the temperature setpoint to the arduino. The main reason to use a thread instead of a simple method
# is to be able to send this value to arduino without blocking the execution of the plotting method.
class setpoint(Thread):
    def __init__(self, serialPort):  #Default constructor
        Thread.__init__(self)
        self.serialPort = serialPort

    def run(self):
        while True:
            threshold = raw_input("Entre o valor do setpoint da temperatura \n") # wait for input in the terminal
            self.serialPort.write('w')              # Write operation, indicated by the 'w' character
            self.serialPort.write(str(threshold))   # Write the value entered previously
            self.serialPort.write('\n')             # Send break of line char

def main():
    plt.ion()           # Interacive plotting, enabling updating the graph as soon as new data is available
    baudRate = 9600     # Serial comm baud rate
    port = "COM4"       # Serial comm port
    arduino = serial.Serial(port, baudRate, timeout=3)  # Create serial comm object
    time.sleep(1)       # wait
    arduino.write('r\n')    # Write a dummy string, just to renew the buffer in the arduino
    a = setpoint(arduino)   # Create thread
    a.start();              # Start Thread
    tempF = 0.0             # Initialize the variable that will store the temperature
    x = list()              # List with x values
    y = list()              # List with y values
    t = 1                   # Auxiliar variable for plotting
    hour_list = list()      # List that will store real time strings
    plt.figure()            # Initialize figure
    plt.xlabel('Horario')   # X axis label
    plt.ylabel('Temperatura')   # Y axis label
    while True:             # main loop
        data = arduino.write('r\n',)                            # send read data command
        tempS = arduino.readline()                              # read data sent back by the arduino
        try:                                                    # try;except statement to bypass any error during communication
            tempF = float(tempS)                                # Convert string to float
            y.append(tempF)                                     # Append to y list
            hora = time.strftime("%H:%M:%S", time.localtime())  # Get real time
            hour_list.append(hora)                              # Append realtime to hour list
            x.append(t)                                         # Append t
            t = t + 1                                           # Increment t
            plt.xticks(x, hour_list)                            # Map t to the realtime string. This was used to be able to add strings to the x axis
            plt.plot(x, y, "r-*")                               # Plot data
            plt.pause(5)                                        #Pause plot and wait for next measurement
        except ValueError:
            print "No concrete value was received"              #Write on terminal if an exception was thrown

if __name__ == "__main__":
    main()