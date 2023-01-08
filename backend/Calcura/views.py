from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages

# The view to handle the home page
def Index(request):

    #If the user is logged in
    if request.user.is_authenticated:

        #Only keep users which are staff or are ocdsb.ca email addresses. If not delete them. 
        if str(request.user.email).split("@")[1]!="ocdsb.ca" and not request.user.is_staff:

            #Getting user object and deleting it\
            user = User.objects.get(email=request.user.email)
            user.delete()

            #Redirect back to homepage to reload and remove the sign out button
            return HttpResponseRedirect("/")
        user = str(request.user.get_full_name()).lower().split(" ")
        messages.error(request, "Welcome " + user[0].capitalize() + " " + user[1].capitalize())
        print(str("Welcome " + user[0].capitalize() + " " + user[1].capitalize())[:1])

    return render(request, 'calcura/index.html')