import board
import adafruit_mma8451
import time
from playsound import playsound
from pygame import mixer
def on():
    #Load resources
    i2c = board.I2C()
    flag = True
    mixer.init()
    mixer.set_num_channels(6)
    channel1 = mixer.Channel(0)
    sound1 = mixer.Sound("resources/Scream.wav")
    while (flag): #used to setup the accelerometer since it is buggy
        try:
            sensor = adafruit_mma8451.MMA8451(i2c,address=i2c.scan()[0])
            flag = False
        except:
            flag = True
            

    while True:
        acceleration = sensor.acceleration
        magnitude =  abs(acceleration[0]) + abs(acceleration[1]) + abs(acceleration[2])
        if magnitude > 15.5: #If magnitude is high enough, play the sound
            channel1.play(sound1)
        time.sleep(1)

if __name__ == "__main__": #Used for testing
    on()
