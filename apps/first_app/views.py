# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect 

# Create your views here.

from models import Users, Quotes, Favorites
from django.db.models import Count
from django.contrib import messages
import bcrypt
import re 
from datetime import date, datetime, timedelta
import random

# Create your views here.

def index(request):
    quotes = Quotes.objects.all()
    print quotes.count()
    if(len(quotes) > 1):
        randomQuote = random.randint(1, quotes.count())
        print randomQuote
        context = {
        "dailyQuote" : quotes.all()[randomQuote].content
        }
        return render(request, 'first_app/index.html', context)
    else:
        context = {
            "dailyQuote" : "Register to become the next great quote sharer!"
        }
        return render(request, 'first_app/index.html', context)

def register(request):

    user = Users.usersManager.add(request.POST['first_name'], request.POST['last_name'], request.POST['email'], request.POST['password'], request.POST['confirm'], request.POST['birthday'])

    if user[0] == False:
        for message in user[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
    else:
        request.session['user_id'] = user[1].id 
        print "successful registration"
        return redirect('/success')

def login(request):

    user = Users.usersManager.login(request.POST['email'], request.POST['password'])

    if user[0] == False:
        for message in user[1]:
            messages.add_message(request, messages.ERROR, message)
        return redirect('/')
    else:
        request.session['user_id'] = user[1].id
        return redirect('/success')


def success(request):

    user = Users.usersManager.get(id=request.session['user_id'])
    quotes = Quotes.objects.all()
    userquotes = Favorites.objects.filter(user_id=request.session['user_id'])

    for userquote in userquotes:
        quotes = quotes.exclude(id=userquote.quote_id)

    context = {
        "user" : user,
        "quotes" : quotes,
        "userquotes" : userquotes    
    }

    return render(request, 'first_app/success.html', context)

def addquote(request):

    name = request.POST['name']
    content = request.POST['content']
    user = Users.usersManager.get(id=request.session['user_id'])

    quote = Quotes.quotesManager.add(name,content,user)

    if quote[0] == False:
        for message in quote[1]:
            messages.add_message(request,messages.ERROR,message)
        return redirect('/success')
    else:
        return redirect('/success')

def logout(request):
    request.session.clear()
    return redirect('/')

def dashboard(request):
    return redirect('/success')

def favorite(request, quote_id):

    favorites = Favorites.objects.filter(user_id = request.session['user_id']).filter(quote_id=quote_id)

    if len(favorites) == 0:
        user = Users.usersManager.get(id=request.session['user_id'])
        quote = Quotes.objects.get(id=quote_id)

        favorite = Favorites.objects.create(user=user,quote=quote)
        print "Successfully added to your list"
        return redirect('/success')
    
    else:
        print "Did not add to you list"
        return redirect('/success')

def remove(request, quote_id):

    check = Favorites.objects.filter(quote_id=quote_id)
    check.delete()

    print"remove from favorite"
    return redirect('/success')

def userpage(request, id):

    user = Users.usersManager.get(id=id)
    counter = Users.usersManager.all().annotate(counter=Count('quotecreator'))
    quotes = Quotes.objects.all()
    

    context = {
        "user" : user, 
        "quotes" : quotes,
        "counter" : counter
    }
    return render(request, 'first_app/userpage.html', context)