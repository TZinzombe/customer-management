from django.shortcuts import render

# Create your views here.
from .models import PersonalInfo

def index(request):
    personal_info = PersonalInfo.objects.all()
    return render(request, 'index.html', {'personal_info': personal_info})
