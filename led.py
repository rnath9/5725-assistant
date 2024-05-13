import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
    
freq = 10
duty_cycle = 100
pwm4 = GPIO.PWM(4,freq)

def setup():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT)
            
        freq = 10
        duty_cycle = 100
        pwm4 = GPIO.PWM(4,freq)
    except:
        print("already setup")

def turn_LED_on():
    pwm4.start(duty_cycle)

def turn_LED_off():
    pwm4.stop()

def shutdown_LED():
    pwm4.stop()
    GPIO.cleanup()