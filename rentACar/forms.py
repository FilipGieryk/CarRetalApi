from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.db import transaction
from .models import User
# class ClientSignUpForm(UserCreationForm):
#     balance = forms.FloatField()
#     money_spent = forms.FloatField()
#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = "__all__"
#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
        
#         user.is_client = True
#         user.save()
#         client = Client.objects.create(user=user)
#         return user
class UserSignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    mobile = forms.CharField(max_length=15)
  
    class Meta(UserCreationForm.Meta):
        model = User
 
    @transaction.atomic
    def save(self):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data.get('first_name')
        user.last_name = self.cleaned_data.get('last_name')
        user.email = self.cleaned_data.get('email')
        user.mobile = self.cleaned_data.get('mobile')
        # test.is_employee = True
        user.save()
        
        return user