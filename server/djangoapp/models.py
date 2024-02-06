from django.db import models
from django.utils.timezone import now

class CarMake(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class CarModel(models.Model):
    TYPE_CHOICES = (("Sedan", "Sedan"), ("SUV", "SUV"), ("WAGON", "WAGON"))
    car = models.ForeignKey(CarMake, related_name="models", on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    dealer = models.IntegerField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    year = models.DateField()

    def __str__(self):
        return "{}-{}-{}".format(self.car.name, self.name, self.year)


# <HINT> Create a plain Python class `CarDealer` to hold dealer data
class CarDealer:
    def __init__(self, address, city, full_name, id, lat, long, short_name, st, zip):
        # Dealer address
        self.address = address
        # Dealer city
        self.city = city
        # Dealer Full Name
        self.full_name = full_name
        # Dealer id
        self.id = id
        # Location lat
        self.lat = lat
        # Location long
        self.long = long
        # Dealer short name
        self.short_name = short_name
        # Dealer state
        self.st = st
        # Dealer zip
        self.zip = zip

    def __str__(self):
        return "Dealer name: " + self.full_name


# <HINT> Create a plain Python class `DealerReview` to hold review data
class DealerReview:
    def __init__(self, dealership, name, purchase, id, review, purchase_date, car_make, car_model, car_year, sentiment):
        # DealerReview dealership
        self.dealership = dealership
        # DealerReview name
        self.name = name
        # DealerReview purchase
        self.purchase = purchase
        # DealerReview purchase_date
        self.purchase_date = purchase_date
        # DealerReview car_make
        self.car_make = car_make
        # DealerReview car_model
        self.car_model = car_model
        # DealerReview car_year
        self.car_year = car_year
        # DealerReview sentiment
        self.sentiment = sentiment
        # DealerReview id
        self.id = id
        # DealerReview review
        self.review = review

    def __str__(self):
        return "Dealer Reviewer name: " + self.name
