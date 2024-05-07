import time
import RPi.GPIO as GPIO
from threading import Thread

def setup_LED():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(4, GPIO.OUT)
    
freq = 10
duty_cycle = 100
pwm4 = GPIO.PWM(4,freq)

def turn_LED_on():
    pwm4.start(duty_cycle)

def turn_LED_off():
    pwm4.stop()

def shutdown_LED():
    pwm4.stop()
    GPIO.cleanup()