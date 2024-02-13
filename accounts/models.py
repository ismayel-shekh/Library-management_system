from django.db import models

# Create your models here.
from django.contrib.auth.models import User
GENDER_TYPE = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)

class UserLibraryAccount(models.Model):
    user = models.OneToOneField(User, related_name='account', on_delete=models.CASCADE)
    account_no = models.IntegerField(unique=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)
    Name = models.CharField(max_length=50)
    birth_date = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    def __str__(self):
        return str(self.Name)