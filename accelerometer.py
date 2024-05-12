import board
import adafruit_mma8451
import time
from playsound import playsound
from pygame import mixer

i2c = board.I2C()
flag = True
mixer.init()
mixer.music.load("resources/scream.mp3")
while (flag):
    try:
        sensor = adafruit_mma8451.MMA8451(i2c,address=i2c.scan()[0])
        flag = False
    except:
        flag = True
        

while True:
    acceleration = sensor.acceleration
    magnitude =  abs(acceleration[0]) + abs(acceleration[1]) + abs(acceleration[2])
    if magnitude > 14.5:
        mixer.music.play()
    time.sleep(1)
