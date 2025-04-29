import queue
import sqlite3
from datetime import datetime
import threading

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
        return f"({self.temperature}, {self.humidity}, {self.pressure}, {self.wind_speed}, {datetime.fromtimestamp(self.utc)})"

class Database:
    def __init__(self, file, override_existing=False):
        self.conn = sqlite3.connect(file, check_same_thread=False)
        self.cursor = self.conn.cursor()
        if override_existing:
            self.cursor.executescript(delete_script)
        self.cursor.executescript(create_script)
        self.conn.commit()

        self.queue = queue.Queue()
        self.thread = threading.Thread(target=self._worker, daemon=True)
        self.thread.start()

    def _worker(self):
        while True:
            func, args, result_queue = self.queue.get()
            try:
                result = func(*args)
                result_queue.put(result)
            except Exception as e:
                result_queue.put(e)

    def _run_on_worker(self, func, *args):
        result_queue = queue.Queue()
        self.queue.put((func, args, result_queue))
        result = result_queue.get()
        if isinstance(result, Exception):
            raise result
        return result

    def _add(self, data: WeatherData):

        sql = insert_script.format(data.temperature, data.humidity, data.pressure, data.wind_speed, data.utc)
        self.cursor.executescript(sql)
        self.conn.commit()

    def _get_recent(self, n):
        sql = select_script.format(n)
        res = self.cursor.execute(sql)
        list = []
        for data in res:
            list.append(WeatherData(data[1], data[2], data[3], data[4], data[5]))

        return list

    def add(self, data: WeatherData):
        self._run_on_worker(self._add, data)

    def get_recent(self, n):
        return self._run_on_worker(self._get_recent, n)

    # For test purposes only
    def fill_with_bogus_data(self):
        for _ in range(100):
            self.curser.executescript(insert_bogus_script)