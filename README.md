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

`pip freeze -r requirements.txt`

## Flask

### `/templates`

This is the directory where html files are stored.
In order to render html file from this directory use `render_template(<file-name>)`

### `/static`

This is the directory where css and javascript files are stored.