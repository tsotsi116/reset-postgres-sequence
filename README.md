Reset Postgresql sequences
==========================

An easy way to reset all postgresql indexes in a database.

Script goes through all the tables in the specified database and resets them.

Found this useful after restoring from an sql file and couldn't insert data because the indexes.

Only tables with integer as a primary key are supported.

# Setting up

```sh
$ git clone https://github.com/tsotsi116/reset-postgres-sequence.git

```
# Create Python Virtual environment
```sh
$ python -m venv venv
```
# Activate the virtual environment
## Linux
```sh
source ./venv/bin/activate
```
## Windows
```powershell
.\venv\Scripts\activate
```


# Install dependencies
```sh
$ pip install -r requirements.txt
```

# Open  main.py with your text editor and modify lines 51 to 56
```py
if __name__ == "__main__":
    host = "localhost"
    port = 5432
    user = "demo"
    password = "demo"
    database_name = "db"
    schema = "public"
```

# Running the script
```sh
$ python main.py
```