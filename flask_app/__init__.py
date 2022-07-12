# __init__.py
from flask import Flask
app = Flask(__name__)
app.secret_key = "Take care of the babies"

DATABASE = 'RoyalDoggie_mydb'