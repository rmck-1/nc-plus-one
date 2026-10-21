# NC Plus One

The NC Plus One REST API project is a backend events platform that allows users to register, browse events, RSVP, and manage their attendance.

## Step One - Database Setup:
Following the below steps will create the nc_plus_one database.

1. Navigate to project root folder: **nc-plus-one**
2. Run the following command: **psql -d postgres -f db/setup.sql**

## Step Two - .env creation:
Establishing the databse connection requires local database credentials. This is passed into **connections.py** via environmental variables. You need to create a new **.env** file with your credentials.

1. An **.env** file should be created with your local database credentials.
2. **.env.example** has been provided with the required variables to help.