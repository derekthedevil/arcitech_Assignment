# Amazon and Ecom Platform

A comprehensive e-commerce platform built with Django, inspired by Amazon. This platform includes user authentication, product listings, shopping cart functionality, order processing, and payment integration.


## Features

- User authentication and profile management
- Product listings with categories and search functionality
- Shopping cart and checkout process
- Order management
- Payment gateway integration
- Admin dashboard for managing products
- Responsive design for mobile and desktop

## Installation


### Prerequisites

- Python 3.x
- Django 3.x or higher
- MYSQL (or your preferred database)

### Steps

1. **Clone the repository:**
   ```
   git clone https://github.com/derekthedevil/arcitech_Assignment.git
   ```
   ```
   cd amazon
   ```

2. **Install requirements :**
    ```
    pip install -r requirements.txt
    ```

3. **Setup enviromental variables:** 
    
    create a .env file 
    setup the following variables :
    - SECRET_KEY:
    - DATABASE_NAME:
    - DATABASE_USER:
    - DATABASE_HOST :
    - DATABASE_PORT :
    - DATABASE_PASSWORD:
    - SECRET_KEY :
     
     ** Note 
     to generate your own secret key use function located at 
     - django.core.management.utils.get_random_secret_key()

3. **createsuperuser:** 
    ```
    cd amazon
    ``` 
    ```
    python manage.py createsuperuser 
    ```

    - enter the requreied prompts 

4. **deploy** 
    ``` 
    python manage.py runserver