from django.contrib import admin
from django.urls import path, include
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from home.serializers import RegisterSerializer,LoginSerializer,CarSerializer
from home.models import Car
from rest_framework.views import APIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication,BasicAuthentication



# api route for registration

class RegisterAPI(APIView):
    def post(self,request):
        data=request.data
        serializer=RegisterSerializer(data=data)
        if not serializer.is_valid():
            return Response(serializer.errors)
        
        serializer.save()
        return Response({'message':'Registration successfully'})
    
# api route for login

class LoginAPI(APIView):
    def post(self, request):
        data = request.data
        serializer = LoginSerializer(data=data)

        if not serializer.is_valid():
            return Response(serializer.errors)
        try:
            user = User.objects.get(email=serializer.validated_data['email'])
        except User.DoesNotExist:
            return Response({'message': 'Invalid email or password'})

        if not user.check_password(serializer.validated_data['password']):
            return Response({'message': 'Invalid email or password'})

        token, created= Token.objects.get_or_create(user=user)

        return Response({'message': 'Login successful', 'token': token.key})


# adding the car 
class AddCarAPI(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        data = request.data
        serializer = CarSerializer(data=data)
        
        if not serializer.is_valid():
            return Response(serializer.errors, status=400)
        
        serializer.save() 
        return Response({'message': 'Car added successfully', 'data': serializer.data}, status=201)


# creating api for view car

class CarDetailAPI(APIView):
    permission_classes = [IsAuthenticated] 
    authentication_classes = [TokenAuthentication]

    def get(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        serializer = CarSerializer(car)
        return Response(serializer.data)

# api for updating car details
class CarUpdateAPI(APIView):
    permission_classes = [IsAuthenticated]  
    authentication_classes = [TokenAuthentication]

    def put(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        serializer = CarSerializer(car, data=request.data, partial=True)  

        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Car updated successfully", "data": serializer.data})
        return Response(serializer.errors, status=400)


class CarDeleteAPI(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def delete(self, request, car_id):
        try:
            # Fetch the car by ID
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=404)

        # Delete the car
        car.delete()
        return Response({"message": "Car deleted successfully"})

urlpatterns = [
    path('api/register/',RegisterAPI.as_view()),
    path('api/login/',LoginAPI.as_view()),
    path('api/addCar/', AddCarAPI.as_view()),
    path('admin/', admin.site.urls),
    path('api/car/<int:car_id>/', CarDetailAPI.as_view()),
    path('api/car/update/<int:car_id>/', CarUpdateAPI.as_view()),
    path('api/car/delete/<int:car_id>/', CarDeleteAPI.as_view()),
 ]
