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




class RentalSerializer(serializers.ModelSerializer):
    
    # rent_employee = serializers.SlugRelatedField(read_only=True, slug_field='username')
    car_info = serializers.SlugRelatedField(read_only=True, slug_field='registration_plate')
    price = serializers.ReadOnlyField()
    rent_client = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    rent_client_slug = serializers.SlugRelatedField(slug_field='username', read_only=True, source='rent_client')
    rent_employee = serializers.HyperlinkedRelatedField(
        view_name='user-detail',
        read_only=True
    )
    rent_employee_slug = serializers.SlugRelatedField(slug_field='username', read_only=True, source='rent_employee')
    create_review_url = serializers.HyperlinkedIdentityField(
        view_name='create-review',
        lookup_field='pk'  
    )
    class Meta:
        model = Rental
        fields ="__all__"

    def to_representation(self,instance):
        if instance.rent_employee.is_employee:
            return super().to_representation(instance)
        return None

    def get_queryset(self):
        return User.objects.filter(is_employee=True)


    def create(self, validated_data):
        current_user = self.context['request'].user

        validated_data['rent_client'] = current_user
    
        return Rental.objects.create(**validated_data)


    
  

class ReviewSerializer(serializers.ModelSerializer):
    rental = serializers.HyperlinkedRelatedField(
        view_name='rental-detail',
        read_only=True
    )
    rental_client = serializers.SerializerMethodField(read_only=True)
    rental_employee = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Review
        fields ='__all__'
    def get_rental_client(self, obj):
        return obj.rental.rent_client.username
    
    def get_rental_employee(self, obj):
        return obj.rental.rent_employee.username
  
  

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
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email','balance','is_employee','rentals_made','rating','rentals_given','reviews_made','reviews_given']


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
    services = serializers.SerializerMethodField()
    rental = serializers.SerializerMethodField()
    create_service_url = serializers.HyperlinkedIdentityField(
        view_name='create-service',
        lookup_field='pk'  
    )
    class Meta:
        model = CarListing  
        fields = "__all__"

    def get_rental(self, obj):
        request = self.context.get('request')
        rental_data = Rental.objects.filter(car_info=obj.id)
        rental_serializer = RentalSerializer(rental_data, many=True, context={'request': request})
        return rental_serializer.data


    def get_services(self,obj):
        request = self.context.get('request')
        service_data = Service.objects.filter(damaged_car=obj.id)
        service_serializer = ServiceSerializer(service_data, many=True, context={'request': request})
        return service_serializer.data

 


        
