from django.shortcuts import render
from car.models import Car, CarItem
# Create your views here.
def car_detail(request, user):
    if request.method == 'POST':
        if request.user.is_authenticated:

            #Create car model for User
            try:
                validate_car = Car.objects.filter(user = user)

                if validate_car:
                    

            except Exception as e:
                pass

        else:
            pass