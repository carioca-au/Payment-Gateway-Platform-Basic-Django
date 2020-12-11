# Payment Gateway Platform
A Basic Django 3 project that as start point

### Models

- Bank
- Company
- Account
- Payment

### Admin
>Basic admin registering all models and no custom features

### Forms

> Basic form (CreateCompanyForm) just to create the login page

### Templates
> Based on HTML 5, Jquery and Bootstrap, the templates implemented in this work are fairly simple and are here just as an example of a login scenario.
- CreateCompanyForm

### Decorators
> Created a custom decorator file to handle simple unauthenticated user's redirection

## API
> It was created a new app to handle API requests. This app responds to simple requests with basic validation.

# INSTALLATION
> Requirements
- Python 3
- PIP 3

> requirements file
>>Use pip install to run the requirement files and have all the used libraries installed.
>>>Run $python manage.py makemigrations and $python manage.py migrate, to kick off your DB.
>>>Run $python manage.py createsuperuser, to create an initial super user and have access to the admin console

> If everything went right it's time to test the system
>> Run $python manage.py runserver 8000, and click on the link that will show up.
>> it will take you to the login page, feel free to login with the super user or create a new company.
>> For a better interaction with the system, you will need to go to the admin page (<link_on_the_console>/admin) an create some banks, accounts, etc


# Soon
- Added auto-populate db script
- Improve authentication on the API requests
- Improve security on the login
- create specific branches to show the evolution process


I hope it has been util.


--- Created By:
#####Rodrigo de Azevedo Carvalho
#####12/12/2020