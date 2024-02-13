from django.db import models
from category.models import Cetagory

class Post(models.Model):
    image = models.ImageField(upload_to='bookposts/media/uploads', blank=True, null=True)
    book_name = models.CharField(max_length=100) 
    book_detail = models.TextField()
    book_price = models.IntegerField()
    category = models.ForeignKey(Cetagory, on_delete=models.CASCADE)
    def __str__(self):
        return self.book_name
    

class Review(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()
    def __str__(self):
        return self.name

