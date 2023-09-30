from rest_framework import serializers
from .models import Rental, CarListing, CarModel, Make, User, Review, Service
import datetime
from django.db.models import Avg

# class EmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Employee
#         fields ='__all__'

        
# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields ='__all__'




class CarModelSerializer(serializers.ModelSerializer):

    make = serializers.SlugRelatedField(queryset=Make.objects.all(), slug_field='make')
    class Meta:
        model = CarModel
        fields = ['make', 'model']

class MakeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Make
        fields ='__all__'

# class ClientSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Client
#         fields ='__all__'

# class EmployeeSerializer(serializers.ModelSerializer):
#     User = UserSerializer()
#     class Meta:
#         model = Employee
#         fields = '__all__'


class RentalSerializer(serializers.ModelSerializer):
    rent_client = serializers.SlugRelatedField(slug_field='username', read_only=True)
    rent_employee = serializers.SlugRelatedField(read_only=True, slug_field='username')
    car_info = serializers.SlugRelatedField(read_only=True, slug_field='registration_plate')
    price = serializers.ReadOnlyField()

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
    # current_user = serializers.SerializerMethodField('_user')

    # # Use this method for the custom field
    # def _user(self, obj):
    #     request = self.context.get('request', None)
    #     if request:
    #         return request.user



    class Meta:
        model = Rental
        fields ="__all__"
  

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    reviewed_employee = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field='username')
    class Meta:
        model = Review
        fields ='__all__'
  



class UserSerializer(serializers.ModelSerializer):
    reviews_made = ReviewSerializer(read_only=True, many=True, source='client_review')
    reviews_given = ReviewSerializer(read_only=True, many=True, source='employee_review')
    rentals_made = RentalSerializer(read_only=True, many=True, source='client_rent')
    rentals_given = RentalSerializer(read_only=True, many=True, source='employee_rent')
    rating = serializers.SerializerMethodField()
    def get_rating(self, ob):
        print(ob.employee_review.all())
        return ob.employee_review.all().aggregate(Avg('rating'))['rating__avg']


    class Meta:
        model = User
        fields = '__all__'


class ServiceSerializer(serializers.ModelSerializer):
    damaged_car = serializers.SlugRelatedField(queryset=CarListing.objects.all(), slug_field='registration_plate')
    guilty = serializers.SlugRelatedField(queryset=User.objects.all(), slug_field=('username'))


    class Meta:
        model = Service
        fields ='__all__'
        
class CarListingSerializer(serializers.ModelSerializer):
    car_model = serializers.SlugRelatedField(queryset=CarModel.objects.all(), slug_field='model')
    services = serializers.SerializerMethodField()
    rental = serializers.SerializerMethodField()

    class Meta:
        model = CarListing
        fields = '__all__'

    def get_rental(self, obj):
        if self.context.get('request').method == 'GET' and str(obj.id) in self.context.get('request').path:
            return RentalSerializer(obj.rental.all(), many=True, read_only=True).data
        else:
            return obj.rental.count()


    def get_services(self,obj):
        if self.context.get('request').method == 'GET' and str(obj.id) in self.context.get('request').path:
            return ServiceSerializer(obj.services.all(), many=True, read_only=True).data
        else:
            return obj.services.count()
 


        
