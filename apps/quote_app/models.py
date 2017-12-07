# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from ..login_app.models import User

#from datetime import date 

from django.db import models

class QuoteManager(models.Manager):
    
    def validate(self, postData):
        results = {'status': True, 'errors':[]}
        if len (postData ['quoted_by']) < 4:
            results['errors'].append('Quoted by must contain more than 3 characters')
            results['status'] = False
        if len (postData ['quote_message']) < 11:
            results['errors'].append('Message must contain more than 10 characters')
            results['status'] = False  
        
        return results



    def creator(self, postData, user_id):
        people = User.objects.get(id=user_id)

        quote = self.create(quoted_by = postData['quoted_by'], quote_message = postData['quote_message'], posted_by = people)

        #quote.quote_favoriter.add(people)

        return quote
        

class Quote(models.Model):
    quoted_by = models.CharField(max_length=255)
    quote_message = models.TextField()
    posted_by = models.ForeignKey(User, related_name="posted_quote")
    quote_favoriter = models.ManyToManyField(User, related_name="favorited_quote")
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    def __repr__(self):
        return "<Quote object: {} {} {} {}>".format(self.destination, self.travel_start, self.travel_end, self.description)

    objects = QuoteManager()


    #tripcreator is going through the user object and defining the added_trip foreign key to get the trip id
    #tripcreator = User.objects.get(added_trip = Trip.objects.get(id=trip_id))
    

    #quotecreator = User.objects.get(posted_quote = Quote.objects.get(id=posted_by))