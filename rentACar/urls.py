from django.contrib.auth.views import LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name = 'index'),
    # cars
    path('cars/', views.CarList.as_view(), name='cars'),
    path('cars/<int:pk>', views.CarDetail.as_view()),
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>', views.UserDetail.as_view()),
    # rentals(orders)
    path('rentals/', views.RentalList.as_view()),
    path('rentals/<int:pk>', views.RentalDetail.as_view()),
    path('services/', views.ServiceList.as_view()),
    path('services/<int:pk>', views.ServiceDetail.as_view()),
    path('reviews/', views.ReviewList.as_view()),
    path('reviews/<int:pk>', views.ReviewDetail.as_view()),
    path('reviews/create/<int:pk>', views.CreateReview.as_view(), name='create-review'),
    # car make / model
    path('makes/', views.MakeList.as_view()),
    path('models/', views.CarModelList.as_view()),





    path('signup', views.UserSignUpView.as_view(), name='signup'),,

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]