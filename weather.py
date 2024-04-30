import requests

def get_weather():
  return requests.get("https://api.weather.gov/gridpoints/BGM/44,70/forecast").json()

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]

numberMap = {"one":1, "two":2 ,"three":3, "four":4, "five":5, "six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11, "twelve":12}

weather = get_weather()

def current_day(forecast):
  seen = set(weekdays)
  for poss in forecast["properties"]["periods"]:
    day = poss['name'].split(" ")[0].lower()
    if day in seen:
      seen.remove(day)
  return seen.pop()

def parse_sentence_for_time(str):
  tokens = str.split(" ")
  for index in range(len(tokens) -1):
    if tokens[index] in numberMap and tokens[index+1] in ["am", "pm"]:
      #they asked for a specific time, check if there's a day of the week too?
      if index-1 >= 0 and tokens[index-1] in weekdays:
        return (tokens[index-1], time_generator_3000(tokens[index] + " " + tokens[index+1]))
      else:
        return (current_day(weather), time_generator_3000(tokens[index] + " " + tokens[index+1]))
  for index in range(len(tokens)-1):
    if tokens[index] in weekdays:
      return (tokens[index], 18 if tokens[index+1] == "night" else 12)
  return -1

def time_generator_3000(str):
  hour = -1
  if "am" in str:
    hour = 0
  elif "pm" in str:
    hour = 12
  else:
    return hour #invalid output
  hour_string = str.split(" ")[0].lower() #assumption, str first element is a number
  if hour_string not in numberMap:
    return -1
  return numberMap[hour_string] + hour

def get_weather_results(input):
  day_time = parse_sentence_for_time(input)
  
  if day_time == -1:
    return #make this exception to propagate into the main function and fix there
  day, time = day_time
  forecast = get_weather()
  today = current_day(forecast)
  parseFor = ""
  if time >= 18 or time < 6:
    day = weekdays[weekdays.index(day) - 1]
  print(day)
  print(time)