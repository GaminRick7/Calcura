from django.shortcuts import render
from django.contrib.auth import logout

# The view to handle the home page
def Index(request):

    #If the user is logged in
    if request.user.is_authenticated:

        #If their email address is not an ocdsb email address, log them out
        if str(request.user.email).split("@")[1]!="ocdsb.ca":
            logout(request) 
    return render(request, 'calcura/index.html')