from __future__ import unicode_literals

from django.db import models
from datetime import date, datetime, timedelta

import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

import bcrypt

# Create your models here.

class UsersManager(models.Manager):
    def add(self,first_name,last_name,email,password,confirm,birthday):

        messages = []

        if len(first_name) < 1:
            messages.append('You must enter your First Name to register')
        if not first_name.isalpha():
            messages.append('First Name must contain letters only')
        if len(last_name) < 1:
            messages.append('You must enter your Last Name to register')
        if not last_name.isalpha():
            messages.append('Last Name must contain letters only')
        if len(email) < 1:
            messages.append('You must enter an email to Register')
        if not EMAIL_REGEX.match(email):
            messages.append('Email must be in a valid format to Register')
        if len(email) > 1:
            check = Users.usersManager.filter(email=email)
            if len(check) > 0:
                messages.append('The email you have entered is already registered')
        if len(password) < 1:
            messages.append('You must enter a password to Register')
        if len(password) < 8:
            messages.append('Password must be atleast 8 characters long')
        if password != confirm:
            messages.append('Password and Password Confirmation do not match')
        
        try:
            birthdate = datetime.strptime(birthday, '%Y-%m-%d')
            print birthday
            print birthdate
            if datetime.now() < datetime.strptime(birthday, '%Y-%m-%d'):
                messages.append("Birthday must be before today's date")
        except:
            messages.append('Not a Valid Date of Birth')
        

        if len(messages) > 0:
            return False, messages
        
        else:

            pw_hash = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt())

            user = Users.usersManager.create(first_name=first_name,last_name=last_name,email=email,password=pw_hash,birthday=birthday)
            return True, user

    
    def login(self,email,password):
         
        messages = []

        user = Users.usersManager.filter(email=email)

        if len(email) == 0:
            messages.append('You must enter an email to login')
        if not EMAIL_REGEX.match(email):
            messages.append('Email format entered is invalid')
        if len(user) < 1:
            messages.append('User does not exist, please register')
            return False, messages
        
        realpassword = user[0].password
        print realpassword
        hash_check = bcrypt.hashpw(password.encode(),realpassword.encode())
        
        if len(realpassword) < 1:
            messages.append('Please enter a password')
        if realpassword != hash_check:
            messages.append('Password entered does not match')

        if len(messages) > 0:
            return False, messages
        
        else:
            return True, user[0]


class Users(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    password = models.CharField(max_length=50)
    birthday = models.DateField('%m/%d/%Y')
    usersManager = UsersManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class QuotesManager(models.Model):
    def add(self,name,content,user):

        messages = []

        if len(name) < 3 :
            messages.append("Must be longer than 3 characters")
            
        if len(content) < 10:
            messages.append("Quote must be longer than 10 characters!")
        
        if len(messages) > 0:
            return False, messages
        
        else:
            quote = Quotes.objects.create(name=name,content=content,user=user)
            return True, quote

class Quotes(models.Model):
    name = models.CharField(max_length=100)
    content = models.CharField(max_length=250)
    user = models.ForeignKey(Users, related_name="quotecreator")
    quotesManager = QuotesManager()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Favorites(models.Model):
    user = models.ForeignKey(Users, related_name="favorites")
    quote = models.ForeignKey(Quotes, related_name="favorites")