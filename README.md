Project Structure:

- dhbs: This is the parent directory of the Django project.
  - scripts: This directory contains the hash function script.
  - booking: This is the Django application used in the project.

Directories and Files:

1. dhbs:
   - This is the parent directory of the Django project.
   - It contains the main project settings, URLs, and WSGI configuration.

2. scripts:
   - This directory contains the hash function script.
   - parser2.py: This script is responsible for data distribution using a hash function. It takes data from the dataset and writes it to different databases using the hash function.

3. booking:
   - This is the Django application used in the project.
   - It contains models, views, templates, and other files related to the application.

Files in the booking Application:

- models.py: Defines the database models for the booking application.
- views.py: Contains the view functions for handling HTTP requests and rendering templates.
- urls.py: Defines URL patterns for the booking application.
- forms.py: Contains form classes for data validation and user input handling.
- admin.py: Registers models to be displayed in the Django admin site.
- templates/booking: This directory contains HTML templates used for rendering dynamic content.
- static: This directory contains static files such as CSS, JavaScript, and images used in the application.

Dataset:

- dataset: This is the file from which the hash function script retrieves data and writes it to different databases for data distribution.

Steps to Run the Project:

1. Run migrations to create the database schema:
   
   python3 manage.py makemigrations
   python3 manage.py migrate
  

2. Run the hash function script to distribute data:
   
   python3 manage.py runscript parser2
   

3. Start the Django development server:
 
   python3 manage.py runserver
  

Note:
- Ensure that the necessary dependencies are installed before running the Django project.
- Before running the hash function script, make sure the dataset file is available and correctly formatted.
