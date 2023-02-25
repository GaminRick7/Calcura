from django.shortcuts import render
from django.contrib.auth import logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Calculator, TempImage
from django.contrib.auth.decorators import login_required
from django.db.models.query_utils import DeferredAttribute

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
    noListings=False
    
    #Looping through all Calculator objects
    for listing in Calculator.objects.all():

        #If the calculator belongs to the user, go inside if statement
        if listing.email==request.user.email:

            #Split the image string by a comma to store each link in its own list index, then append the listing to the list containing all listings
            listing.image=listing.image.split(",")
            print(listing.tags)
            listing.tags = listing.tags.split("  ")[0:-1]
            a.append(listing)
    
    #Reversing list, so most recent is at top
    a.reverse()

    #If a is empty, there are no listings. Pass as context to frontend
    if len(a) == 0:
        noListings = True
    #Returning the template with listings information
    return render(request, "calcura/vendorPage.html", {"listing": a, "length": noListings})

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
            if not checkValidImageEnding(str(image)):
                return render(request, "calcura/createListing.html", {"invalidEnding": True})
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
        a=Calculator(title=title, description=description,image=imageUrls,price=price,tags=tags,email=request.user.email,fullname=request.user.get_full_name())
        a.save()
        return HttpResponseRedirect("/vendorPage")
    return render(request, "calcura/createListing.html")

def editListing(request, id):
    #Define listing variable, set it to the Calculator model
    listing=Calculator

    #Try to get a calculator with the given id, if it doesn't exist, return to vendorPage
    try:
        listing=Calculator.objects.all().get(id=id)
    except:
        return HttpResponseRedirect("/vendorPage")
    print(listing)

    #If the listing doesn't belong to the user, then redirect back to index
    if listing.email!=request.user.email:
        return HttpResponseRedirect("/")

    #Getting the first image in the image list stored within the listing
    originalImageUrls = listing.image
    listing.image = listing.image.split(",")
    listing.image.pop(-1)

    #If submitting editListing form
    if  "submit" in request.POST:

        #Get form data, and if its blank leave it as is
        if request.POST['title'] != "":
            title=request.POST['title']
        else:
            title= listing.title

        if request.POST['price'] != "":
            price=float(request.POST['price'])
            #Round the price to two decimal places
            price = round(float(price),2)
        else:
            price= listing.price

        if request.POST['description'] != "":
            description=request.POST['description']
        else:
            description = listing.description

        if request.POST['tags'] != "":
            tags=request.POST['tags']
        else:
            tags = listing.tags

        if len(request.FILES.getlist('docfile')) > 0:
            images=request.FILES.getlist('docfile')
            #Looping through the images they pasted, and storing them in TempImage database model. Storing them to upload to cloudinary and to get image link url. Email is needed to link a temporary image to the user
            for image in images:
                if not checkValidImageEnding(str(image)):
                    return render(request, "calcura/editListing.html", {"l": listing, "invalidEnding": True})

                tempImg = TempImage(image= image, email=request.user.email)
                tempImg.save()

            #Getting the images stored in TempImage, and defining a string to store the urls of images
            images=TempImage.objects.all()
            imageUrls=""

            #Go through the images, and if the image belongs to the user, add it to the imageUrls string. After that, delete the image from the database for storage purposes
            for image in images:
                if image.email==request.user.email:
                    imageUrls += str(image.image.url) + ","
                    image.delete()
        else:
            imageUrls = originalImageUrls

        #Updating the calculator object
        Calculator.objects.filter(id=id).update(title=title,price=price,description=description,tags=tags,image=imageUrls)

        #Redirecting user to the vendorPage
        return HttpResponseRedirect("/vendorPage")
        
    #If they submit the delete form, delete the listing and send user to vendorPage
    elif 'delete' in request.POST:
        listing.delete()
        return HttpResponseRedirect("/vendorPage")
    
    #Return template, with the listing which is being edited
    return render(request, "calcura/editListing.html", {"l": listing})

@login_required(login_url='/')
def shop(request):

    #If form didn't return anything/method wasn't POST, return all available listings, and state no filters were given
    filter=None
    listings=Calculator.objects.all()


    
    #If the request was sent through the search bar...
    if request.method=="POST":

        #Get the filter from the form
        filter = request.POST["search-navbar"]

        #Get all listings from Calculator table, and create an empty list to append filtered listings
        allListings=Calculator.objects.all()
        listings=[]

        #Loop through all the listings
        for listing in allListings:

            #If the filter is in a listing title, append the listing to the filtered listings list
            if filter.lower() in listing.title.lower():
                listings.append(listing)
    
    #In the listings, split the image list so it is accessible as a list
    for i in range(len(listings)):
        listings[i].image = listings[i].image.split(",")
        listings[i].tags = listings[i].tags.split("  ")[0:-1]

    #Return the template
    return render(request, "calcura/shop.html", {"listings":listings, "filter": filter})

def checkValidImageEnding(imageLink):
    splitImage=imageLink.split(".")
    if splitImage[len(splitImage)-1] not in ["jpg","webp","png","jpeg"]:
        return False
    return True