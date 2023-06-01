
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

To run this project, you will need to add the following environment variable to your `.env` file with your database password.

```
databasepass=*****
```



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

The first time you run the program, you need to create admin account. To do this, first ensure you are in `backend/` then run and follow the prompts

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




## Authors

- [@GaminRick7](https://www.github.com/GaminRick7)
- [@Iwillgetmy](https://www.github.com/Iwillgetmy)


## Support

For support, email calcura06@gmail.com.

## Citations




## License

[MIT](https://choosealicense.com/licenses/mit/)

