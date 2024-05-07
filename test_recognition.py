import pyaudio
from time import sleep as slumber
from vosk import Model, KaldiRecognizer
import json
import pyttsx3
import weather
import jokes
engine = pyttsx3.init()
engine.setProperty('voice',"english")
engine.setProperty('rate',120)

model = Model('vosk-model-small-en-us-0.15')
recognizer = KaldiRecognizer(model, 16000)

cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True,frames_per_buffer=8192)
stream.start_stream()
with open("resources/prompts.json", "rb") as f:
    prompt_map = json.load(f)

ITHACA_LOCATION = (42.440498, -76.495697)

loop_running = True
while loop_running:
    data_initial = stream.read(2048, exception_on_overflow=False)
    if recognizer.AcceptWaveform(data_initial):
        keyword = recognizer.Result()
        print(keyword)
        if ("mongo" in keyword):    
            print("WASSUP")
        
            print("ready")
            while True:
                data = stream.read(4096, exception_on_overflow=False)
                if recognizer.AcceptWaveform(data):
                    t = (recognizer.Result())[14:-3]
                    match = None
                    for k,v in prompt_map.items():
                        for possible_match in v:
                            if possible_match in t:
                                match = k
                    print(t)
                    print(match)
                    if match == None:
                        engine.say("i do not understand")
                    else:
                        if match == 'weather':
                            engine.say(weather.get_weather_results(t))
                        elif match == 'joke':
                            engine.say(jokes.get_joke())
                        elif match == 'close':
                            engine.say("we over")
                            engine.runAndWait()
                            loop_running = False
                            break
                        else:
                            engine.say("unimplemented command")
                    engine.runAndWait()
                    break