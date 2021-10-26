import json
import requests
from datetime import datetime, timedelta
from dotenv import load_dotenv
import pymysql 
import os

load_dotenv()

weatherSearchAPI = "https://www.metaweather.com/api/location/search/"
weatherAPI= "https://www.metaweather.com/api/location/"

locations = [["Oslo", "862592","1"], ["London", "44418","2"],["Athens", "946738","3"]]

connection = pymysql.connect(host=os.getenv("DB_URL"),
                             user=os.getenv("DB_UNAME"),
                             password=os.getenv("DB_PASS"),
                             database=os.getenv("DB_SCHEMA"),
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

def get_date_diff(date1, date2):
    sec = datetime.fromisoformat(date2)
    first = datetime.fromisoformat(date1)

    return abs(sec - first).days + 1 


def get_next_day(day):
    date = datetime.fromisoformat(day)
    nextDay = (date + timedelta(days=1)).strftime("%Y/%m/%d")
    return nextDay


def lambda_handler(event="", context=""):
    
    for location in locations:
        
        resp = requests.get(weatherAPI+location[1]+"/")
        resp = resp.json()

        weather = resp["consolidated_weather"]

        dateDiff = get_date_diff(weather[0]["applicable_date"], weather[-1]["applicable_date"]) 
        if dateDiff<7:
            for i in range(7-dateDiff):
                nextDate=get_next_day(weather[-1]["applicable_date"])

                day = requests.get(weatherAPI+location[1]+"/"+nextDate)
                day = day.json()

                weather.append(day[0])


        print(json.dumps(weather, indent=4, sort_keys=True))
        
        values = []
        for report in weather:
            values.append([
                location[2], 
                report["air_pressure"], 
                report["applicable_date"], 
                report["humidity"],
                report["max_temp"],
                report["min_temp"],
                 report["predictability"],
                 report["the_temp"],
                 report["visibility"],
                 report["weather_state_abbr"],
                 report["weather_state_name"],
                report["wind_direction"],
                report["wind_direction_compass"],
                report["wind_speed"]])
        
        
        cursor.executemany("INSERT INTO forecast (city_id, air_pressure, applicable_date, humidity, max_temp, min_temp, predictability, cur_temp, visibility, weather_state_abbr, weather_state_name, wind_direction, wind_direction_compass, wind_speed) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" , values)
        connection.commit()

    return {
    'statusCode': 200,
    'body': json.dumps('Hello from Lambda!')
    }
