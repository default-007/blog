# blog
# [blog](https://blog-pitch.herokuapp.com/)
## blog  is a flask application that is meant for users to add pitches on 7 different categories

#### By **[Brian Otieno](https://github.com/default-007)**

## Description
The blog web application is meant for users to post pitches on any of the 7 different categories. These categories are:

    1. Interview Pitch
    2. Product Pitch
    3. Promotion Pitch
    4. Business
    5. Academic
    6. Political
    7. Technology
    8. Health

A user can select any of the categories from the navbar to view the pitches on these categories

Other users can give feedback to the pitch posts by commenting, liking or disliking the pitch. 


## BDD

| Behavior            | Input                         | Output                        | 
| ------------------- | ----------------------------- | ----------------------------- |
| Signing up | Fill in the form in the signup page | Redirects to the login page |
| Signing in | Fill in the form in the signin page | Redirects to the home page |
| Posting a pitch | In the home page, enter your pitch in text, select a category in the drop down menu and hit Pitch It Button! | Reloads the page with the pitch as the newest pitch |
| Liking a pitch | Press the thumbs up button | Redirects the user to the specific pitch, and the like counter goes to 1 |
| Disliking a pitch | Press the thumbs down button | Redirects the user to the specific pitch, and the dislike counter goes to 1 |
| Leaving feedback on the pitch | Type the feedback on the text area field in the pitch page, and hit post comment | Reloads the page and posts the feedback. The comments will be shown from the most recent |
| Viewing user profile | Click on the users name | Redirects the user to the clicked user profile |
| Uploading a photo | Click on the choose file button and choose file | The page will be refreshed with the profile photo updated |
| Editing the bio | Click on the ```edit bio``` button and enter your bio  | Redirects the page back to the profile page with an updated bio |


## Live link

https://blog-pitch.herokuapp.com/

## Set-up and Installation

### Prerequsites
    - Python 3 or later version
    - pip 
    - flask

### Clone the Repo
Run the following command on the terminal:
`https://github.com/default-007/blog.git`

Install [Postgres](https://www.postgresql.org/download/)

### Create a Virtual Environment
Run the following commands in the same terminal:
`sudo apt-get install python3.6-venv`
`python3.6 -m venv virtual`
`source virtual/bin/activate`

### Install dependancies
Install dependancies that will create an environment for the app to run
`pip3 install -r requirements`

### Prepare environment variables
```bash
export DATABASE_URL='postgresql+psycopg2://username:password@localhost/pitchit'
export SECRET_KEY='Your secret key'
```

### Run Database Migrations
```
python manage.py db init
python manage.py db migrate -m "initial migration"
python manage.py db upgrade
```

### Running the app in development
In the same terminal type:
`python3 manage.py server`

Open the browser on `http://localhost:5000/`

## Known bugs

```None so far but i'll be glad to be communicated to if there is one ```


## Technologies used
    - Python 3.6
    - HTML
    - Bootstrap 4
    - Animate CSS
    - Heroku
    - Postgresql

## Support and contact details
Contact me on brianokola@gmail.com for any comments, reviews or advice.

### License
Copyright (c) **Brian Otieno**
