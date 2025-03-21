import sqlite3
from datetime import datetime

with open('sql/CREATE_TABLES.sql', 'r') as f:
    create_script = f.read()

with open('sql/DELETE_TABLES.sql', 'r') as f:
    delete_script = f.read()

with open('sql/INSERT_DATA.sql', 'r') as f:
    insert_script = f.read()

with open('sql/INSERT_BOGUS_DATA.sql', 'r') as f:
    insert_bogus_script = f.read()

with open('sql/SELECT_RECENT.sql', 'r') as f:
    select_script = f.read()

class WeatherData:
    def __init__(self, temperature, humidity, pressure, wind_speed, utc):
        self.temperature = temperature
        self.humidity = humidity
        self.pressure = pressure
        self.wind_speed = wind_speed
        self.utc = utc # unix timestamp

    def as_dict(self) -> dict:
        return {
            'temperature': self.temperature,
            'humidity': self.humidity,
            'pressure': self.pressure,
            'wind_speed': self.wind_speed,
            'utc': datetime.fromtimestamp(self.utc).strftime('%Y-%m-%d %H:%M:%S'),
        }

    def __repr__(self):
        return f"({self.temperature}, {self.humidity}, {self.pressure}, {self.wind_speed}, {self.utc})"

class Database:
    def __init__(self, file, override_existing=False):
        conn = sqlite3.connect(file)
        self.curser = conn.cursor()

        if override_existing:
            self.curser.executescript(delete_script)

        self.curser.executescript(create_script)

    def add(self, data: WeatherData):
        sql = insert_script.format(data.temperature, data.humidity, data.pressure, data.wind_speed, data.utc)
        self.curser.executescript(sql)

    def get_recent(self, n):
        sql = select_script.format(n)
        res = self.curser.execute(sql)
        list = []
        for data in res:
            list.append(WeatherData(data[0], data[1], data[2], data[3], data[4]))

        return list

    # For test purposes only
    def fill_with_bogus_data(self):
        for _ in range(100):
            self.curser.executescript(insert_bogus_script)