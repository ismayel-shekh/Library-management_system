from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('details/<int:id>', views.BookPostView.as_view(), name='detail_post'),
    path('borrow/<int:id>', views.borrowed_book, name='borrowed_book'), 
    path('review/<int:id>', views.BookPostReiewView.as_view(), name='review'),
]
