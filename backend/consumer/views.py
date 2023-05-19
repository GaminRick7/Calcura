from datetime import datetime
from django.utils import timezone
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from Calcura.models import Calculator, Favourite, MessageRoom, Administration, Report, User
from django.http import HttpResponseRedirect
from Calcura.views import generateId, mergeSort, checkIfChecked
from django.db.models import Q  
# Create your views here.
@login_required(login_url='/')
def shop(request, pageNum):
    """
    Backend for the shop page
    Args:
        request (User): the user making the request to the page
        pageNum (int): the page number which is being accessed
    Returns:
        render: the request
    """

    #Initialize variables
    filter=""
    listings=list(Calculator.objects.exclude(user=request.user))
    tags=[]
    min=""
    max=""
    sortMethod=""
    notSorted=True
    
    #Reporting a listing
    checkReport(request)

    #Favouriting a listing
    checkFavourite(request)

    #If the request was sent through the search bar...
    if "search-navbar" in request.POST:
        #Get the filter from the form
        filter = request.POST["search-navbar"]

        #Get all listings from Calculator table, and create an empty list to append filtered listings
        listings=[]

        #Loop through all the listings
        for listing in Calculator.objects.exclude(user=request.user):

            #If the filter is in a listing title, append the listing to the filtered listings list
            if filter.lower() in listing.title.lower():
                listings.append(listing)

    #If they submitted the advanced filter, or if the clicked the previous or next button (still want to check for filters on new page)
    if "advancedFilter" in request.POST or "prev" in request.POST or "next" in request.POST or "favourite" in request.POST:
        print(listings)
        #Initialization of variables
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

        filterListings(advancedFilters,listings,tags,min,max, filter, request)
        
        #Sorting the listings
        sortMethod=request.POST["sorting"]
        sortList(sortMethod,listings)
        notSorted=False

    #If they made a request to talk to a vendor . . .
    if "chat" in request.POST:

        #Get the email of the vendor from the request
        email = request.POST["email"]

        #dealing with message rooms
        return messageRoomCreationOrRouting(request,email)
       
   

    #If they didn't submit a sorting option, sort listings by datetime
    if notSorted:
        mergeSort(listings,"datetime")
        listings.reverse()

    nextListingsPresent=False
    if len(listings[10*(pageNum+1):10*(pageNum+2)])>0:
        nextListingsPresent=True

    listings=listings[10*pageNum:10*(1+pageNum)]




    #In the listings, split the image list so it is accessible as a list
    for i in range(len(listings)):
        listings[i].image = listings[i].image.split(",")[:-1]
        listings[i].numImages=len(listings[i].image)
        listings[i].imageNumber = range(listings[i].numImages)
        listings[i].tags = listings[i].tags.split("  ")[0:-1]

    #Check if listings are present
    listingsPresent = len(listings)!=0
    print(request.POST)
    favoritedListings=[]
    for i in Favourite.objects.filter(user=request.user):
        favoritedListings.append(i.listing.id)
    #Return the template
    return render(request, "calcura/shop.html", {"listings":listings, "filter": filter,"tagList":tags, "allTags": Administration.objects.all()[0].tags.split(","), "min":min,"max":max, "sortMethod":sortMethod, "listingsPresent":listingsPresent, "pageNum": pageNum, "favourites": favoritedListings, "nextListingsPresent":nextListingsPresent, "shopPage": True})

@login_required(login_url='/')
def favourites(request):
    """
    Backend for the favourites page
    Args:
        request (User): the user making the request
    Returns:
        render: the template
    """
    #Check if they are attempting to remove listing
    if "listing" in request.POST:
        try:
            id=request.POST["listing"]
            Favourite.objects.get(listing=Calculator.objects.get(id=id)).delete()
        except:
            pass
    
    #Get all listings which are favourited
    listings=Favourite.objects.filter(user=request.user)
    
    #In the listings, split the image list so it is accessible as a list
    for i in range(len(listings)):
        listings[i].listing.image = listings[i].listing.image.split(",")[:-1]
        listings[i].listing.numImages=len(listings[i].listing.image)
        listings[i].listing.imageNumber = range(listings[i].listing.numImages)
        listings[i].listing.tags = listings[i].listing.tags.split("  ")[0:-1]

    return render(request, "calcura/favourites.html", {"listings": listings})

def sortList(sortMethod, listings):
    #Sort by price ascending
    if sortMethod=="PA":
        mergeSort(listings, "price")

    #Sort by price descending
    elif sortMethod=="PD":
        mergeSort(listings,"price")
        listings.reverse()

    #Sort by date added (default)
    elif sortMethod=="DA":

        #Sorts by datetime from earliest, so most recent calculators are at end. That is why reverse() is needed
        mergeSort(listings,"datetime")
        listings.reverse()

def messageRoomCreationOrRouting(request, email):
    """
    Either creates a message room for uesrs to participate in, or routes users to a message room they already have with the user
    Args:
        request (User)
        email (str): email of the user to chat with
    """

    
    #Get the two possible variations for users in a room (in db stored as consumer + vendor)
    users1=request.user.email+","+email
    users2=email+","+request.user.email

    #Checking if the variations already exist in a message room to ensure duplication does not occur
    if MessageRoom.objects.filter(users=users1).exists():
        obj=MessageRoom.objects.get(users=users1)
        return HttpResponseRedirect("/chat/"+str(obj.id))
    if MessageRoom.objects.filter(users=users2).exists():
        obj=MessageRoom.objects.get(users=users2)
        return HttpResponseRedirect("/chat/"+str(obj.id))
    
    #Create a new message room for the users, and redirect the user to the new message room
    else:
        id=generateId(MessageRoom)
        messageRoom = MessageRoom(users=users1, user1= request.user, user2= User.objects.get(email__exact=email),id=id, latestDateTime=datetime.now(timezone.utc))
        messageRoom.save()
        return HttpResponseRedirect("/chat/"+str(id)) 

def filterListings(advancedFilters, listings, tags, min, max, filter, request):
    """
    Method to filter listings based on what filters were gived in the webpage
    Args:
        advancedFilters (list): a list of booleans which indicate which filters were actually passed through (what to filter by)
        listings (list): all listings. Holds filtered calculators
        tags (list): which tags were wanted by the user
        min (int): min price of listing
        max (int): max price of listing
        filter (str): the search query to filter by
    """

    #Loop through all listings
    for listing in Calculator.objects.exclude(user=request.user):

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
            
            #If the count variable is not the same as the length of selected tags, break
            if count!=len(tags):
                continue
        
        #Check if the price is within the tags
        if advancedFilters[0]:
            if listing.price not in range(min,max+1):
                continue

        #Append the listing to the list with all acceptable listings
        listings.append(listing) 

def checkReport(request):
    if "report" in request.POST:
        listing = Calculator.objects.get(id=request.POST['listingid'])
        description = request.POST['description']
        r = Report(listing=listing, description=description, user=request.user)
        r.save()

def checkFavourite(request):
    print(request.POST)
    if "favourite" in request.POST:
        listing=Calculator.objects.get(id=request.POST['listing'])
        if request.POST['favorited']=="False":
            Favourite(user=request.user, listing=listing).save()
        else:
            Favourite.objects.get(listing=listing).delete()
            