DROP TABLE IF EXISTS weather_data;
CREATE TABLE weather_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    temperature FLOAT,  -- from bme280 sensor
    humidity FLOAT,     -- from bme280 sensor
    pressure FLOAT,     -- from bme280 sensor
    wind_speed FLOAT,   -- from anemometer sensor
    notes TEXT          -- optional field for any funny business from sensors or weird data
);

CREATE INDEX idx_timestamp ON weather_data(timestamp);