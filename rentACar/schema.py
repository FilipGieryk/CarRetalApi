import graphene
from graphene_django.types import DjangoObjectType
from .models import Make, CarModel, CarListing, User, Rental, Review, Service

class MakeType(DjangoObjectType):
    class Meta:
        model = Make

class CarModelType(DjangoObjectType):
    class Meta:
        model = CarModel

class CarListingType(DjangoObjectType):
    class Meta:
        model = CarListing

class UserType(DjangoObjectType):
    class Meta:
        model = User

class RentalType(DjangoObjectType):
    class Meta:
        model = Rental

class ReviewType(DjangoObjectType):
    class Meta:
        model = Review

class ServiceType(DjangoObjectType):
    class Meta:
        model = Service

class Query(graphene.ObjectType):
    # Add queries for each model if needed
    all_makes = graphene.List(MakeType)
    all_car_models = graphene.List(CarModelType)
    all_car_listings = graphene.List(CarListingType)
    all_users = graphene.List(UserType)
    all_rentals = graphene.List(RentalType)
    all_reviews = graphene.List(ReviewType)
    all_services = graphene.List(ServiceType)

    def resolve_all_makes(self, info):
        return Make.objects.all()

    def resolve_all_car_models(self, info):
        return CarModel.objects.all()

    def resolve_all_car_listings(self, info):
        return CarListing.objects.all()

    def resolve_all_users(self, info):
        return User.objects.all()

    def resolve_all_rentals(self, info):
        return Rental.objects.all()

    def resolve_all_reviews(self, info):
        return Review.objects.all()

    def resolve_all_services(self, info):
        return Service.objects.all()

schema = graphene.Schema(query=Query)