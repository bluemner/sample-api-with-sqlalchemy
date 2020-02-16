# Sample Application
This is a demo of flask, flask rest-plus and SqlAlchmey database

* [Folder Structure](#Folder-Structure)
    * [API](#API)  
        * [Endpoint](#Endpoint)
        * [Swagger](#Swagger)
    * [Data](#Data)
        * [Data Access](#Data-Access)
        * [Data Models](#Data-Models)
    * [Domain](#Domain)
* [Running](#Running)
* [Python Virtual Environment](#Python-Virtual-Environment)

# Folder Structure

Here is a folder structure that works, and is an attempt to break concepts up. 
```
├── sample
│   ├── api
│   │   ├── auth.py
│   │   ├── endpoints
│   │   │   ├── __init__.py
│   │   │   ├── person.py
│   │   │   └── status.py
│   │   ├── __init__.py
│   │   ├── restplus.py
│   │   └── swagger
│   │       ├── __init__.py
│   │       ├── factory.py
│   │       └── status.py
│   ├── app.py
│   ├── data
│   │   ├── access
│   │   │   ├── accessible.py
│   │   │   ├── __init__.py
│   │   │   └── person.py
│   │   ├── __init__.py
│   │   └── models
│   │       ├── __init__.py
│   │       ├── model.py
│   │       └── person.py
│   ├── __init__.py
│   └── settings.py
├── README.md
├── requirements-dev.txt
├── requirements.txt
├── run.py
└── test
    ├── api
    │   All tests can go here
    └── __init__.py

```


## API
Flask rest plus logic will go here as well as an auth
* [Endpoint](#Endpoint)
* [Swagger](#Swagger)

### Endpoint
Endpoints are the Restful endpoints.

### Swagger
Swagger Folder has the flask rest plus model definitions.
Factory will auto generated.

## Data
Data folder will allow interface to different information sources and data structures.
* [Data Access](#Data-Access)
* [Data Models](#Data-Models)

### Data Access
Data Access Layer used to interface between different data source. Examples are database, AWS services, Azure services etc.

### Data Models
Models use for SQlAlchemy

## Domain 
One folder below the `root` aka `sample` in this example would be `domain` which would house logic that could be unit tested with invoking flask. 

> Try to avoid data access calls in the domain. Any data needed can be an argument of the function

A good example could be like:
```python 
    def sum_up_money(money:List[float])->float:
        """ 
        """
        return sum(money)
```
Try to avoid this kind of setup.

```python 
    def sum_up_money(user_account_access: Access)->float:
        """ 
        """
        money: List[float] = user_account_access.get_money_from_accounts()
        return sum(money)
```

Why you may ask? The first function does one thing, the second does two thing. gets the data then sums it up.

With a unit test you now have to test two concepts vs just one. 



# Running


## Local 

To get the application running you can 

### Flask built in run

This will call `flask_application.run(...)` and should not be used in production
```shell
    python3 run.py
```
### Gunicorn 
This mode runs Gunicorn with some default settings, and can be used in a 
production, please update default information in settings.

This method is calling `__main__.py` which can be accessed from the `python3 -m` 
command, sample after the `-m` is the folder which should match the name in the 
setup.py. This means sample api application could be published to pip as a pip module. 


```shell
    python3 -m sample
```
> [Gunicorn](https://en.wikipedia.org/wiki/Gunicorn) is an implementation for a [Web Server Gateway Interface(WSGI)](https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface)

# Python Virtual Environment

It is a good idea to Use Python Virtual Environment to prevent versions issue between software stacks

## Linux (Aptitude)

Install python3.7
> You can change the version to what your project needs, and install multiple versions

* Install
    ```bash 
    sudo apt update
    sudo apt upgrade
    sudo apt install -y python3.7-venv
    ```

* Change directory to folder
    ```base
    cd /path/to/project
    ```

* Enable Virtual Environment
    ```bash
    python3 -m venv .venv
    ```
* Each bash window will need to:
    ```bash
    source /srv/git/<project>/.venv/bin/activate
    ```
* Extra packages
    ```bash
    pip3 install python-dateutil
    ```