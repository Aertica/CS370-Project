# CS370-Project

## Setting up your dev enviornment

Open a terminal and cd to the project root directory.

Create a virtual enviornment by running the command:

`python3 -m venv env`

Activate the virtual enviornment by running the command:

`env/Scripts/activate` (note, this path is for windows)

Install any project dependencies by running the command:

`pip install -r requirements.txt`

Add a package to your dev enviornment by running the command:

`pip install <package-name>`

Save any future dependencies you add by running the command:

`pip freeze > requirements.txt`

## Flask

### `/templates`

This is the directory where html files are stored.
In order to render html file from this directory use `render_template('<file-name>')`

### `/static`

This is the directory where css and javascript files are stored.

## Database

Connect to a database through `Database(file, overrride_existing)`, where `file` is the path to the database file, and `override_existing` specifies if it should connect to an existing database or create a new one with no data.

`Add(data)` inserts one row into the database. `get_recent(n)` gets the top n rows, when sorting by time.

### WeatherData

`self.temperature`: 

`self.humidity`: 

`self.pressure`: 

`self.wind_speed` :

`self.utc`: unix timestamp at the time the data was recorded (see [here](https://en.wikipedia.org/wiki/Unix_time))
