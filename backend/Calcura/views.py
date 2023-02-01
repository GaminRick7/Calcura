from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Calculator
from django.contrib.auth.decorators import login_required
from imgurpython import ImgurClient

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
            return HttpResponseRedirect("/", {"gmail": True})
        # user = str(request.user.get_full_name()).lower().split(" ")
        # messages.error(request, "Welcome " + user[0].capitalize() + " " + user[1].capitalize())
        # print(str("Welcome " + user[0].capitalize() + " " + user[1].capitalize())[:1])

    return render(request, 'calcura/index.html')

def chatPage(request, *args, **kwargs):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("/")
    context = {}
    return render(request, "calcura/chatPage.html", context)

@login_required(login_url='/')
def vendorPage(request):
    a=[]
    for listing in Calculator.objects.all():
        if listing.email==request.user.email:
            a.append(listing)
    return render(request, "calcura/vendorPage.html", {"listing": a})


@login_required(login_url='/')
def createListing(request):
    if request.method=="POST":
        title=request.POST['title']
        price=float(request.POST['price'])
        description=request.POST['description']
        tags=request.POST['tags']
        images=request.FILES.getlist('docfile')
        print("hi",len(images),title, price)
        print(images)
        # for image in images:
        #     print("ji")
        #     print(image)
        price = round(float(price),2)
        # client = ImgurClient("e4d2ee6042064ef", "effc638490e3951b29079d257969bdf93e4bb773")
        # for image in images:
        #     listing = Calculator(title=title, price=price,description=description,tags=tags,image=image,email=request.user.email)
        #     listing.save()

    return render(request, "calcura/createListing.html")