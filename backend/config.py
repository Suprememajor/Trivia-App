import os

SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database
DIALECT = "postgresql"
USER = "suprememajor"
PASSWORD = "12345678"
HOST = "localhost"
PORT = "5432"
DATABASE_NAME = "test6"
SQLALCHEMY_DATABASE_URI = f'{DIALECT}://{USER}:{PASSWORD}@{HOST}:{PORT}/{DATABASE_NAME}'
SQLALCHEMY_TRACK_MODIFICATIONS = False
