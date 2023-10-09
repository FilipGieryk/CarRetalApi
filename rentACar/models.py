from django.core.validators import MinValueValidator, MaxValueValidator, ValidationError
from django.contrib.auth.models import AbstractUser
from datetime import timedelta
from datetime import datetime
from django.db import models

class Make(models.Model):
    make = models.CharField('Make', max_length=150, unique = True)

    def __str__(self):
        return self.make


class CarModel(models.Model):
    make = models.ForeignKey(Make, on_delete = models.CASCADE, related_name='models')
    model = models.CharField('Model', max_length=150, unique = True)

    def __str__(self):
        return f'{self.make} {self.model}'


class CarListing(models.Model):
    car_model = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car')
    registration_plate = models.CharField(max_length=10, unique = True)
    mileage = models.IntegerField(default = 0)
    fuel = models.IntegerField(
        validators = [
            MaxValueValidator(100),
            MinValueValidator(1)
        ],
        default = 100
    )
    basic_price = models.FloatField()
    production_year = models.IntegerField(
        validators = [
            MaxValueValidator(datetime.now().year + 1)
        ]
    )

    def __str__(self):
        return self.registration_plate



class User(AbstractUser):
    is_employee = models.BooleanField(default = False)
    balance = models.FloatField(default = 0)
    mobile = models.CharField(max_length=15, blank=True)



    def __str__(self):
        return f'{self.first_name} {self.last_name}'









class Rental(models.Model):
    rent_client = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'client_rent')
    rent_employee = models.ForeignKey(User, on_delete = models.CASCADE, related_name = 'employee_rent')
    car_info = models.ForeignKey(CarListing, on_delete = models.CASCADE, related_name='rental')
    price = models.FloatField()
    rent_start = models.DateField()
    rent_end = models.DateField()



    def save(self, *args, **kwargs):
        days_count = (self.rent_end - self.rent_start) // timedelta(days=1)
        basic_price = self.car_info.basic_price
        self.price = days_count * basic_price
        super(Rental, self).save(*args, **kwargs)


    def __str__(self):
        return f'{self.rent_client.first_name} {self.rent_client.last_name} - {self.car_info.registration_plate}'

    def clean(self):
        if self.rent_start > self.rent_end:
            raise ValidationError('start date cannot be bigger than end date')

class Review(models.Model):
    rental = models.OneToOneField('Rental', on_delete=models.CASCADE, related_name = 'reviews')
    comment = models.CharField(max_length=999)
    rating = models.IntegerField(
        validators = [
            MaxValueValidator(5),
            MinValueValidator(1)
        ],
    )

class Service(models.Model):
    damage = models.CharField(max_length=299)
    damaged_car = models.ForeignKey(CarListing, on_delete = models.CASCADE, related_name='services')
    guilty = models.ForeignKey(User, on_delete = models.CASCADE, blank = True) 
    is_done = models.BooleanField(default=False)