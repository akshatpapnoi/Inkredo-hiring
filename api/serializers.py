from django.contrib.auth import authenticate
from main.models import UserProfile, Company
from rest_framework import serializers, generics
from knox.models import AuthToken
from django.contrib.auth.models import User




class LoginUserSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        user = authenticate(**data)
        if user and user.is_active:
            return user
        raise serializers.ValidationError("Credentials wrong")

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password',]

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        read_only_fields = ['user']


class CreateUserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ['username', 'profile', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],  validated_data['password'])
        profile_data = validated_data.pop('profile')
        profile = UserProfile.objects.create(
            user = user,
            name = profile_data['name'],
            date_of_birth = profile_data['date_of_birth'],
            email = profile_data['email'],
            mobile = profile_data['mobile'],
            company = profile_data['company'],
        )
        return user



class ComapanySerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ['password',]

class CompanyProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        read_only_fields = ['admin']


class CreateCompanySerializer(serializers.ModelSerializer):
    company = CompanyProfileSerializer(required=True)
    class Meta:
        model = User
        fields = ['username', 'company', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],  validated_data['password'])
        profile_data = validated_data.pop('company')
        profile = Company.objects.create(
            admin = user,
            name = profile_data['name'],
            category = profile_data['category'],
            email = profile_data['email'],
            mobile = profile_data['mobile'],
            address = profile_data['address'],
        )
        return user