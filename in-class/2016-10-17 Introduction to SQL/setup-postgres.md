Postgres setup notes
====================

Follow these directions if you have already installed Postgres and Psycopg2. 


## Initial setup

You might need to add the Postgres binary directory to your `PATH`.  The Postgres binary directory (and how you add it to your `PATH`) varies among installations.

+ If you do not already have a postgres database user: `createuser -P postgres`
+ Create a database for the student registration app:  `createdb -U postgres registration`.
+ You might need to give the `postgres` user additional permissions:  Run `psql -U postgres registration`, then:
    - GRANT ALL PRIVILEGES ON DATABASE registration TO postgres;

## Creating the database schema

We have already set up the sample Django application to use the `registration` database and the `postgres` account with no password.  See `settings.py` for details.

You will still need to use `makemigrations` and `migrate` to create the database schema, and use `loaddata` to load the data we provided:

+ `python manage.py makemigrations sio`
+ `python manage.py migrate`
+ `python manage.py loaddata registration.json`

## Access the shell:

You should then be able to use the Postgres shell with `psql -U postgres registration`.  Postgres supports both SQL and internal Postgres-specific (non-SQL) commands.  Some useful Postgres commands:

+ `\list` lists all databases
+ `\dt` lists all tables in the current database
