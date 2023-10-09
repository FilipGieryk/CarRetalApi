from .models import Rental, CarListing, CarModel, Make, User, Review, Service
from rest_framework import serializers
from django.db.models import Avg


        





class CarModelSerializer(serializers.ModelSerializer):

    make = serializers.SlugRelatedField(queryset=Make.objects.all(), slug_field='make')
    class Meta:
        model = CarModel
        fields = ['make', 'model']

class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields ='__all__'






    
  

class ReviewSerializer(serializers.ModelSerializer):
    rental = serializers.HyperlinkedRelatedField(
        view_name='rental-detail',
        read_only=True
    )
    rental_client = serializers.ReadOnlyField(source='rental.rent_client.username')
    rental_employee = serializers.ReadOnlyField(source='rental.rent_employee.username')

    class Meta:
        model = Review
        fields ='__all__'

  
class RentalSerializer(serializers.ModelSerializer):
    

    car_info = serializers.SlugRelatedField(read_only=True, slug_field='registration_plate')
    price = serializers.ReadOnlyField()
    rent_client = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    rent_employee = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    create_review_url = serializers.HyperlinkedIdentityField(
        view_name='create-review',
        lookup_field='pk'  
    )
    reviews = ReviewSerializer(read_only=True)
    class Meta:
        model = Rental
        fields ="__all__"

    def to_representation(self,instance):
        data = super().to_representation(instance)
        if data['reviews']:
            data.pop('create_review_url', None)
        return data





class UserSerializer(serializers.ModelSerializer):
    rating = serializers.SerializerMethodField(read_only=True)

    def get_rating(self, obj):
        reviews_given = Review.objects.filter(rental__rent_employee=obj)
        if reviews_given:
            avg_rating = reviews_given.aggregate(Avg('rating'))['rating__avg']
            return avg_rating
        else:
            return None

    class Meta:
        model = User
        fields = ['id','username','first_name','last_name','email','balance','is_employee','rating']

class UserDetailSerializer(serializers.ModelSerializer):
    reviews_made = serializers.SerializerMethodField(read_only=True)
    reviews_given = serializers.SerializerMethodField(read_only=True)
    rentals_made = RentalSerializer(read_only=True, many=True, source='client_rent')
    rentals_given = RentalSerializer(read_only=True, many=True, source='employee_rent')
    rating = serializers.SerializerMethodField(read_only=True)
    def get_reviews_made(self, obj):
        request = self.context.get('request')
        reviews_given = Review.objects.filter(rental__rent_client=obj)
        serializer = ReviewSerializer(reviews_given, many=True, context = {'request':request})
        return serializer.data

    def get_reviews_given(self, obj):
        request = self.context.get('request')
        reviews_given = Review.objects.filter(rental__rent_employee=obj)
        serializer = ReviewSerializer(reviews_given, many=True, context = {'request':request})
        return serializer.data
    def get_rating(self, obj):
        reviews_given = Review.objects.filter(rental__rent_employee=obj)
        if reviews_given:
            avg_rating = reviews_given.aggregate(Avg('rating'))['rating__avg']
            return avg_rating
        else:
            return None
    def to_representation(self,instance):
        data = super().to_representation(instance)
        if data['is_employee'] == False:
            data.pop('rating', None)
            data.pop('reviews_given', None)
            data.pop('rentals_given', None)
        return data
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','balance','is_employee','rating','rentals_made','reviews_made','rentals_given','reviews_given']


class ServiceSerializer(serializers.ModelSerializer):
    damaged_car = serializers.SlugRelatedField(read_only=True, slug_field='registration_plate')
    guilty = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field=('username'))
    

    class Meta:
        model = Service
        fields ='__all__'


        
class CarListingSerializer(serializers.ModelSerializer):
    car_model = serializers.SlugRelatedField(queryset=CarModel.objects.all(), slug_field='model')


    class Meta:
        model = CarListing
        fields = ['car_model', 'registration_plate','basic_price','production_year']



class CarListingDetailSerializer(serializers.ModelSerializer):
    car_model = serializers.SlugRelatedField(queryset=CarModel.objects.all(), slug_field='model')
    services = ServiceSerializer(many=True, read_only=True)
    rental = RentalSerializer(many=True, read_only=True)
    create_service_url = serializers.HyperlinkedIdentityField(
        view_name='create-service',
        lookup_field='pk',
        read_only=True
    )
    class Meta:
        model = CarListing  
        fields = "__all__"


 


        
