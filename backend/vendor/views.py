"""
File: views.py
Authors: Raihaan Sandhu and Darun Kanesalingam
Last Modified: May 26, 2023
Version: 1.0.0

This file contains logic for the vendor pages.
"""

from django.shortcuts import render
from Calcura.models import Calculator, TempImage
from Calcura.views import mergeSort, generateId
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required

def vendorPage(request):
    """
    Hosts the backend for the vendorPage
    Args:
        request: User making the request
    Returns:
        render: the template
    """
    #Variables
    listings=[]
    noListings=False
    
    #Looping through all Calculator objects
    for listing in Calculator.objects.all():

        #If the calculator belongs to the user, go inside if statement
        if listing.user.email==request.user.email:

            #Split the image string by a comma to store each link in its own list index, then append the listing to the list containing all listings
            listing.image=listing.image.split(",")
            listing.tags = listing.tags.split("  ")[0:-1]
            listings.append(listing)
    
    #Reversing list, so most recent is at top
    mergeSort(listings,"datetime")
    listings.reverse()
    
    #If a is empty, there are no listings. Pass as context to frontend
    noListings = len(listings) == 0
    
    #Returning the template with listings information
    return render(request, "calcura/vendorPage.html", {"listing": listings, "length": noListings})

#Method to create a listing in the calculator model
@login_required(login_url='/')
def createListing(request):
    """
    Backend for creating a listing
    Args:
        request (User): user making the request to the page
    Returns:
        render: the template
    """
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
            if not checkValidImageEnding(str(image)): #Although there is limiting in the frontend, it may not work on older browsers so nice to keep
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
        a=Calculator(title=title, description=description,image=imageUrls, price=price,tags=tags,id=generateId(Calculator), user=request.user)
        a.save()
        return HttpResponseRedirect("/vendorPage")
    return render(request, "calcura/createListing.html", {})

def editListing(request, id):
    
    """
    Backend for the editListing page
    Args:
        request (User): user making the request
        id (int): id of the calculator to be edited
    Returns:
        HttpResonseRedirect: To home if accessing someone else's listing, or to vendorpage if an invalid id is provided/deleting a listing
        render: the template
    """

    #Define listing variable, set it to the Calculator model
    listing=Calculator
    #Try to get a calculator with the given id, if it doesn't exist, return to vendorPage
    try:
        listing=Calculator.objects.all().get(id=id)
    except:
        return HttpResponseRedirect("/vendorPage")

    #If the listing doesn't belong to the user, then redirect back to index
    if listing.user.email!=request.user.email:
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

# Create your views here.
def checkValidImageEnding(imageLink):
    """
    Check if an image ending is valid
    Args:
        imageLink (str): the link of the image to check
    Returns:
        True if its of acceptable ending
        False if it is not
    """

    #Split the image by its period
    splitImage=imageLink.split(".")

    #If the last element in the list is not of an acceptable format, return False
    if splitImage[len(splitImage)-1] not in ["jpg","webp","png","jpeg","svg"]:
        return False
    
    #If not, return True
    return True
