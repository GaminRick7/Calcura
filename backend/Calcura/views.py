from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Calculator, TempImage
from django.contrib.auth.decorators import login_required


# The view to handle the home page
def Index(request):
    """
    Contains the backend for the index page
    Returns:
        HttpResponseRedirect: if the user is not ocdsb.ca or a staff
        The template itself
    """
    
    #If the user is logged in
    if request.user.is_authenticated:
        #Only keep users which are staff or are ocdsb.ca email addresses. If not delete them. 
        if str(request.user.email).split("@")[1]!="ocdsb.ca" and not request.user.is_staff:

            #Getting user object and deleting it
            user = User.objects.get(email=request.user.email)
            user.delete()

            #Redirect back to homepage to reload, hence removing the sign out button
            return HttpResponseRedirect("/", {"gmail": True})

    #Returning the template
    return render(request, 'calcura/index.html')

def chatPage(request, *args, **kwargs):
    if request.user.is_authenticated == False:
        return HttpResponseRedirect("/")
    context = {}
    return render(request, "calcura/chatPage.html", context)

@login_required(login_url='/')
def vendorPage(request):
    #Variables
    a=[]

    #Looping through all Calculator objects
    for listing in Calculator.objects.all():

        #If the calculator belongs to the user, go inside if statement
        if listing.email==request.user.email:

            #Split the image string by a comma to store each link in its own list index, then append the listing to the list containing all listings
            listing.image=listing.image.split(",")
            a.append(listing)

    #Returning the template with listings information
    return render(request, "calcura/vendorPage.html", {"listing": a})

#Method to create a listing in the calculator model
@login_required(login_url='/')
def createListing(request):

    #Retrieve items if they sent form
    if request.method=="POST":
        title=request.POST['title']
        price=float(request.POST['price'])
        description=request.POST['description']
        tags=request.POST['tags']
        images=request.FILES.getlist('docfile')

        #Round the price to two decimal places
        price = round(float(price),2)

        #Looping through the images they pasted, and storing them in TempImage database model. Storing them to upload to cloudinary and to get image link url. Email is needed to link a temporary image to the user
        for image in images:
            listing = TempImage(image= image, email=request.user.email)
            listing.save()

        #Getting the images stored in TempImage, and defining a string to store the urls of images
        images=TempImage.objects.all()
        imageUrls=""

        #Go through the images, and if the image belongs to the user, add it to the imageUrls string. After that, delete the image from the database for storage purposes
        for image in images:
            if image.email==request.user.email:
                imageUrls += str(image.image.url) + ","
                image.delete()

        #Creating a new calculator listing, with the images stored as a string. 
        a=Calculator(title=title, description=description,image=imageUrls,price=price,tags=tags,email=request.user.email)
        a.save()
    return render(request, "calcura/createListing.html")

def editListing(request, id):
    listing=Calculator
    if id>len(Calculator.objects.all()):
        return HttpResponseRedirect("/")
    for c in Calculator.objects.all():
        if c.id==id:
            if c.email==request.user.email:
                listing=c
            else:
                return HttpResponseRedirect("/vendorPage")
    if request.method=="POST":
        title=request.POST['title']
        price=float(request.POST['price'])
        description=request.POST['description']
        tags=request.POST['tags']
        images=request.FILES.getlist('docfile')
        #Round the price to two decimal places
        price = round(float(price),2)

        #Looping through the images they pasted, and storing them in TempImage database model. Storing them to upload to cloudinary and to get image link url. Email is needed to link a temporary image to the user
        for image in images:
            listing = TempImage(image= image, email=request.user.email)
            listing.save()

        #Getting the images stored in TempImage, and defining a string to store the urls of images
        images=TempImage.objects.all()
        imageUrls=""

        #Go through the images, and if the image belongs to the user, add it to the imageUrls string. After that, delete the image from the database for storage purposes
        for image in images:
            if image.email==request.user.email:
                imageUrls += str(image.image.url) + ","
                image.delete()
        print(imageUrls)

        listing.title=title
        listing.price=price
        listing.description=description
        listing.tags=tags
        listing.image=imageUrls
        print(listing.title)
        print(listing.price)
        print(listing.description)
        print(listing.tags)
        print(listing.image)
        Calculator.objects.filter(id=id).update(title=title,price=price,description=description,tags=tags,image=imageUrls)
        

    return render(request, "calcura/editListing.html", {"l": listing})