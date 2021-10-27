from dotenv import load_dotenv
import pymysql 
from pymysql.constants import CLIENT
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

def avg_forecast():

    cursor.execute("WITH top_forecasts AS ( "+
    "SELECT f.*, ROW_NUMBER() OVER (PARTITION BY  city_id,DATE_FORMAT(applicable_date , '%Y-%m-%d ') ORDER BY applicable_date DESC) AS rn " +
    "FROM forecast AS f) "+
    "SELECT cities.name, avg(cur_temp), DATE_FORMAT(applicable_date , '%Y-%m-%d ') as the_day "+
    "FROM ( "+
    "SELECT * "+
    "FROM top_forecasts "+
    "WHERE rn<=3 "+
    ") AS tops, cities "+
    "WHERE  tops.city_id=cities.id "+
    "GROUP BY DATE_FORMAT(applicable_date , '%Y-%m-%d '), tops.city_id")

    resp = Response()
    resp.body = cursor.fetchall()

    return resp

avg_forecast()