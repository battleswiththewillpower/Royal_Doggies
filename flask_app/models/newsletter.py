from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from flask_app.models import doggie

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DATABASE = 'RoyalDoggie_mydb'

class Newsletter:
    def __init__( self , data ):
        self.id = data['id']
        self.email = data['email']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.doggie_id = data['doggie_id']


    @classmethod
    def create_newsletter(cls, data:dict):
        query = "INSERT INTO newsletter (email, created_at, updated_at, doggie_id) VALUES (%(email)s, NOW(), NOW(), %(doggie_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM newsletter WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM newsletter;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            newsletter = []
            for eachcontact in results:
                newsletter.append( cls(eachcontact) )
            return newsletter
        return False


    @staticmethod
    def validate_newsletter( user ):
        is_valid = True
        if not EMAIL_REGEX.match(user['email']): 
            flash("Invalid email address!", 'err_email')
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query,user)
            if len(results) >= 1:
                flash("Email already taken.", 'err_email')
                is_valid=False 
