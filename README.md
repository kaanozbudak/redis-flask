# `Flask Key Value Application`

## Introduction

[core/helpers.py](./core/helpers.py) has Redis Helper 

[.gitignore](./.gitignore) stands for a text file that tells Git which files or folders to ignore in a project. 

[controllers/controller.py](./controllers/controller.py) stands for api controller methods 

[app.py](./app.py) stands for view handlers 


## Installation

### Local

Create virtual environment and activate it

    virtualenv venv/
    source venv/bin/activate

Install requirements 

    pip install -r requirements.txt

Make sure you have a working redis instance connection. 
You can install redis on your local or if you want to use redis as a docker container
    
    docker pull redis
    docker run -d -p 6379:6379 --name redis1 redis


### Docker

Make sure you have installed **docker** and **docker-compose**.

    docker-compose up -d --build 


## Test

    python -m unittest tests/test.py
