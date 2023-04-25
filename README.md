# exchange

this is a code challenge.

## Package Used list
```
Django==4.2
djangorestframework==3.14.0
django-environ==0.10.0
django-cors-headers==3.13.0
djangorestframework-recursive==0.1.2
djangorestframework-simplejwt==5.2.0
decorator==5.1.1
redis==4.5.4
gunicorn==20.1.0
```

## env variables
```
SECRET_KEY=abcdefghijklmnopqrstuvwxyz
MINIMUM_PER_PURCHASE=10
DEBUG=true
ADMIN_ENABLED=true
REDIS_HOST=localhost
REDIS_DB=0
REDIS_PORT=6379
AUTH_PREFIX=Bearer
AUTH_HEADER_TYPES=Bearer
```

## Test

1. test all
```
python manage.py test
```

2. user authentication
```
python manage.py test user.tests.UserTestCases.test_UserAuth
```

3.  user balance
```
python manage.py test balance.tests.BalanceTestCases.test_UserBalance
```

4. user order
```
python manage.py test order.tests.OrderTestCases.test_UserOrder
python manage.py test order.tests.OrderTestCases.test_MultipleUserOrder
```

## Run

1. build project
```
docker-compose build
```

2. start project
```
docker-compose up -d
```

3. check health
```
curl http://localhost:8000/api/v1/healthcheck/
```

4. import coin data from fixtures
```
python manage.py loaddata fixtures/*
```
