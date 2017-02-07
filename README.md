# API for control work time

## About
##### Using this API you can:
1. Start work (with marking work start time)
2. Stop work (with marking work stop time)


##### Superuser can:
1. Get a report with time periods and its workers.
2. Apply sorts and filters to the report.

## How to use?

### 1. Sign Up
You can use **curl** or **httpie** (for instance).

API request:
```
http POST http://80.87.200.153:1234/api/register/ username=test_api_user password=123qweQWE first_name=Тест last_name=Тестовый email=test@test.ru
```
Server response:


```
HTTP/1.0 201 Created
Allow: POST, OPTIONS
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:20:48 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

{
    "email": "test@test.ru",
    "first_name": "Тест",
    "id": 12,
    "last_name": "Тестовый",
    "username": "test_api_user"
}
```

### 2. Get authtoken

API request:
```
http POST http://80.87.200.153:1234/get-api-token/ username=test_api_user password=123qweQWE
```
Server response:


```
HTTP/1.0 200 OK
Allow: POST, OPTIONS
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:21:02 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept-Language, Cookie

{
    "token": "e4db4166d855319762c8484aa5071ec3a47a9f8d"
}
```

### 3. Use API

```
http POST http://80.87.200.153:1234/api/start-work/ 'Authorization: Token  e4db4166d855319762c8484aa5071ec3a47a9f8d'

HTTP/1.0 201 Created
Allow: POST
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:22:48 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

"Тест Тестовый. Работа началась 07.02.17 в 10:22:48"
```

```
http POST http://80.87.200.153:1234/api/stop-work/ 'Authorization: Token  e4db4166d855319762c8484aa5071ec3a47a9f8d'

HTTP/1.0 201 Created
Allow: POST
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:23:15 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

"Тест Тестовый. Работа началась 07.02.17 в 10:22:48. Закончилась в 07.02.17 в 10:23:15"
```

```
http POST http://80.87.200.153:1234/api/stop-work/ 'Authorization: Token  e4db4166d855319762c8484aa5071ec3a47a9f8d'


HTTP/1.0 428 Precondition Required
Allow: POST
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:23:40 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

"Тест, чтобы закончить работу, её нужно сначала начать"
```

## Superuser options

##### Possible parameters:
 1. **sort_by** - sort by *day(d)*, *month(m)* **and/or** *year(y)*
 2. **by_day_week** - filter by day week *(sun, mon, tue, wed, thu, fri, sat)*
 3. **by_day** - filter by day number *(1-31)*
 4. **by_month** - filter by month *(jan, feb, mar, apr, may, jun, jul, aug, sep, oct, nov, dec)*
 5. **by_year** - filter by year *(i.e. 2014, 2016)*


#### Examples:

##### Without params: 
```
http GET http://80.87.200.153:1234/api/report/ 'Authorization: Token  ************************************'


HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:43:06 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

{
    "count": 35,
    "next": "http://80.87.200.153:1234/api/report/?page=2",
    "previous": null,
    "results": [
        {
            "comment": null,
            "end": "2014-02-04T15:58:16Z",
            "start": "2014-02-04T13:58:16Z",
            "user": 12
        },
        {
            "comment": null,
            "end": "2015-12-05T16:55:08Z",
            "start": "2015-12-05T11:11:08Z",
            "user": 10
        },
        {
            "comment": null,
            "end": "2014-05-14T02:06:15Z",
            "start": "2014-05-13T19:46:15Z",
            "user": 9
        },
        ....
        {
            "comment": null,
            "end": "2016-05-29T06:31:12Z",
            "start": "2016-05-28T20:31:12Z",
            "user": 7
        },
    ]
}
```

##### Sort by date, filter by Monday: 
```
http GET http://80.87.200.153:1234/api/report/?sort_by=dmy&by_week_day=mon 'Authorization: Token  ************************************'

HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:44:50 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

{
    "count": 35,
    "next": "http://80.87.200.153:1234/api/report/?page=2&sort_by=dmy",
    "previous": null,
    "results": [
        {
            "comment": null,
            "end": "2014-01-29T02:27:50Z",
            "start": "2014-01-28T18:27:50Z",
            "user": 6
        },
        {
            "comment": null,
            "end": "2014-01-29T08:27:50Z",
            "start": "2014-01-29T01:27:50Z",
            "user": 4
        },
        {
            "comment": null,
            "end": "2014-02-04T15:58:16Z",
            "start": "2014-02-04T13:58:16Z",
            "user": 12
        },
        .....
        {
            "comment": null,
            "end": "2016-05-29T06:31:12Z",
            "start": "2016-05-28T20:31:12Z",
            "user": 7
        }
    ]
}
```

##### Sort by date, filter by June: 

```
http GET http://80.87.200.153:1234/api/report/?sort_by=dmy\&by_month=jun 'Authorization: Token  ************************************'

HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:46:19 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

{
    "count": 2,
    "next": null,
    "previous": null,
    "results": [
        {
            "comment": null,
            "end": "2014-06-14T04:40:05Z",
            "start": "2014-06-13T20:40:05Z",
            "user": 8
        },
        {
            "comment": null,
            "end": "2016-06-26T06:54:35Z",
            "start": "2016-06-26T05:14:35Z",
            "user": 4
        }
    ]
}
```

##### Sort by date, filter by December 2016: 

```
http GET http://80.87.200.153:1234/api/report/?sort_by=dmy\&by_month=dec\&by_year=2016 'Authorization: Token  ************************************'

HTTP/1.0 200 OK
Allow: GET, HEAD, OPTIONS
Content-Language: ru
Content-Type: application/json
Date: Tue, 07 Feb 2017 10:46:44 GMT
Server: WSGIServer/0.2 CPython/3.4.3
Vary: Accept, Accept-Language, Cookie

{
    "count": 1,
    "next": null,
    "previous": null,
    "results": [
        {
            "comment": null,
            "end": "2016-12-10T10:15:34Z",
            "start": "2016-12-10T00:15:34Z",
            "user": 10
        }
    ]
}
```

