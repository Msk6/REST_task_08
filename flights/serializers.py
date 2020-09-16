from rest_framework import serializers
from django.contrib.auth.models import User

from .models import Flight, Booking, Profile
from datetime import datetime


class FlightSerializer(serializers.ModelSerializer):
	class Meta:
		model = Flight
		fields = ['destination', 'time', 'price', 'id']


class BookingSerializer(serializers.ModelSerializer):
	flight = serializers.SlugRelatedField(read_only=True, slug_field='destination')
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'id']


class BookingDetailsSerializer(serializers.ModelSerializer):
	total = serializers.SerializerMethodField()
	flight = FlightSerializer()
	class Meta:
		model = Booking
		fields = ['flight', 'date', 'passengers', 'id', 'total']
	
	def get_total(self, obj):
		return obj.flight.price * obj.passengers


class AdminUpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['date', 'passengers']


class UpdateBookingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Booking
		fields = ['passengers']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'password', 'first_name', 'last_name']

    def create(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']
        first_name = validated_data['first_name']
        last_name = validated_data['last_name']
        new_user = User(username=username, first_name=first_name, last_name=last_name)
        new_user.set_password(password)
        new_user.save()
        return validated_data


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = User
		fields = ['first_name', 'last_name',]


class ProfileSerializer(serializers.ModelSerializer):
	tier = serializers.SerializerMethodField()
	past_bookings = serializers.SerializerMethodField()
	user = UserSerializer()

	class Meta:
		model = Profile
		fields = ['user', 'miles', 'past_bookings', 'tier',]
		#fields = ['first_name', 'last_name', 'miles', 'tier',]
	
	def get_past_bookings(self, obj):
		return BookingSerializer(
			obj.user.bookings.filter(date__lt=datetime.now()), many=True
			).data

	def get_tier(self, obj):
		if 9999 >= obj.miles >= 0:
			return 'Blue'
		elif obj.miles <= 59999:
			return 'Silver'
		elif obj.miles <= 99999:
			return 'Gold'
		elif obj.miles >= 100000:
			return 'Platinum'

		
		

