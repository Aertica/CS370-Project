import numbers
import threading
from database import Database, WeatherData
from sensors import Anemometer, Temp
from flask import Flask, render_template
import board
import time

app = Flask(__name__)

@app.route('/')
def index():
    database = Database('data.db')
    recent = database.get_recent(240)
    if len(recent) == 0:
        recent = [WeatherData(0, 0, 0, 0, 0)]
        
    data = recent[0].as_dict()
    data['temperature_avg'] = 0
    data['humidity_avg'] = 0
    data['wind_speed_avg'] = 0
    for weatherdata in recent:
        data['temperature_avg'] = data['temperature_avg'] + weatherdata.temperature
        data['humidity_avg'] = data['humidity_avg'] + weatherdata.humidity
        data['wind_speed_avg'] = data['wind_speed_avg'] + weatherdata.wind_speed
    data['temperature_avg'] = data['temperature_avg'] / len(recent)
    data['humidity_avg'] = data['humidity_avg'] / len(recent)
    data['wind_speed_avg'] = data['wind_speed_avg'] / len(recent)

    for key in data:
        if isinstance(data[key], numbers.Number):
            data[key] = int(data[key] * 100) / 100

    return render_template('index.html', data=data)

if __name__ == "__main__":
    database = Database('data.db', True)
    
    print(threading.current_thread())
    anemometer = Anemometer(5)
    def init():
        anemometer.start()
    threading.Thread(target=init).start()

    temp = Temp(board.D4)

    def add_data():
        while True:
            temperature = temp.temp_f()
            humidity = temp.humidity()
            pressure = 0
            wind_speed = anemometer.current_speed

            utc = time.time()
            data = WeatherData(temperature, humidity, pressure, wind_speed, utc)
            database.add(data)

            time.sleep(1)

    threading.Thread(target=add_data).start()

    app.run(host='0.0.0.0', debug=False)