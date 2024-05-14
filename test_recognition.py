import pyaudio
import os
import pygame
from time import sleep as slumber
slumber(20)
from vosk import Model, KaldiRecognizer
import json
import pyttsx3
import weather
import jokes
import game
import RPi.GPIO as GPIO
import random
from pygame import mixer
from glob import glob
import accelerometer
from threading import Thread
import sys
RPi = True
try:
    import led
except:
    RPi = False
else:
    RPi = True

os.putenv('SDL_VIDEODRIVER', 'fbcon')
os.putenv('SDL_FBDEV', '/dev/fb0')
os.putenv('SDL_MOUSEDRV', 'dummy')
os.putenv('SDL_MOUSEDEV','/dev/null')
os.putenv('DISPLAY','')

screen_width = 320
screen_height = 220
screen = pygame.display.set_mode((320, 240)) 
pygame.mouse.set_visible(False)

# Set the caption of the screen 
pygame.display.set_caption('Mungo Chess') 

# Fill the background colour to the screen 
pygame.init()
screen.fill((100,100,255)) 
font = pygame.font.Font(None, 32)
text = font.render("MUNGO!", True, (255,255,255))
text_rect = text.get_rect()
text_rect.center = (screen_width // 2, screen_height // 2)
# screen.blit(text, text_rect)

engine = pyttsx3.init()
engine.setProperty('voice',"english")
engine.setProperty('rate',120)

model = Model('vosk-model-small-en-us-0.15')
recognizer = KaldiRecognizer(model, 44100)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=44100, input=True,frames_per_buffer=8192)
stream.start_stream()
with open("resources/prompts.json", "rb") as f:
    prompt_map = json.load(f)

ITHACA_LOCATION = (42.440498, -76.495697)

available_buttons = set([17, 22, 23, 27])

for i in available_buttons:
    GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def quit_callback(channel):
    sys.exit()

GPIO.add_event_detect(17, GPIO.FALLING, callback=quit_callback, bouncetime=300)

t1 = Thread(target = accelerometer.on)
t1.setDaemon(True)
t1.start()
loop_running = True
#led.turn_LED_on()
engine.say("booted up")
engine.runAndWait()
try:
    while loop_running:
        data_initial = stream.read(4096, exception_on_overflow=False)
        if recognizer.AcceptWaveform(data_initial):
            keyword = recognizer.Result()
            print(keyword)
            mongo_match = False
            for v in prompt_map["keyword"]:
                if v in keyword:
                    mongo_match = True
            if mongo_match:    
                if RPi:
                    led.turn_LED_on()
                else:
                    print("not RPi")
                while True:
                    try:
                        data = stream.read(4096, exception_on_overflow=False)
                        if recognizer.AcceptWaveform(data):
                            if RPi:
                                led.turn_LED_off()
                            t = (recognizer.Result())[14:-3]
                            match = None
                            for k,v in prompt_map.items():
                                for possible_match in v:
                                    if possible_match in t:
                                        match = k
                            if match == None:
                                engine.say("i do not understand")
                            else:
                                if match == 'weather':
                                    engine.say(weather.get_weather_results(t))
                                elif match == 'joke':
                                    engine.say(jokes.get_joke())
                                elif match == 'game':
                                    engine.say('would you like to play easy, medium, or hard')
                                    engine.runAndWait()
                                    if RPi:
                                        led.turn_LED_on()
                                    else:
                                        print("Not RPi")
                                    while True:
                                        data = stream.read(4096, exception_on_overflow=False)
                                        if recognizer.AcceptWaveform(data):
                                            if RPi:
                                                led.turn_LED_off()
                                            t = (recognizer.Result())[14:-3]
                                            engine.say("good luck!")
                                            engine.runAndWait()
                                            pygame.mouse.set_visible(True)
                                            if ('ea' in t):
                                                game.play_chess(600)
                                            elif ('m' in t):
                                                game.play_chess(1200)
                                            elif ('h' in t):
                                                game.play_chess(1800)
                                            else:
                                                game.play_chess(1200)
                                            break
                                    led.setup()                                  
                                    for i in available_buttons:
                                        GPIO.setup(i, GPIO.IN, pull_up_down=GPIO.PUD_UP)
                                    screen = pygame.display.set_mode((320, 240))
                                    screen.fill((255,255,255))
                                    screen.blit(text, text_rect)
                                    pygame.mouse.set_visible(False)
                                    engine.say('that was fun!')
                                elif match == 'close':
                                    engine.say("we over")
                                    engine.runAndWait()
                                    loop_running = False
                                    break
                                elif match == 'music':
                                    quit = False
                                    music_files = glob("resources/music/*")
                                    song_index = random.randint(0,len(music_files)-1)
                                    song = music_files[song_index]
                                    print(song)
                                    channel2 = mixer.Channel(1)
                                    sound2 = mixer.Sound(song)
                                    #mixer.music.load(song)
                                    #mixer.music.play()
                                    channel2.play(sound2)
                                    channel2.set_volume(0.6)
                                    volume = 0.6
                                    while not quit and channel2.get_busy():
                                        if (not GPIO.input(27)):
                                            quit = True
                                        if GPIO.input(22):
                                            volume = min(volume+0.1, 1)
                                            channel2.set_volume(volume)
                                        if GPIO.input(23):
                                            volume = max(volume-0.1, 0.1)
                                            channel2.set_volume(volume)
                                    channel2.stop()
                                    led.setup()
                                else:
                                    engine.say("unimplemented command")
                            engine.runAndWait()
                            break
                    except ValueError:
                        engine.say("Invalid Time")
                        engine.runAndWait()
except KeyError:
    print("caught")
    pass
if RPi:
    led.shutdown_LED()
