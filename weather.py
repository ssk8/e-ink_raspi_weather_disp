# export OPEN_WEATHER_TOKEN='api token'
from os import environ
import time
import requests
from weather_graphic import Conditions, Weather_Graphic
from collections import namedtuple


LAT, LON = "39.571", "-97.662"
url = "http://api.openweathermap.org/data/2.5/weather"
params = {"appid": environ['OPEN_WEATHER_TOKEN'], "lat": LAT, "lon": LON, }


Display = namedtuple( 'Display', [ 'width', 'height' ] )
display = Display(255,122)

if True:
    response = requests.get(url=url, params=params)
    print(response)
    print(response.text)       
    if response.status_code == 200:
        conditions = Conditions(response.json())
        graphic = Weather_Graphic(conditions, display)
        graphic.display_weather()
        im = graphic.create_image()
        im.save("weather.jpg", "JPEG")
    else:
        print(f"Unable to retrieve {response.url}")
    #time.sleep(600)

