# NC Plus One

The NC Plus One REST API project is a backend events platform that allows users to register, browse events, RSVP, and manage their attendance.

## Initial setup
Install the program dependencies via the **requirements.txt** file in a python virtual environment:
```
python -m venv.venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Step One - Database Setup:
Following the below steps will create the **nc_plus_one** database.

Navigate to project root folder: **nc-plus-one**

Run the following command: 
```
psql -d postgres -f db/setup.sql
```

## Step Two - .env creation:
Establishing the database connection requires local database credentials. This is passed into **connections.py** via environmental variables. You need to create a new **.env** file with your credentials.

1. An **.env** file should be created with your local database credentials.
2. **.env.example** has been provided with the required variables to help.

The structure looks like this:
```
PGDATABASE=
PGUSER=
PGPASSWORD=
PGHOST=
PGPORT=
```

## Step Three - seed the database tables
The database is comprised of four tables:
* Users
* Venues
* Events
* RSVPs

Sample data for the four database tables has been provided in **db/data** in json format.

To create the tables and seed the sample data run the following command from the project root:
```
python db/seed/seed.py
```