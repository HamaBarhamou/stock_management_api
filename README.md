# Stock Management API  
This application is an API-based inventory management system created with Django and Django REST Framework. 
Stock Management API is an inventory management system built using Django and Django REST Framework. This API provides a  
comprehensive set of endpoints for managing stocks, products, and orders. It was created as a collaborative project by the team  
members (Issaka Hama Barhamou, Djogona Mahamat Belna, Mellanie Achieng Oduori, and Rodrigue Mbiaha) as a final project for the  
ALX-Holberton School program. With this API, users can easily manage their inventory, track stock levels, and analyze sales data,  
among other functions.

## Installation 
Clone the git repository in a local directory on your machine: 
```
git clone git@github.com:HamaBarhamou/stock_management_api.git
cd stock_management_api
```
## Create a virtual environment for the project and activate it:
```
python3 -m venv venv
source venv/bin/activate
```
## Install the project dependencies:
```
pip install -r requirement.txt
```

## Create the database using the following command:
```
python manage.py migrate
```

## (Optional) To populate the database with initial data, you can run the provided data.py script: 
```
python manage.py runscript scripts.data.py -v2
```

## Create a user
```
python manage.py createsuperuser
```


# Usage  
## To start the development server, run the following command:  
```
python manage.py runserver
```
Go to  
[http://127.0.0.1:8000](http://127.0.0.1:8000)  
[http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/) administration page  

## API Documentation:  
[http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/) with redoc  
[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/) with swagger 
