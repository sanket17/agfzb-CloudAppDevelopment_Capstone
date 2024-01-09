from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
# from .models import related models
# from .restapis import related methods
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from datetime import datetime
import logging
import json

from .restapis import (get_dealers_from_cf, get_dealer_by_id_from_cf, 
get_dealer_reviews_from_cf, post_request)

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


def about(request):
    return render(request,'djangoapp/about.html')

def contact(request):
    return render(request,'djangoapp/contact.html')

def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['psw']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('djangoapp:index')
        else:
            context['message'] = "Invalid username or password."
            return render(request, 'djangoapp/login.html', context)
    else:
        return render(request, 'djangoapp/login.html', context)

def logout_request(request):
    logout(request)
    return redirect('djangoapp:index')

def registration_request(request):
    context = {}
    if request.method == 'GET':
        return render(request, 'djangoapp/registration.html', context)
    elif request.method == 'POST':
        # Check if user exists
        username = request.POST['username']
        password = request.POST['psw']
        first_name = request.POST['firstname']
        last_name = request.POST['lastname']
        user_exist = False
        try:
            User.objects.get(username=username)
            user_exist = True
        except:
            logger.error("New user")
        if not user_exist:
            user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                            password=password)
            login(request, user)
            return redirect("djangoapp:index")
        else:
            context['message'] = "User already exists."
            return render(request, 'djangoapp/registration.html', context)

# Update the `get_dealerships` view to render the index page with a list of dealerships
def get_dealerships(request):
    if request.method == "GET":
        url = "https://kundansable-3000.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # Get dealers from the URL
        dealerships = get_dealers_from_cf(url)
        # Concat all dealer's short name
        dealer_names = ' '.join([dealer.short_name for dealer in dealerships])
        # Return a list of dealer short name
        return HttpResponse(dealer_names)

# Create a `get_dealer_details` view to render tdealershipshe reviews of a dealer
def get_dealer_details(request, dealer_id):
     if request.method == "GET":
        url = "https://kundansable-3002.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/get"
        # Get dealers from the URL
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        # # Concat all dealer's short name
        results = ' '.join(["{}-{}".format(review.name, review.sentiment) for review in reviews])
        # Return a list of review short name
        return HttpResponse(results)

        
# Create a `add_review` view to submit a review
def add_review(request, dealer_id):
    if request.method == "POST":
        review = dict()
        review["time"] = datetime.utcnow().isoformat()
        review["dealership"] = dealer_id
        review["review"] = request.POST.get('review', '')
        review["purchase"] = request.POST.get('purchase', '')
        review["purchase_date"] = request.POST.get('purchase_date')
        review["name"] = request.POST.get('name', '')
        review["car_make"] = request.POST.get('car_make')
        review["car_model"] = request.POST.get('car_model')
        review["car_year"] = request.POST.get('car_year')
        url = "https://kundansable-3004.theiadockernext-0-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/post"
        res = post_request(url, review)
    return render(request, 'djangoapp/add_review.html', {"dealer_id": dealer_id})
