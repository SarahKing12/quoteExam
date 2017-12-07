# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re, bcrypt  ##import Regular Expressions for email validation

# Create your models here.

class UserManager(models.Manager):

    def validate(self, postData):
        results = {'status': True, 'errors':[]}
        ##########Validation for name
        if len (postData ['name']) < 2:
            results['errors'].append('Your name is too short.')
            results['status'] = False
        ##########Validating name only contains characters
        if not re.match("[A-Za-z]", postData['name']):
            results['errors'].append('Name must only contain characters.')
            results['status'] = False
        ##########Validation for username
        if len (postData ['alias']) < 2:
            results['errors'].append('Your alias is too short.')
            results['status'] = False
        ##########Validating username only contains characters
        if not re.match("[A-Za-z]", postData['alias']):
            results['errors'].append('Alias must only contain characters.')
            results['status'] = False
        ##########Validation for email        
        if not re.match("[^@]+@[^@]+\.[^@]+", postData['email']):
            results['errors'].append('Email is not valid.')
            results['status'] = False
        ##########Validation for password equals password confirmation
        if postData['pw'] != postData['pwcon']:
            results['errors'].append('Passwords do not match.')
            results['status'] = False 
        ##########Validation length of password
        if len(postData['pw']) < 5:
            results['errors'].append('Password needs to be 5 characters long at least.')
            results['status'] = False
        ##########Validating if email already exists in database 
        if len(self.filter(email = postData ['email'])) > 0:
            results['errors'].append('User already exists.')
            results['status'] = False
        return results
        ##########Validating if email already exists in database 
        if len(postData['birthday']) < 8:
            results['errors'].append('Please enter your birthday.')
            results['status'] = False
        return results

        ##########Putting new form data in database
    def creator(self, postData):
        user = self.create(name = postData['name'], alias = postData['alias'], email = postData['email'], password = bcrypt.hashpw(postData['pw'].encode(), bcrypt.gensalt()), birthday = postData['birthday'])
        return user

        ##########Checking login info to see if user exsists
    def loginVal(self, postData):
        results = {'status': True, 'errors':[], 'user': None}
        users = self.filter(email = postData['email'])

        if len(users) < 1:
            results['status'] = False
        else:
            if bcrypt.checkpw(postData['pw'].encode(), users[0].password.encode()):
                results['user'] = users[0]
            else:
                results['status'] = False 
        return results


class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    birthday = models.DateField(auto_now=False, auto_now_add=False)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<User object: {} {} {} {} {}>".format(self.name, self.alias, self.email, self.password, self.birthday,)

    objects = UserManager()