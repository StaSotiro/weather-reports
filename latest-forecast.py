from dotenv import load_dotenv
import pymysql 
import os

load_dotenv()

connection = pymysql.connect(host=os.getenv("DB_URL"),
                             user=os.getenv("DB_UNAME"),
                             password=os.getenv("DB_PASS"),
                             database=os.getenv("DB_SCHEMA"),
                             cursorclass=pymysql.cursors.DictCursor)

cursor = connection.cursor()


class Response:
    body = []
    status = 200


def latest_forecast():

    cursor.execute("SELECT cities.name, tab.* FROM(SELECT max(applicable_date) AS latest_date, forecast.* FROM forecast group by city_id ORDER BY applicable_date DESC) AS tab, cities WHERE city_id=cities.id")
    resp = Response()
    resp.body = cursor.fetchall()

    return resp

latest_forecast()