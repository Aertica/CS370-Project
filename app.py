from flask import Flask, render_template, jsonify
import sqlite3
from datetime import datetime
import os

app = Flask(__name__)
app.config['DATABASE'] = os.path.join(app.instance_path, 'weather.db')

def init_db():
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    with app.app_context():
        db = get_db()
        with app.open_resource('schema.sql') as f:
            db.executescript(f.read().decode(utf8))
        db.close()

def get_db():
    db = sqlite3.connect (
        app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
    )
    db.row_factory = sqlite3.Row
    return db

def close_db(e=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/')

def index():
    return render_template('index.html')

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0')