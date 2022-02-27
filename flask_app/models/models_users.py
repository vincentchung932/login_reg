# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
# model the class after the friend table from our database
import re
from flask import flash


Database = 'users'
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 
class Users:
    def __init__( self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    
    
    
    @classmethod
    def add(cls,data):
        query = "INSERT INTO users (first_name,last_name,email,password) VALUES ( %(first_name)s,%(last_name)s,%(email)s,%(password)s);"    
        return connectToMySQL(Database).query_db(query,data)
    
    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(Database).query_db(query)
        all_users = []
        for one_user in results:
            all_users.append( cls(one_user) )
        
        if results:
            return all_users
        else:
            return []
        
    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(Database).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return []

    @classmethod
    def get_by_mail(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(Database).query_db(query,data)
        if results:
            return cls(results[0])
        else:
            return [] 
        
    
    @staticmethod
    def validate(new):
        is_valid = True # we assume this is true
        all_email = Users.get_all()
        email_name = []
        for one_email in all_email:
            email_name.append(one_email.email)
        if len(new['first_name'])<3:
            flash("First name must be at least 3 char!",'reg_error')
            is_valid = False
        
        if len(new['last_name'])<3:
            flash("Last name must be at least 3 char!",'reg_error')
            is_valid = False
        
        if not EMAIL_REGEX.match(new['email']):
            flash("Invalid email address!",'reg_error')
            is_valid = False
        if new['email'] in email_name:
            flash("This email address is already exsit",'reg_error')
            is_valid = False
        
        if len(new['password'])<8:
            flash("password must be at least 8 char!",'reg_error')
            is_valid = False
        
        if new['password'] != new['confirm_password']:
            flash("Password should be the same!",'reg_error')
            is_valid = False
        return is_valid
    
    
