import pyaudio
from time import sleep as slumber
from vosk import Model, KaldiRecognizer
import json
import pyttsx3
import weather
import jokes
import game
RPi = True
try:
    import led
except:
    RPi = False
else:
    RPi = True

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

loop_running = True
while loop_running:
    data_initial = stream.read(4096, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data_initial):
        keyword = recognizer.Result()
        print(keyword)
        if ("mongo" in keyword):    
            if RPi:
                led.turn_LED_on()
            else:
                print("not RPi")
            while True:
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
                    print(t)
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
                                led.turn_LED_on
                            else:
                                print("Not RPi")
                            while True:
                                data = stream.read(4096, exception_on_overflow=False)
                                if recognizer.AcceptWaveform(data):
                                    if RPi:
                                        led.turn_LED_off
                                    t = (recognizer.Result())[14:-3]
                                    if ('ea' in t):
                                        game.play_chess(600)
                                    elif ('m' in t):
                                        game.play_chess(1200)
                                    elif ('h' in t):
                                        game.play_chess(1800)
                                    else:
                                        game.play_chess(1200)
                                    break
                            engine.say('that was fun!')
                        elif match == 'close':
                            engine.say("we over")
                            engine.runAndWait()
                            loop_running = False
                            break
                        else:
                            engine.say("unimplemented command")
                    engine.runAndWait()
                    break
if RPi:
    led.shutdown_LED()
