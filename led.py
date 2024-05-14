import RPi.GPIO as GPIO

# Set up GPIO pins when imported

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
    
freq = 10
duty_cycle = 100
pwm4 = GPIO.PWM(4,freq)


# Set up GPIO pins with desired frequency and duty cycle.
def setup():
    try:
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(4, GPIO.OUT)
            
        freq = 10
        duty_cycle = 100
        pwm4 = GPIO.PWM(4,freq)
    # Catch in case pins were already set up. This should occur but just in case.
    except:
        print("already setup")


def turn_LED_on():
    pwm4.start(duty_cycle)

def turn_LED_off():
    pwm4.stop()

# Clean up GPIO pins and turn off LED.
def shutdown_LED():
    pwm4.stop()
    GPIO.cleanup()