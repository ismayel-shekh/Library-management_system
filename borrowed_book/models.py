from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class borrowed_history(models.Model):
    book_name = models.CharField(max_length=100)
    price = models.IntegerField()
    borrowed_date = models.DateTimeField(auto_now_add=True)
    book_id = models.IntegerField()
    account = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['borrowed_date']
    