from django.shortcuts import render
from django.views.generic import TemplateView
from category.models import Cetagory
from bookposts.models import Post
from borrowed_book.models import borrowed_history
def home(request, category_slug = None):
    data = Post.objects.all()
    if category_slug is not None:
        category = Cetagory.objects.get(Name = category_slug)
        data = Post.objects.filter(category = category)
    categories = Cetagory.objects.all()

    return render(request, 'home.html', {'data': data, 'category': categories,})

# def home(request, category_slug = None):
#     data = Post.objects.all()
#     if category_slug is not None:
#         category = Category.objects.get(Name = category_slug)
#         #not clear that part
#         data = Post.objects.filter(category  = category)
#     categories = Category.objects.all()
#     return render(request, 'home.html', {'data' : data, 'category' : categories})