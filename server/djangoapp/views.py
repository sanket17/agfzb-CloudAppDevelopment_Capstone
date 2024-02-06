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

# Get an instance of a logger
logger = logging.getLogger(__name__)


# Create your views here.


# Create an `about` view to render a static about page
# def about(request):
# ...
def about(request):
    return render(request, 'djangoapp/about.html')


# Create a `contact` view to return a static contact page
def contact(request):
    return render(request,'djangoapp/contact.html')

# Create a `login_request` view to handle sign in request
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
        context = {}
        # url = "https://sankettikam1-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        # dealerships = get_dealers_from_cf(url)
        # context['dealerships'] = dealerships
        return render(request, 'djangoapp/index.html', context)

# Create a `get_dealer_details` view to render tdealershipshe reviews of a dealer
def get_dealer_details(request, dealer_id):
     if request.method == "GET":
        context = {}
        # Get dealers from the URL
        url = "https://sankettikam1-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
        dealer = get_dealer_by_id_from_cf(url, dealer_id)

        url = "https://sankettikam1-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/get"
        reviews = get_dealer_reviews_from_cf(url, dealer_id)
        context['reviews'] = reviews
        context['dealer'] = dealer
        return render(request, 'djangoapp/dealer_details.html', context)

        
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
        url = "https://sankettikam1-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/reviews/post"
        res = post_request(url, review)
        return redirect("djangoapp:dealer_details", dealer_id=dealer_id)
    url = "https://sankettikam1-8000.theiadockernext-1-labs-prod-theiak8s-4-tor01.proxy.cognitiveclass.ai/dealerships/get"
    dealer = get_dealer_by_id_from_cf(url, dealer_id)
    cars = CarModel.objects.all()
    return render(request, 'djangoapp/add_review.html', {"dealer": dealer, "cars": cars})