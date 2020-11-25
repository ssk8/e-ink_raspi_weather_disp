from os import environ
from time import sleep
from datetime import datetime, timedelta
import requests
from weather_graphic import Conditions, Weather_Graphic
from digitalio import DigitalInOut
from busio import SPI
import board
from adafruit_epd.ssd1675 import Adafruit_SSD1675 

display = Adafruit_SSD1675(122, 250, SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO), 
            cs_pin=DigitalInOut(board.CE0), dc_pin=DigitalInOut(board.D22), sramcs_pin=None,
            rst_pin=DigitalInOut(board.D27), busy_pin=DigitalInOut(board.D17),)

display.rotation = 3


LAT, LON = "39.571", "-97.662"
url = "http://api.openweathermap.org/data/2.5/weather"
params = {"appid": environ['OPEN_WEATHER_TOKEN'], "lat": LAT, "lon": LON, }

last_update = datetime.now()-timedelta(minutes=20)

while True:
    now = datetime.now()
    if (6<now.hour<21) and ((((now-last_update).seconds)/60)>15):
        response = requests.get(url=url, params=params)
        # print(response.text)   
        if response.status_code == 200:
            conditions = Conditions(response.json())
            graphic = Weather_Graphic(conditions, display)
            im = graphic.create_image()
        else:
            print(f"Unable to retrieve {response.url}")
        display.image(im)
        display.display()
        last_update = datetime.now()
    sleep(60)