from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Calculator, TempImage, Administration, MessageRoom
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random

# The view to handle the home page
def Index(request):
    """
    Contains the backend for the index page
    Returns:
        HttpResponseRedirect: if the user is not ocdsb.ca or a staff
        The template itself
    """
    # a=Administration()
    # a.save()
    #If the user is logged in
    if request.user.is_authenticated:
        #Only keep users which are staff or are ocdsb.ca email addresses. If not delete them. 
        if str(request.user.email).split("@")[1]!="ocdsb.ca" and not request.user.is_staff:

            #Getting user object and deleting it
            user = User.objects.get(email=request.user.email)
            user.delete()

            #Redirect back to homepage to reload, hence removing the sign out button
            messages.error(request, "You must log in with an OCDSB account")
            return HttpResponseRedirect("/")

    #Returning the template
    return render(request, 'calcura/index.html')

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
        a=Calculator(title=title, description=description,image=imageUrls,price=price,tags=tags,email=request.user.email,fullname=request.user.get_full_name(),id=generateId(Calculator))
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
    filter=""
    listings=Calculator.objects.all()
    tags=[]
    min=""
    max=""

    #If the request was sent through the search bar...
    if "search-navbar" in request.POST:
        #Get the filter from the form
        filter = request.POST["search-navbar"]

        #Get all listings from Calculator table, and create an empty list to append filtered listings
        listings=[]

        #Loop through all the listings
        for listing in Calculator.objects.all():

            #If the filter is in a listing title, append the listing to the filtered listings list
            if filter.lower() in listing.title.lower():
                listings.append(listing)

    #If they submitted the advanced filter 
    if "advancedFilter" in request.POST:
        
        #Initialization
        filter=request.POST["filter"]
        listings=[]
        advancedFilters=[False,False,False]
        a=Administration.objects.all()

        #Getting filter with min and max, if one is blank accept neither
        if request.POST['min'] != "" and request.POST['max']!="":
            max=int(request.POST["max"])
            min=int(request.POST["min"])
            advancedFilters[0]=True
        
        #For all currently existing tags, check if they are checked using checkIfChecked method
        for i in a[0].tags.split(","):
            checkIfChecked(request, i, tags)
        
        #If the tags list's length is greater than zero, then accept it as a filter
        if len(tags)>0:
            advancedFilters[1]=True

        #If the filter is not none, then accept it as a filter
        if filter!=None:
            advancedFilters[2]=True

        #Loop through all listings
        for listing in Calculator.objects.all():

            #Reset a count variable used for tag filtering
            count=0

            #If the filter is in a listing title, and the price lies within the min and max, append the listing to the filtered listings list
            if advancedFilters[2]:

                #Check if the filter is within the title of a listing. If skip all and go to next listing
                if filter.lower() not in listing.title.lower():
                    continue
                    
            #Check for tags
            if advancedFilters[1]:

                #For each tag in the tags that were selected
                for i in tags:
                    
                    #If the tag (i) is within the listing's tags, increase the count
                    if i in listing.tags.split("  "):
                        count+=1
                
                #If the count is not the same as the length of selected tags, break
                if count!=len(tags):
                    continue
            
            #Check if the price is within the tags
            if advancedFilters[0]:
                if listing.price not in range(min,max+1):
                    continue
            
            #Append the listing to the list with all acceptable listings
            listings.append(listing)
    if "chat" in request.POST:
        fullname = request.POST["name"]
        if request.user.get_full_name()!=fullname:
            name=request.user.get_full_name()+","+fullname
            name2=fullname+","+request.user.get_full_name()
            if MessageRoom.objects.filter(users=name).exists():
                obj=MessageRoom.objects.get(users=name)
                return HttpResponseRedirect("/chat/"+str(obj.id))
            if MessageRoom.objects.filter(users=name2).exists():
                obj=MessageRoom.objects.get(users=name2)
                return HttpResponseRedirect("/chat/"+obj.id)
            else:
                id=generateId(MessageRoom)
                messageRoom = MessageRoom(users=name, id=id)
                messageRoom.save()
                return HttpResponseRedirect("/chat/"+str(id))

    #In the listings, split the image list so it is accessible as a list
    for i in range(len(listings)):
        listings[i].image = listings[i].image.split(",")
        listings[i].tags = listings[i].tags.split("  ")[0:-1]

    #Items in the listings table are stored so the higher rows are the earliest added. Default option is sort by upload date, so reverse so most recent uplaoded/edited listing is at top
    for l in listings:
        print(l.datetime)
    #Check if listings are present
    listingsPresent=True
    if len(listings)==0:
        listingsPresent=False

    #Return the template
    return render(request, "calcura/shop.html", {"listings":listings, "filter": filter,"tagList":tags, "allTags": Administration.objects.all()[0].tags.split(","), "min":min,"max":max, "listingsPresent":listingsPresent})

def checkValidImageEnding(imageLink):
    """
    Check if an image ending is valid
    Args:
        imageLink: the link of the image to check
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

def checkIfChecked(request, string, listy):
    """
    Function to check if a checkbox is checked
    Args:
        request: the request sent by user
        string (str): the name of the checkbox to check
        listy (list): list which contains all checked checkboxes
    """

    #If a request contains the checkbox, it was checked. If not, it wasn't checked
    try:
        #Check if request contains the string, and if yes, append it
        request.POST[string]
        listy.append(string)
    except:
        #They did not check the textbox
        pass

def generateId(model):
    id=random.randint(10**10,10**11-1)
    while model.objects.filter(id=id).exists():
        id=random.randint(10**20,10**21-1)
    return id