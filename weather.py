import requests
import datetime

# Pulls the weather information json from national weather service
def get_weather():
  return requests.get("https://api.weather.gov/gridpoints/BGM/44,70/forecast").json()

weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
# Number map for converting numbers in strings to actual int
numberMap = {"one":1, "two":2 ,"three":3, "four":4, "five":5, "six":6,"seven":7,"eight":8,"nine":9,"ten":10,"eleven":11, "twelve":12}

weather = get_weather()
# Returns the current day of the week using datetime.
def current_day():
    index = datetime.datetime.now().weekday()
    return weekdays[index]
# Parses string for the time slot in the string. Returns the day of the week and the time in 'number period' format.
def parse_sentence_for_time(s):
    tokens = s.split(" ")
    period = ""
    time = ""
    day = None
    # Pull the time period from the string.
    if "am" in tokens:
        period = "am"
    else:
        period = "pm"
    # Pull the day and time if there from the string.
    for index in range(len(tokens)):
        if tokens[index] in weekdays:
            day = tokens[index]
        if tokens[index] in numberMap and time == "":
            time = tokens[index]
    # Default case if there is no day.
    if day is None:
        if "tomorrow" in tokens:
            day = weekdays[(weekdays.index(current_day())+1)%7]
        else:
            day = current_day()
    # Default case if there is no time.
    if time == "":
        if "night" in tokens or "tonight" in tokens:
            time = "eight"
            period = "pm"
        else:
            time = "twelve"
            period = "pm"
    # Check if all information is available before returning.
    if time is not None and period is not None and day is not None:
        return (day, time_generator_3000(time + " " + period))
    # Otherwise return an invalid value to be caught later.
    return -1

# Return an integer representing the time on the 24 hour clock. Takes in a str in the format 'time period' on 
# the 12 hour clock cycle.
def time_generator_3000(str):
    hour = -1
    if "am" in str:
        hour = 0
    elif "pm" in str:
        hour = 12
    else:
        return -1 #invalid output
    hour_string = str.split(" ")[0].lower() #pre-condition, str first element is a number.
    if hour_string not in numberMap:
        return -1 # invalid output
    # Check the special case of 12pm and 12am being switched based on the simple conversion logic.
    if hour_string == "twelve":
        if "am" in str:
            return numberMap[hour_string] + 12
        else:
            return numberMap[hour_string] 
    return numberMap[hour_string] + hour

# Returns the detailed weather report based on the input string. Catches the invalid outputs from
# the function calls it makes and raises a ValueError to be caught in the main polling loop.
def get_weather_results(input):
    day_time = parse_sentence_for_time(input)
    # Raise error if invalid time.
    if day_time == -1:
        raise ValueError
    # Pull day and time.
    day, time  = day_time
    # Get current weather json from national weather service.
    w = get_weather()
    # Find correct index to get the right time period from the json.
    index = find_index(day,time)
    return w['properties']['periods'][index]['name'], w['properties']['periods'][index]['detailedForecast']

# Takes the day and time and returns the corret json index to receive the detailed weather forecast.
def find_index(day,time):
    # Time_bonus variable used from shifting day from changing at 12am to 4am. Additionally adds 1 to index
    # if at night to work with the json for night weather calling.
    time_bonus = 0
    if (time <= 4):
        time_bonus = -1
    elif (time >= 18):
        time_bonus = 1
    else: 
        time_bonus = 0
    # Curr_time_offset takes the current time into account for indexing because if it is already night,
    # there will only be a night weather report for the day. Otherwise there will be an index for the 
    # current time period (morning or afternoon for example) and night.
    curr_time_offset = 0
    if (datetime.datetime.now().hour >= 18):
        curr_time_offset = -1
    today = current_day()
    # Current day index in weekdays.
    today_index = weekdays.index(today)
    # Requested day index in weekdays.
    day_index = weekdays.index(day)
    diff = day_index - today_index
    result = 0
    # If requested day comes before current day in weekdays map, this is the index logic.
    if (diff <0):
        result = (7 + diff) * 2 + time_bonus + curr_time_offset
    # Index logic if day comes after current day in weekdays map.
    else:
        result = diff * 2 + time_bonus + curr_time_offset
    # If index out of bounds return current day.
    if (result < 0 or result > 14):
        result = 0

    return result