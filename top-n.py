from dotenv import load_dotenv
import pymysql 
from pymysql.constants import CLIENT
import os

load_dotenv()

connection = pymysql.connect(host=os.getenv("DB_URL"),
                             user=os.getenv("DB_UNAME"),
                             password=os.getenv("DB_PASS"),
                             database=os.getenv("DB_SCHEMA"),
                             client_flag=CLIENT.MULTI_STATEMENTS,
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()

class Response:
    humidity=[],
    air_pressure=[],
    min_temp=[],
    cur_temp=[],
    visibility=[],
    wind_speed=[],
    max_temp=[],
    status = 200

def top_n(n=3):
    cursor.execute(
        "SELECT cities.name, humidity FROM forecast, cities where cities.id=city_id ORDER BY humidity DESC LIMIT %s; "+
        "SELECT cities.name, air_pressure FROM forecast, cities where cities.id=city_id ORDER BY air_pressure DESC LIMIT %s; "+
        "SELECT cities.name, min_temp FROM forecast, cities where cities.id=city_id ORDER BY min_temp DESC LIMIT %s; "+
        "SELECT cities.name, cur_temp FROM forecast, cities where cities.id=city_id ORDER BY cur_temp DESC LIMIT %s; "+
        "SELECT cities.name, visibility FROM forecast, cities where cities.id=city_id ORDER BY visibility DESC LIMIT %s; "+
        "SELECT cities.name, wind_speed FROM forecast, cities where cities.id=city_id ORDER BY wind_speed DESC LIMIT %s; "+
        "SELECT cities.name, max_temp FROM forecast, cities where cities.id=city_id ORDER BY max_temp DESC LIMIT %s; ",
        (n,n,n,n,n,n,n)
    )

    resp3 = cursor.fetchall()
    finalResp = Response()
    finalResp.humidity = resp3
    
    while cursor.nextset():
        nextRes = cursor.fetchall()
        listkeys=list(nextRes[0].keys())
        # finalResp[listkeys[1]] = nextRes <-- Dynamic key creation (wanted to do)
        setattr(finalResp, listkeys[1], nextRes)

    return finalResp

top_n()