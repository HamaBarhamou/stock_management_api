# Stock Management API  
This application is an API-based inventory management system created with Django and Django REST Framework. 

## Installation 
Clone the git repository in a local directory on your machine: 
```
git clone git@github.com:HamaBarhamou/stock_management_api.git
```
## Create a virtual environment for the project and activate it:
```
python3 -m venv venv
source venv/bin/activate
```
## Install the project dependencies:
```
pip install -r requirements.txt
```

## Create the database using the following command:
```
python manage.py migrate
```

## (Optional) To populate the database with initial data, you can run the provided data.py script: 
```
python manage.py runscript scripts.data.py -v2
```

# Usage  
## To start the development server, run the following command:  
```
python manage.py runserver
```


## API Documentation:  
[http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/) with redoc  
[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/) with swagger 
