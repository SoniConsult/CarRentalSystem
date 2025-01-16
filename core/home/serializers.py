from rest_framework import serializers
from .models import Car
from django.contrib.auth.models import User 


# serializer for registration
class RegisterSerializer(serializers.Serializer):
      username=serializers.CharField()
      email= serializers.EmailField()
      password= serializers.CharField()
      role=serializers.CharField()
      def validate(self,data):
          if data['username']:
            if  User.objects.filter(username=data['username']).exists():
              raise serializers.ValidationError('Username already exists')
          if data['email']:
            if  User.objects.filter(email=data['email']).exists():
              raise serializers.ValidationError('Username already exists')
          
          return data
      
      def create(self,validate_data):
          user=User.objects.create(username=validate_data['username'],email=validate_data['email'])
          user.set_password(validate_data['password'])
          user.save()
  
          return validate_data
# creating user for login
      
class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()


# creating serializer for adding new car


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = ['model', 'year', 'registration_number', 'seating_capacity']  

