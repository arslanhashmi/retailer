# Retailer Demo App

This provides RESTful retailer API.

## Major Requirements:

- Python 3.7
- Django 2.1
- Django Rest Framework 3.8

Please have a look at `requirements.txt` for list of all the project dependencies.

## Installation

Please run the following command to setup Retailer App locally
```sh
$> curl https://gist.githubusercontent.com/Qubad786/ab8d5dc5f90d0e7569c290e05972ab0e/raw/432094369c2229a2768d3487d9f10f22217a4455/setup.sh > setup.sh
$> bash setup.sh
```

Now, you should be able to play with the app @ `localhost:8080`.

You will need to create a super user in order to log into the Django Administration Console @ `localhost:8080/admin` to add products/categories/users etc.
```sh
# SSH into the rtailer web container and run createsuperuser 
# management command to setup an admin user.

$> docker exec -it rtailer.web /bin/bash
$> python manage.py createsuperuser
```

## API Docs

API documentation can be found [here](https://documenter.getpostman.com/view/985924/RWaLwnnk) and Postman collection containing the API endpoints can be found [here](https://www.getpostman.com/collections/144654fe5193f6e55cbb), this can be imported into your Postman client directly.


--
Thank you!