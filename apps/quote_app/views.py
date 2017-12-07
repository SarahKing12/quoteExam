# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import HttpResponse, redirect, render 
from ..login_app.models import User 
from .models import Quote
from django.contrib import messages

#route: '/quotes'          main quote page
def quotes(request):
    user = User.objects.get(id=request.session['user'])
    # user from (other_traveler=user) is the user from above: user = User.objects.get(id=request.session['user'])
    #allquotes = Quote.objects.filter(quote_favoriter=user) 
    allquotes = Quote.objects.exclude(quote_favoriter=user)    
    favoritequotes = Quote.objects.filter(quote_favoriter=user)

    context = {
        'user': user,
        'allquotes': allquotes,
        'favoritequotes': favoritequotes,
    }
    return render(request, 'quote_app/quotes.html', context)


#route: '/quotes/create'   route that adds a quote to DB
def create(request):
    results = Quote.objects.validate(request.POST)
    if results['status'] == True:
        quote = Quote.objects.creator(request.POST, request.session['user'])
        return redirect('/quotes')
    else:
        for error in results['errors']:
            messages.error(request, error)
        return redirect('/quotes')

#route: '/quotes/favorite'   route that moves a quote to the logged in users' favorite list when Add to My List is selected
def favorite(request, quote_id):
    thisquote = Quote.objects.get(id=quote_id)
    thisuser = User.objects.get(id=request.session['user'])
    thisquote.quote_favoriter.add(thisuser)
    return redirect('/quotes')

#route: '/quotes/favorite'   route that removes a quote from a logged in users' favorite list when Remove from My List is selected
def remove(request, quote_id):
    thisquote = Quote.objects.get(id=quote_id)
    thisuser = User.objects.get(id=request.session['user'])
    thisquote.quote_favoriter.remove(thisuser)
    return redirect('/quotes')

#route: '/quotes/users/user_id'      main users' page
def users(request, user_id):
    user = User.objects.get(id=user_id)
    postedquotes = Quote.objects.filter(id=user_id)
    #postedquotes = Quote.objects.filter(posted_by_id=user)
    #quotecreator = User.objects.get(posted_quote = Quote.objects.get(id=posted_by_id))
    context = {
        'postedquote': Quote.objects.get(id=user_id),
        'user': user,
        'postedquotes': postedquotes,
    } 
    return render(request, 'quote_app/users.html', context)

#route: '/quotes/logout'     logout button that logs you out and takes you back to login page
def logout(request):
    request.session.flush()
    return redirect ('/main')
