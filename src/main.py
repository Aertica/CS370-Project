from database import Database, WeatherData
from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    database = Database('test.db')
    data = database.get_recent(1)
    if len(data) == 0:
        data = WeatherData(0, 0, 0, 0, 0)
    else:
        data = data[0]
        
    return render_template('index.html', data=data.as_dict())

if __name__ == "__main__":
    database = Database('test.db', True)
    database.fill_with_bogus_data()

    app.run(debug=True)