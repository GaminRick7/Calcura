from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Message

# Create your views here.
@login_required(login_url='/')
def chat(request, room_name):
    if request.method == 'POST':
        room=request.POST['roomname']
        print(room)
    return render(request, 'chat/chatPage.html')