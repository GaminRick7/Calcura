
# Calcura

An e-commerce platform where students can buy and sell graphing calculators online.


## User Features

- ✏️ Create and Edit Your Listings
    - As a seller on Calcura, you can create and edit your own listings to sell your calculator.
- 👛 Browse Through Listings
    - As a buyer on Calcura, you can browse through various listings and filter your search to find the perfect calculator for you.
- 💖 Favourite Listings
    - Users can favourite calculator listings that they like and save them to view later.
- 💬 Real-time Chat System
    - Buyers can contact sellers through a real-time chat system and discuss where to meet, price etc.

## Administrator Features
- 👤 Manage All Users
    - To keep the Calcura community safe, administrators have the ability to create/edit/delete all aspects of user's profile, listings, and chat room.
- ❗Report Listings
    - To keep the Calcura community safe, users have the ability to report listings and message rooms which admins can view.
- 🔒 Lock Chat Rooms
    - To keep the Calcura community safe, administrators can lock and delete message rooms.

## Installation and Setup

Clone the project using Git

```bash
git clone https://github.com/GaminRick7/Calcura 
```
Create a virtual environment and activate it.
```bash
python -m venv env
env/Scripts/Activate
```
Install the dependencies 
```bash
pip install -r requirements.txt 
```

    
## Deployment

### Setting Up Database

To deploy this project, you will need to create a database.

For this, you will need to download PostgreSQL [here](https://www.postgresql.org/download/). We recommend installing PGAdmin4 during the installation process.

Create a database called `calcura` on port number `5432`. If you have a different port number, go to `backend/settings.py` and then change the 'PORT' in the following code to your port number.

```python
DATABASES = {
     'default': {

        'ENGINE': 'django.db.backends.postgresql_psycopg2',

        'NAME': 'calcura',

        'USER': 'postgres',

        'PASSWORD': os.getenv('databasepass'), 

        'HOST': '127.0.0.1',

        'PORT': '5432',

    }
}
```



### Environment Variables

To run this project, you will need to add the following environment variable to your `.env` file.

```
databasepass=["YOUR DATABASE PASSWORD"]
```

You must have quotes around your database password.

### Migrations

Once the database is created and set up, change directory into `backend`. Then, run the following:

```bash
python manage.py makemigrations Calcura
python manage.py migrate Calcura
python manage.py makemigrations chatSystem
python manage.py migrate chatSystem
python manage.py makemigrations
python manage.py migrate
```
## Running The Program

The first time you run the program, you need to create admin account. To do this, first ensure you are in `backend/` then follow the instructions after running the command below

```
python manage.py createsuperuser
```
Then, go to `settings.py`, and uncomment the following lines of code in `Index` function:

```python
a=Administration()
a.save()
```

Then, start the server using
```
python manage.py runserver
```
Open the server (http://127.0.0.1:8000) in a browser and once you see the home page, you know it's working!

Go back and comment back the lines you previously uncommented.
```python
a=Administration()
a.save()
```
Then, in your browser, proceed to http://127.0.0.1:8000/admin and login with the credentials you previously created.

### Setting Up Google OAuth

In the sidebar of the admin page, proceed to `Social Applications`create a new social application. Select `Google` as the Provider, name it `Calcura`, set the Client ID to
```
894016689644-i7e3dg6d1gb753lvl3cv7v4e0r8re9ue.apps.googleusercontent.com
```
and set Secret Key to 
```
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
```
Double click `example.com` such that it moves to Chosen Sites. Then, click the plus icon to add `http://127.0.0.1:8000`.

The website is now fully setup! Every time you want to run the server, in `Calcura/backend` use `python manage.py runserver`.


## Developers

- [@GaminRick7](https://www.github.com/GaminRick7)
- [@Iwillgetmy](https://www.github.com/Iwillgetmy)

## Known Bugs

- When clicking to the outside of a sidebar, the screen appears grey and nothing is clickable. To fix this issue on mobile, reload your page. On a laptop, click the "ESC" button. 
- Sometimes, the image carousel of listings temporarily breaks and appears as a white screen without warning. It then fixes itself. It may be a problem associated with flowbite scripts; however, the current nature of the issue isn't known

## Support

For support, email calcura06@gmail.com.

## Citations
[1] “Free SVG vectors and icons,” SVG Repo, https://www.svgrepo.com/ (accessed Jun. 1, 2023). 
* Used for the Calcura Logo, "No Chats" image, "Open a Chat" image, and Chat icon


[2] Heroicons, https://heroicons.com/ (accessed Jun. 1, 2023). 
* Used for all icons on the website (i.e. dashboard icons) with the exception of the ones retrieved from SVG Repo above.

[3] “Bad Words List,” Google, https://code.google.com/archive/p/badwordslist/downloads (accessed March, 2023).
* Used as a list to check of bad words sent when chatting

[4] “Django - sending e-mails,” Online Courses and eBooks Library, https://www.tutorialspoint.com/django/django_sending_emails.htm (accessed Ju. 1, 2023).
* Code used for the contact page form to send emails using Django’s SMTP library 

[5] “Realtime chat app using Django,” GeeksforGeeks, https://www.geeksforgeeks.org/realtime-chat-app-using-django/ (accessed March. 1, 2023).
* Code used to create the ChatConsumer class, create routing for websockets, and create javascript to send messages to websockets & receive messages from websockets.


[6] “Merge sort - data structure and algorithms tutorials,” GeeksforGeeks, https://www.geeksforgeeks.org/merge-sort/ (accessed April, 2023). 
* 

[7] “Tailwind CSS animation on scroll library,” TAOS, https://versoly.com/taos (accessed Jun. 1, 2023). 
* Code used for fade in and slide in animations seen on the home page.

[8] “Typwriter JS V2,” Typewriter JS - A simple yet powerful native javascript plugin for a cool typewriter effect., https://safi.me.uk/typewriterjs/ (accessed Jun. 1, 2023).
* Code used for typrewriter effect seen on home page.

[9] “Flowbite Components,” Flowbite.com, https://flowbite.com/ (accessed Jun. 1, 2023). 
* Components used for:
    * Delete listing, view listing, report listing, and report message room popups
    * Input fields for the search bar and the message bar
    * Popup sidebar to apply filters on the shop page and see the list of chats in the mobile view.
    * Radio button to select between setting a price or setting the listing as negotiable
 

[10] “Tailwind UI - official tailwind CSS components &amp; templates,” Tailwind UI - Official Tailwind CSS Components &amp; Templates, https://tailwindui.com/ (accessed Jun. 1, 2023). 
* Components used for hero section for home page and grid of listings for shop page/vendor page


[11] “Tailwind CSS Docs,” Tailwind CSS, https://tailwindcss.com/docs/ (accessed Jun. 1, 2023).
* Used for general Tailwind CSS reference.

[12] “Uploading images to cloudinary from a django application,” Section, https://www.section.io/engineering-education/uploading-images-to-cloudinary-from-django-application/ (accessed Jun. 1, 2023).
* Code used to upload images to online database (Cloudinary) using Cloudinary API. 

[13] “Django,” Django Project, https://docs.djangoproject.com/en/4.1/ (accessed May 31, 2023). 
* Used for general Django reference

[14] “Select2,” Atom, https://select2.org/ (accessed May 31, 2023). 
* Code used for multiple select dropdown for the taks system when creating or editing a listing.



## License

[MIT](https://choosealicense.com/licenses/mit/)