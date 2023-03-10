# stock_management_api
Webstack - Portfolio Project

```
git clone git@github.com:HamaBarhamou/stock_management_api.git
cd stock_management_api
python3 -m venv env
source env/bin/activate
pip install -r requirement.txt
python manage.py migrate 
python manage.py createsuperuser 
python manage.py runserver
curl -H 'Accept: application/json; indent=4' -u admin:password123 http://127.0.0.1:8000/users/
```

##Find all documented termination points here: 
[http://127.0.0.1:8000/api/schema/redoc/](http://127.0.0.1:8000/api/schema/redoc/) with redoc 
[http://127.0.0.1:8000/api/schema/swagger-ui/](http://127.0.0.1:8000/api/schema/swagger-ui/) 