from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
import re	# the regex module
from flask_app.models import doggie

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DATABASE = 'RoyalDoggie_mydb'

class Contactform:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name= data['last_name']
        self.email = data['email']
        self.state = data['state']
        self.question = data['question']
        self.telephone = data['telephone']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.doggie_id = data['doggie_id']
        self.doggies = []


    
    @classmethod
    def create_contact(cls, data:dict):
        query = "INSERT INTO contactform (first_name, last_name, email, telephone, state, question, created_at, updated_at, doggie_id) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(telephone)s, %(state)s, %(question)s, NOW(), NOW(), %(doggie_id)s);"
        result = connectToMySQL(DATABASE).query_db(query, data)
        return result

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM contactform WHERE id = %(id)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        return cls(result[0])

  
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM contactform;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            contactform = []
            for contact in results:
                contactform.append( cls(contact) )
            return contactform
        return False
        

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM contactform WHERE email = %(email)s;"
        result = connectToMySQL(DATABASE).query_db(query,data)
        # Didn't find a matching contact
        if len(result) < 1:
            return False
        return cls(result[0])  

    @staticmethod
    def validate_contact_info( contact ):
        is_valid = True
        if not EMAIL_REGEX.match(contact['email']): 
            flash("Invalid email address!", "err_contactform_email")
            is_valid = False
        else:
            query = "SELECT * FROM users WHERE email = %(email)s;"
            results = connectToMySQL(DATABASE).query_db(query,contact)
            if len(results) >= 1:
                flash("Email already taken.", "err_contactform_email")
                is_valid=False 
        
        if len(contact['first_name']) < 2:
            is_valid = False
            flash("Name must be at least 2 characters!",'err_contactform_first_name')
        if len(contact['last_name']) < 2:
            is_valid = False
            flash("I told you at least 2 characters!", 'err_contactform_last_name')
        if len(contact['telephone']) < 10:
            is_valid = False
            flash("Need valid number", 'err_contactform_telephone')
        if contact['state'] != 2:
            flash("Please choose a state", 'err_contactform_state')
        if contact['question'] == '':
            is_valid = False
            flash("Please ask a question or simply tell us about you", 'err_contactform_question')
        return is_valid

    @classmethod
    def get_all_contact(cls):
        query = "SELECT * FROM contactform JOIN doggies ON contactform.doggie_id = doggies.id;"
        results = connectToMySQL(DATABASE).query_db(query)
        print(results)
        if results:
            contactform = []
            for contact in results:
                contact_actual = cls(contact)
                data = {
                    'id': contact['doggie_id'],
                    'created_at': contact['doggies.created_at'],
                    'updated_at': contact['doggies.updated_at'],
                    'name': contact['name'],
                    'breed': contact['breed'],
                    'age': contact['age'],
                    'location': contact['location'],
                    'color': contact['color'],
                    'disabilities': contact['disabilities']    
                }
                potentialfamily = doggie.Doggie(data)
                contact_actual.potentialfamily = potentialfamily

                contactform.append(contact_actual)
            return contactform
        return []


    # @classmethod
    # def get_one_contact(cls,data):
    #     query = "SELECT * FROM contactform JOIN doggies ON contactform.doggie_id = doggies.id WHERE contactform.id = %(id)s;"
    #     result = connectToMySQL(DATABASE).query_db(query,data)
    #     print(result)
    #     contact = cls(result[0])
    #     if not result[0]['doggies.id'] == None:
    #         for row in result:
    #             doggie_data = {
    #                 'id': row['doggies.id'],
    #                 'name': row['name'],
    #                 'breed': row['breed'],
    #                 'age': row['age'],
    #                 'location': row['location'],
    #                 'color': row['color'],
    #                 'disabilities': row['disabilities'],
    #                 'doggie_id': row['doggie_id'],
    #                 'created_at': row['contactform.created_at'],
    #                 'updated_at': row['contactform.updated_at']
    #             }

    #             contact.doggie = doggie.Doggie(doggie_data)
    #     return contact




