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
    data = database.get_recent(1)
    if len(data) == 0:
        data = WeatherData(0, 0, 0, 0, 0)
    else:
        data = data[0]
        
    print(data)
    return render_template('index.html', data=data.as_dict())

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
            if wind_speed == 0:
                continue

            utc = time.time()
            data = WeatherData(temperature, humidity, pressure, wind_speed, utc)
            database.add(data)

            time.sleep(4)

    threading.Thread(target=add_data).start()

    app.run(host='0.0.0.0', debug=False)