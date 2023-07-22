# AskMe

## Description

The Quora-like Django app is a social question-and-answer platform designed to mimic the functionality of Quora. This web application provides users with the 
ability to create accounts, post questions, and answer questions posted by others. Additionally, users can like answers to show their appreciation for helpful 
responses.

# Getting Started

Create a new directory and switch to that directory

    $ mkdir ask-me
    $ cd ask-me
    
Clone the repository from Github:

    $ git clone git@github.com/Aniket-89/Ask-Me.git
    
Create a new virtual environment (Ignore if already created)

    $ pip install virtualenv
    $ virtualenv env
    
Activate the virtualenv for your project.

    $ env\scripts\activate
    
Install project dependencies:

    $ pip install -r requirements/base.txt
    
    
Then simply apply the migrations:

    $ python manage.py migrate
    

You can now run the development server:

    $ python manage.py runserver
