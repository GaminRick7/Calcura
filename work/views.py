from django.shortcuts import render
# from .models import calculator
from django.contrib.auth.models import User
from django.contrib.auth.forms import User, UserCreationForm

# Create your views here.


def index(request):
    # a = calculator(title="test", price=0.0, description="hi",
    #                tags="hi,hi", images="")
    # a.save()
    print(request.user)
    return render(request, 'index.html')
