from django.contrib.auth.views import LogoutView
from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'services', views.ServiceViewSet)
router.register(r'users', views.UserViewSet)
router.register(r'cars', views.CarViewSet)
router.register(r'reviews', views.ReviewViewSet)
router.register(r'rentals', views.RentalViewSet)
router.register(r'makes', views.MakeViewSet)
router.register(r'models', views.CarModelViewSet)
urlpatterns = [
    path('api/', include(router.urls)),
    path('', views.index, name = 'index'),
    path('api/reviews/create/<int:pk>', views.CreateReview.as_view(), name='create-review'),
    path('api/services/create/<int:pk>', views.CreateReview.as_view(), name='create-service'),
    # cars
    # path('cars/', views.CarList.as_view(), name='cars'),
    # path('cars/<int:pk>', views.CarDetail.as_view(), name='get-car'),
    # path('users/', views.UserList.as_view()),
    # path('users/<int:pk>', views.UserDetail.as_view(), name='user-detail'),
    # rentals(orders)
    # path('rentals/', views.RentalList.as_view()),
    # path('rentals/<int:pk>', views.RentalDetail.as_view(), name='rental-detail'),
    # path('services/', views.ServiceList.as_view()),
    # path('services/<int:pk>', views.ServiceDetail.as_view()),
    # path('services/create/<int:pk>', views.CreateService.as_view(), name='create-service'),
    # path('reviews/', views.ReviewList.as_view()),
    # path('reviews/<int:pk>', views.ReviewDetail.as_view()),
    # path('reviews/create/<int:pk>', views.CreateReview.as_view(), name='create-review'),
    # car make / model
    # path('makes/', views.MakeList.as_view()),
    # path('models/', views.CarModelList.as_view()),
    # path('makes/<int:pk>/', views.MakeDetail.as_view()),
    # path('models/<int:pk>/', views.CarModelDetail.as_view()),





    path('signup', views.UserSignUpView.as_view(), name='signup'),

    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]