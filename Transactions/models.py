from django.db import models
from accounts.models import UserLibraryAccount

# Create your models here.
class transaction(models.Model):
    account = models.ForeignKey(UserLibraryAccount, related_name = 'transactions', on_delete = models.CASCADE)
    amount = models.DecimalField( max_digits=12, decimal_places=2)
