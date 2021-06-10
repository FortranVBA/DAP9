# LITReview MVP: Book review application

LITReview is a MVP (Minimal Viable Product) application to be executed locally in the context of OpenClassroom educational project. 
It allow registered users to ask for book reviews, post book reviews and reply to book review requests with a system of following other users from the community.
This application has been developed with the Django framework, using SQlite database.
As MVP purpose, a SQlite database with precreated users and reviews is included with the application.

## Warning

This application is intented for local execution and shall not be used as such in production !
The current image upload system is not designed to prevent malicious file upload to the server.

## Installation and first launch

This locally-executable application can be installed and executed from [http://localhost:8000/](http://localhost:8000/) using the following steps.

1. Clone this repository using $ git clone `https://github.com/FortranVBA/DAP9.git` (you can also download the code using [as a zip file](https://github.com/FortranVBA/DAP9/archive/refs/heads/main.zip))
2. Move to the application root folder.
3. Create a virtual environment for the project with `$ py -m venv .venv` on windows or `$ python3 -m venv .venv` on macos or linux.
4. Activate the virtual environment with `$ .venv\Scripts\activate` on windows or `$ source .venv/bin/activate` on macos or linux.
5. Install project dependencies with `$ pip install -r requirements.txt`
6. Run the server with `$ python manage.py runserver`

When the server is running after step 6 of the procedure, the LITReview application can be used with the following base URL: http://localhost:8000/.


## Usage with user profiles

For subsequent launches of the application, you only have to execute the following steps from the root folder of the project:
1. Activate the virtual environment with `$ .venv\Scripts\activate` on windows or `$ source .venv/bin/activate` on macos or linux.
2. Run the server with `$ python manage.py runserver`

Once you have launched the server, the main application entry point can be reached by visiting [http://localhost:8000/](http://localhost:8000/).

You can either register as a new user, or use one of the already created users:
-	Username: aze ; Password: a1z2e3r4
-	Username: azer ; Password: a1z2e3r4
-	Username: jean_5679 ; Password: a1z2e3r4
-	Username: sarahj ; Password: a1z2e3r4
-	Username: severine123 ; Password: a1z2e3r4

## Admin panel

Once you have launched the server, the Django default admin panel can be reached by visiting [http://localhost:8000/admin/](http://localhost:8000/admin/).

The super user admin has the following login:
-	Username: admin ; Password: admin
