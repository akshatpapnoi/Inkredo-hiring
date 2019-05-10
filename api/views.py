from rest_framework import generics, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from knox.models import AuthToken

from api.serializers import *
from .permissions import IsOwnerOrReadOnly
from main.models import UserProfile, Company

class UserRegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })

class UserProfileRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserProfileSerializer
    lookup_field = 'user'
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
    	return UserProfile.objects.all()

    def get_object(self):
    	user = self.kwargs.get('user')
    	return UserProfile.objects.get(user__username=user)

class CompanyRegistrationAPI(generics.GenericAPIView):
    serializer_class = CreateCompanySerializer
    queryset = User.objects.all()
    permission_classes = []
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user, context=self.get_serializer_context()).data,
        })

class CompanyProfileRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CompanyProfileSerializer
    lookup_field = 'name'
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        return UserProfile.objects.all()

    def get_object(self):
        name = self.kwargs.get('name')
        return UserProfile.objects.get(name=name)


