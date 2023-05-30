from as7263 import AS7263
import time
import RPi.GPIO as GPIO

as7263 = AS7263()

as7263.set_gain(16)
as7263.set_integration_time(17.857)
as7263.set_measurement_mode(2)
as7263.set_illumination_led(1)

redPin = 16   #Set to appropriate GPIO
greenPin = 18 #Should be set in the 

def blink(pin):
    GPIO.setmode(GPIO.BOARD)
    
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)
    
def turnOff(pin):
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def redOn():
    blink(redPin)

def redOff():
    turnOff(redPin)

def greenOn():
    blink(greenPin)

def greenOff():
    turnOff(greenPin)

try:
    while True:
        values = as7263.get_calibrated_values()
        R, S, T, U, V, W = [(value) for value in values]
        print("R = " + "{:4.6f}".format(R))
        print("S = " + "{:4.6f}".format(S))
        print("T = " + "{:4.6f}".format(T))
        print("U = " + "{:4.6f}".format(U))
        print("V = " + "{:4.6f}".format(V))
        print("W = " + "{:4.6f}".format(W))
        NDVI=((V-S)/(V+S))
        print("NDVI = {:4.2f}".format(NDVI))
        file = open("NDVI.csv","a")
        file.write("{0:0.1f},{1:0.1f},{2:0.1f},{3:0.1f},{4:0.1f},{5:0.1f},{6:0.1f}".format(R, S, T, U, V, W, NDVI)+"\n")
        file.close()        
        if NDVI > 0.2 and NDVI < 0.65:
            print("HEALTY" + "\n")
            greenOn()
            redOff()
        else:
            print("UNHEALTHY" + "\n")
            redOn()
            greenOff()
        
        time.sleep(0.5)   

except KeyboardInterrupt:
    as7263.set_measurement_mode(3)
    as7263.set_illumination_led(0)