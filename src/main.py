from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    data = {
        'temp': 1,
        'humidity': 1,
        'pressure': 1,
        'wind_speed': 1,
    }
    
    return render_template('index.html', data=data)

if __name__ == "__main__":
   app.run(debug=True)