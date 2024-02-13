from django.shortcuts import render

# Create your views here.
from . import models

def history_view(request):
    history = models.borrowed_history.objects.filter(account = request.user)
    return render(request, 'history.html', {'data': history})