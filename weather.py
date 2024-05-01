import requests
import datetime

def get_weather():
  return requests.get("https://api.weather.gov/gridpoints/BGM/44,70/forecast").json()

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

numberMap = {"one":1, "two":2 ,"three":3, "four":4, "five":5, "six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11, "twelve":12}

weather = get_weather()

def current_day(forecast):
    index = datetime.datetime.now().weekday()
    return weekdays[index]

def parse_sentence_for_time(s):
    tokens = s.split(" ")
    period = ""
    time = ""
    day = None
    if "am" in tokens:
        period = "am"
    else:
        period = "pm"
    for index in range(len(tokens) - 1):
        if tokens[index] in weekdays:
            day = tokens[index]
        if tokens[index] in numberMap and time == "":
            time = tokens[index]

    if day is None:
        day = current_day(weather)
    if time == "":
        if "night" in tokens or "tonight" in tokens:
            time = "eight"
            period = "pm"
        else:
            time = "twelve"
            period = "pm"
    if time is not None and period is not None and day is not None:
        return (day, time_generator_3000(time + " " + period))
    return -1

def time_generator_3000(str):
    hour = -1
    if "am" in str:
        hour = 0
    elif "pm" in str:
        hour = 12
    else:
        return -1 #invalid output
    hour_string = str.split(" ")[0].lower() #assumption, str first element is a number
    if hour_string not in numberMap:
        return -1
    if hour_string == "twelve":
        if "am" in str:
            return numberMap[hour_string] + 12
        else:
            return numberMap[hour_string] 
    return numberMap[hour_string] + hour

def get_weather_results(input):
    day_time = parse_sentence_for_time(input)
    if day_time == -1:
        raise ValueError
    day, time = day_time
    today = current_day(weather)
    print(day)
    print(time)