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


# <HINT> Create a plain Python class `DealerReview` to hold review data
