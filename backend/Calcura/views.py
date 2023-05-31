from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib import messages
from Calcura.models import Administration
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import random
from django.urls import reverse
from django.core.mail import send_mail

# The view to handle the home page
def Index(request):
    """
    Contains the backend for the index page
    Returns:
        HttpResponseRedirect: if the user is not ocdsb.ca or a staff
        The template itself
    """

    #Create administration object for tags
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
    return render(request, 'calcura/index.html', {})

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
    """
    Function to generate a random integer for models, of order of magnitude 10^10 (to be changed depending on scale of users)
    Args:
        model (class): which model to create an id for
    Returns:
        id (int): unique id to use for the model provided
    """

    #Generate an id
    id=random.randint(10**10,10**11-1)
    
    #If the id already exists, create another id till it doesn't exist
    while model.objects.filter(id=id).exists():
        id=random.randint(10**20,10**21-1)
    
    #Return the id
    return id

def mergeSort(a, param):
    """
    Function which performs mergeSort based on a list which holds objects via recursion
    Args:
        a (list): list which holds the objects
        param (str): what parameter to check by
    Returns:
        a: the sorted list
    """

    #Once list is sorted down to single indices, stop splitting list
    if len(a)>1:

        #Declare variables
        mid=len(a)//2
        L=a[:mid]
        R=a[mid:]
        pointerL=pointerR=pointerArr=0
        
        #Start splitting list down to single indices via recursion. Only once finished it will start merging the indices
        mergeSort(L, param)
        mergeSort(R, param)
        
        #While there are elements left in the left and right side of the arrays
        while pointerL<len(L) and pointerR<len(R):

            #If the left side is smaller at its current pointer, append to the main array and increase its pointer
            if getattr(L[pointerL],param)<getattr(R[pointerR],param):
                a[pointerArr]=L[pointerL]
                pointerL+=1
            #If the right side is smaller at its pointer, append to the main array and increase its pointer
            else:
                a[pointerArr]=R[pointerR]
                pointerR+=1
            #Increase global pointer
            pointerArr+=1
        
        #If there are elements left in the left array, append all to main array
        while pointerL<len(L):
            a[pointerArr]=L[pointerL]
            pointerArr+=1
            pointerL+=1
        
        #If there are elements left in the righ array, append all to main array
        while pointerR<len(R):
            a[pointerArr]=R[pointerR]
            pointerArr+=1
            pointerR+=1
        
        #Return the array
        return a



def contact(request):
    """
    Backend for the contact page
    Args:
        request (User): the user making the request
    Returns:
        render: the template
    """

    #If they submitted the form
    if request.method=="POST":

        #Get all data from form 
        name=request.POST["name"]
        email=request.POST["email"]
        message=request.POST["message"]

        #Use send_mail function to send email to Calcura06@gmail.com with form data
        try:
            res = send_mail("Message from: "+name, message+"\nEmail of sender: "+email, email, ["Calcura06@gmail.com"], fail_silently=False)
            #Notify user that their message wassent
            messages.success(request, "Your message was sent! We will get back to you as soon as possible.")
        except:
            messages.error(request, "Something went wrong. Please try again at a later time.")
    return render(request, "calcura/contact.html")