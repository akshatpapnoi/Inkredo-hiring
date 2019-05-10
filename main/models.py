from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from django.core.validators import MaxValueValidator, MinValueValidator

# Create your models here.

CATEGORY = (
        ('Education', 'Education'),
        ('Healthcare', 'Healthcare'),
        ('Hospitality', 'Hospitality'),
        ('Manufacturing', 'Manufacturing'),
        ('Media', 'Media'),
        ('Software', 'Software'),
    )

class Company(models.Model):
	admin = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
	name = models.CharField(_("Company Name"), max_length=200, unique=True)
	category = models.CharField(choices=CATEGORY, max_length=100)
	email = models.CharField(max_length=100, unique=True)
	mobile = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(9999999999)])
	address = models.TextField(max_length=200, blank=True, null=True)

	def __str__(self):
		return self.name
	


class UserProfile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.CharField(max_length=255)
	date_of_birth = models.DateField(_("Date of birth"), blank=True, null=True)
	email = models.EmailField(max_length=255, unique=True, null=True)
	mobile = models.PositiveIntegerField(blank=True, null=True, validators=[MaxValueValidator(9999999999)])
	company = models.ForeignKey(Company, on_delete=models.CASCADE)


	def __str__(self):
		return self.user.username