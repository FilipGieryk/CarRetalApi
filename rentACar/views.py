from .serializers import RentalSerializer , CarListingSerializer, CarModelSerializer, MakeSerializer, UserSerializer, ReviewSerializer, ServiceSerializer
from .models import  Rental, CarListing, CarModel, Make, User, Review, Service
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from rest_framework.response import Response
from django.views.generic import CreateView
from rest_framework import serializers
from django.urls import reverse_lazy
from .forms import UserSignUpForm
from django.urls import reverse
import random


def index(request):
    return render(request, 'base.html')

    # cars CRUD

class CarList(generics.ListCreateAPIView):
    queryset = CarListing.objects.all()
    serializer_class = CarListingSerializer




class CarDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CarListingSerializer
    queryset = CarListing.objects.all()



# rentals(orders) CRUD

class RentalList(generics.ListCreateAPIView):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer


    def get_permissions(self):
        if self.request.user.is_staff:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Rental.objects.all()
        else:
            return Rental.objects.filter(rent_client=self.request.user)

    def perform_create(self, serializer):
        rent_start = serializer.validated_data['rent_start']
        rent_end = serializer.validated_data['rent_end']

        avaliable_cars = CarListing.objects.exclude(
            rental__rent_start__lte=rent_end,
            rental__rent_end__gte=rent_start,
        )
        if not avaliable_cars:
            raise serializers.ValidationError({'message': 'no avaliable cars for that date at the moment sorry:l'})

        chosen_car = random.choice(avaliable_cars)
        employee = random.choice(User.objects.filter(is_employee=True))


        serializer.save(rent_client=self.request.user,car_info=chosen_car, rent_employee=employee)


class RentalDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RentalSerializer

    def get_permissions(self):
        if self.request.user.is_staff:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Rental.objects.all()
        else:
            return Rental.objects.filter(rent_client=self.request.user)


# reviews

class CreateReview(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        rental = Rental.objects.get(pk=pk)
        serializer.save(rental=rental)



class ReviewList(generics.ListAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.request.user.is_staff:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        else:
            return Review.objects.filter(rental__rent_client=self.request.user)

class ReviewDetail(generics.RetrieveDestroyAPIView):
    serializer_class = ReviewSerializer


    def get_permissions(self):
        if self.request.user.is_staff:
            return [permissions.IsAdminUser()]
        else:
            return [permissions.IsAuthenticated()]

    def get_queryset(self):
        if self.request.user.is_staff:
            return Review.objects.all()
        else:
            return Review.objects.filter(rental__rent_client=self.request.user)


# service
class ServiceList(generics.ListCreateAPIView):
    queryset = Service.objects.all()
    serializer_class = ServiceSerializer

class ServiceDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = ServiceSerializer
    queryset = Service.objects.all()




class MakeList(generics.ListCreateAPIView):
    queryset = Make.objects.all()
    serializer_class = MakeSerializer

class CarModelList(generics.ListCreateAPIView):
    queryset = CarModel.objects.all()
    serializer_class = CarModelSerializer

# user CRUD

class UserList(generics.ListCreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = UserSerializer
    queryset = User.objects.all()


class ReviewCreateView(generics.CreateAPIView):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer












class UserSignUpView(CreateView):
    model = User
    form_class = UserSignUpForm
    template_name = 'signup.html'
    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'user'
        return super().get_context_data(**kwargs)
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('index')

class UserLoginView(LoginView):
    redirect_authenticated_user = True
    template_name = 'login.html'
    def get_success_url(self):
        return reverse_lazy('index')

#     def form_invalid(self, form):
#         messages.error(self.request,"invalid username or password")
#         return self.render_to_response(self.get_context.data(form=form))

