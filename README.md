# How to get this up and running

- Please make sure that you are using python3.8 as your interpreter. (If I had enough time I would dockerize this 
project. I hope you can run it without any problems)

- Create a .env file for your environment variables (required variables are SECRET_KEY, DEBUG, ACCESS_TOKEN_LIFETIME, 
REFRESH_TOKEN_LIFETIME and DEVEL)

- Install requirements (i.e. ```pip install -r requirements.txt```)

- Create project's tables (i.e. ```python manage.py makemigrations``` and ```python manage.py migrate```)

- Running tests (i.e ```python manage.py test```)

- For using APIs, use "Bearer" as your authorization header key (because I used simple jwt for authentication)

- For obtaining access and refresh tokens please use obtain and refresh token APIs
(http://running-host/api/v1/accounts/token/obtain/ and http://running-host/api/v1/accounts/token/refresh/)

- For creating a super user use ```python manage.py createsuperuser```

- For checking documentation of APIs please go to http://running-host/api/v1/docs/
