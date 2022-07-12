from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from flask_app.models import user
from flask_app.models import contactform
from flask_app.models import newsletter
 
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


from flask_app import DATABASE


class Doggie:
    def __init__( self , data ):
        self.id = data['id']
        self.name = data['name']
        self.age = data['age']
        self.breed = data['breed']
        self.disability = data['disability']
        self.location = data['location']
        self.color = data['color']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.contactform = []
        # self.users = []


    @classmethod
    def create(cls, data:dict):
        query = "INSERT INTO doggies (name, breed, age, location, color, disability, created_at, updated_at, user_id) VALUES (%(name)s, %(breed)s, %(age)s, %(location)s, %(color)s, %(disability)s, NOW(), NOW(), %(user_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result


    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM doggies WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        if result:
            return cls(result[0])
        return False


    @classmethod
    def get_all(cls):
        query = "SELECT * FROM doggies;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            doggies = []
            for dog in results:
                doggies.append( cls(dog) )
            return doggies
        return []


    @classmethod
    def update(cls, data):
        query = "UPDATE doggies SET name=%(name)s,breed=%(breed)s,age=%(age)s,location=%(location)s,color=%(color)s,disability=%(disability)s,updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM doggies WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)



    @classmethod
    def get_one_user(cls,data):
        query = "SELECT * FROM doggies LEFT JOIN contactform ON doggies.id = contactform.doggie_id WHERE doggies.id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        print(result)
        dog = cls(result[0])
        if not result[0]['contactform.id'] == None:
            for row in result:
                contactform_data = {
                    'id': row['contactform.id'],
                    'first_name': row['first_name'],
                    'last_name': row['last_name'],
                    'email': row['email'],
                    'state': row['state'],
                    'question': row['question'],
                    'telephone': row['telephone'],
                    'doggie_id': row['doggie_id'],
                    'created_at': row['contactform.created_at'],
                    'updated_at': row['contactform.updated_at']
                }
                dog.contactform.append(contactform.Contactform(contactform_data))
        return dog


     # PASS IN VALIDATION FOR doggie create form
    @staticmethod
    def validate_doggie_info( dog ):
        is_valid = True
        if len(dog['name']) < 3:
            is_valid = False
            flash("Name must be at least 2 characters", 'err_users_name')
        if len(dog['breed']) < 2:
            is_valid = False
            flash("Please add breed, at least 2 characters!", 'err_users_breed')
            # add in the age val
        # if value=int(dog["age"] < 0):
        #     is_valid = False
        #     flash("Please put 0 if younger", 'err_users_age')
        if dog['location'] == '':
            is_valid = False
            flash("Location must be at least 2 characters!", 'err_users_location')
        if len(dog['color']) < 2:
            is_valid = False
            flash("Color must be at least 2 characters!", 'err_users_color')
        if len(dog['disability']) < 2:
            is_valid = False
            flash("Please add disability, it must be at least 2 characters!", 'err_users_dis')
        return is_valid
    


