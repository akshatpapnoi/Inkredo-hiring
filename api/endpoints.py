from django.urls import path, include
from api.views import *

urlpatterns =[
	path('register', UserRegistrationAPI.as_view(), name="register"),
	path('<slug:user>', UserProfileRUDAPIView.as_view(), name="user-profile-rud"),
	path('company/register', CompanyRegistrationAPI.as_view(), name="company-register"),
	path('company/<slug:name>', CompanyProfileRUDAPIView.as_view(), name="company-profile-rud"),


]