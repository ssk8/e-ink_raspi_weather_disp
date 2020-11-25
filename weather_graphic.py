from datetime import datetime
import json
from PIL import Image, ImageDraw, ImageFont
from pint import UnitRegistry

ureg = UnitRegistry()
uQ = ureg.Quantity

small_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
medium_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 20)
large_font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 24)
w_icon_font = ImageFont.truetype("./meteocons.ttf", 52)

vane = Image.open('arrow_30x30.jpg')
vane_mask = Image.new("L", vane.size, 0)
v_draw = ImageDraw.Draw(vane_mask)
v_draw.ellipse((2, 2, vane.size[0]-2, vane.size[1]-2), fill=255)

icon_map = {"01d": "B","01n": "C","02d": "H","02n": "I","03d": "N","03n": "N","04d": "Y","04n": "Y","09d": "Q","09n": "Q","10d": "R","10n": "R","11d": "Z","11n": "Z","13d": "W","13n": "W","50d": "J","50n": "K",}

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


class Conditions:
    def __init__(self, w):
        self.name = f"{w['name']}"
        self.timestamp = datetime.fromtimestamp(w['dt'])
        self.timeszone = w['timezone']
        self.main = f"{w['weather'][0]['main']}"
        self.description = f"{w['weather'][0]['description']}"
        self.icon = icon_map[w['weather'][0]['icon']]
        self.temperature = uQ(w['main']['temp'], ureg.degK)
        self.heatIndex = uQ(w['main']['feels_like'], ureg.degC)
        self.windSpeed = w['wind']['speed']*ureg.kilometers/ureg.hour
        self.windDir = w['wind']['deg']
        self.barometricPressure = w['main']['pressure']*ureg.pascal
        self.humidity = w['main']['humidity']


class Weather_Graphic:
    def __init__(self, current_conditions, display):
        self.small_font = small_font
        self.medium_font = medium_font
        self.large_font = large_font
        self.display = display
        self.cond = current_conditions
        self._time_text = f"{self.cond.timestamp.strftime('%b %d  %H:%M')}"
        #self._temperature = f"{self.cond.temperature.to('degC').magnitude:.1f}°C"
        self._temperature = f"{self.cond.temperature.to('degF').magnitude:.0f}°F"
        self._wind = f"{self.cond.windSpeed.to(ureg.miles/ureg.hour).magnitude:.1f} mph"
        self._dir =  vane.rotate(359-self.cond.windDir)
        self._press = f"{self.cond.barometricPressure.to(ureg.inch_Hg).magnitude:.2f}\" Hg"
        self._humi = f"{self.cond.humidity:.0f}% hum"


    # def display_weather(self):
    #     print(f"{self.cond.name=}")
    #     print(f"{self.cond.timestamp=}")
    #     print(f"{self.cond.timeszone=}")
    #     print(f"{self.cond.main=}")
    #     print(f"{self.cond.description=}")
    #     print(f"{self.cond.icon=}")
    #     print(f"{self.cond.temperature=}")
    #     print(f"{self.cond.heatIndex=}")
    #     print(f"{self.cond.windSpeed=}")
    #     print(f"{self.cond.windDir=}")
    #     print(f"{self.cond.barometricPressure=}")



    def create_image(self):
        image = Image.new("RGB", (self.display.width, self.display.height), color=WHITE)
        draw = ImageDraw.Draw(image)

        # Draw the Icon
        font_width, font_height = w_icon_font.getsize(self.cond.icon)
        position = (self.display.width // 2 - font_width // 2 +5, self.display.height // 2 - font_height // 2 - 5,)
        draw.text(position, self.cond.icon, font=w_icon_font,fill=BLACK,)

        # Draw the city
        draw.text((5, 5), self.cond.name, font=self.small_font, fill=BLACK,)

        # Draw the time
        font_width, font_height = small_font.getsize(self._time_text)
        draw.text((self.display.width - font_width - 5,  5), self._time_text, font=self.small_font, fill=BLACK,)

        #Draw wind
        font_width, font_height = small_font.getsize(self._wind)
        draw.text((self.display.width - font_width -5, font_height * 2 - 5), self._wind, font=self.small_font, fill=BLACK,)
        image.paste(self._dir, (self.display.width -40, self.display.height//2-5), vane_mask)

        #Draw press
        font_width, font_height = small_font.getsize(self._press)
        draw.text((5, font_height * 2 - 5), self._press, font=self.small_font, fill=BLACK,)

        #Draw humidity
        font_width, font_height = small_font.getsize(self._humi)
        draw.text((5, font_height * 3 + 5), self._humi, font=self.small_font, fill=BLACK,)

        # Draw the main text
        font_width, font_height = large_font.getsize(self.cond.main)
        draw.text((5, self.display.height - font_height * 2), self.cond.main, font=self.large_font, fill=BLACK,)

        # Draw the description
        (font_width, font_height) = small_font.getsize(self.cond.description)
        draw.text((5, self.display.height - font_height - 5), self.cond.description, font=self.small_font, fill=BLACK,)

        # Draw the temperature
        font_width, font_height = large_font.getsize(self._temperature)
        position = (self.display.width - font_width - 2,self.display.height - font_height * 1.2,)
        draw.text(position, self._temperature, font=self.large_font, fill=BLACK,)

        return image

