<table align="center"><tr><td align="center" width="9999">

<img src="https://advcloudfiles.advantech.com/cms/e3e079d5-76ec-4e2d-bbb0-030671ae2478/Content/content-image-1595228900162.jpg" align="center" width="200" alt="Project icon">

# Goblins MMO Server

*Massive Multiplayer Online Game Server API*
</td></tr>

</table>    

<div align="center">

> ![Version badge](https://img.shields.io/badge/version-0.0.2-silver.svg)

>![GraphQl Badge](https://badgen.net/badge/icon/graphql/pink?icon=graphql&label)
[![Docs Link](https://badgen.net/badge/docs/github_wiki?icon=github)](https://github.com/brunolcarli/Goblins-Server/wiki)
[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.com/cgi-bin/webscr?cmd=_donations&business=PPYA5P239NRML&currency_code=USD&source=url)
![docker badge](https://badgen.net/badge/icon/docker?icon=docker&label)

</div>

<hr />

This project implements a backend server for a tactics online multiplayer game. It is an open source experimental project. This service aims to store players data, like their position, lv, characters, and all game stuff that must be persistent. The server uses websockets based on GraphQL subscriptions to broadcast ingame events to all connected clients, like chat messages, player actions and all events that must be updated on the client side within the game environment. The server is supposed to be online and serving a GraphQL API so that the clients can write and read data through the API.

# Service configuration and execution


OS reference:

It is suggested to run this project on unix-like operating systems, example:

- Linux
- OSX (MacOS)

<hr />

Clone or download the project to a workspace directory of your preference:

```
$ git clone https://github.com/brunolcarli/Goblins-Server.git
```

## Run Local

> Follow this settings to manually run the service. For this method you might have some dependecies installed on your machine. If you dont wat to install any dependency on your machine, you may skip this section and run with Docker (instructions below on next topic).

Required dependencies:

- [Python3](https://www.python.org/) (suggested 3.9.9);
- [Python virtualenv](https://docs.python.org/3/tutorial/venv.html) (suggestion: [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/));
- [Redis-Server](https://redis.io/topics/quickstart);


### Setting up

First of all you must have the primary system dependencies mentioned above running, so if you dont have the previous stuff ready it is suggested to visit the mentioned technologies page and docs and find out how to install on your machine.

Export the environment reference variable to development:

```
$ export ENV_REF=development
```

Set up a python virtualenv, navigate to the project root and install the requirements through makefile inside the venv:

```
$ mkvirtualenv game_server
$ (game_server) make install
```

Now lets set the environment variables. There is a template file on `game_server/environment/local_template`, create a copy (or rename it) and change the variable values to the values of your preference (since it satisfies the dependencies). Example:

```
$ cp game_server/environment/local_template game_server/environment/local_env
```

Open the file and edit the `foo` values, changing to valid values for your environment, example:


*game_server/environment/local_env*
```
export SECRET_KEY=anythingHere
export DJANGO_SETTINGS_MODULE=game_server.settings.development
export REDIS_HOST=localhost
export REDIS_PORT=6379
```

Source the variables:

```
$ source game_server/environment/local_env
```

Run the migrations to create database tables:

```
$ make migrate
```

Finally run the web server, which should be available at: `http://localhost:11000/graphql/`

```
$ make run
```

<hr />

## Run with Docker

> Follow this instructions to run the service with Docker.

Required dependencies:

- Python3.x (suggested 3.9.9);
- Docker;
- docker-compose;



### Setting up

First of all you must have [Docker](https://www.docker.com/) installed. If you dont, go to docker docummentation and follow the installation guidelines for your Operating System. You will also need to install `docker-compose` which can be done through Python **pip**:

```
$ pip install docker-compose==1.29.2
```

Now lets set the environment variables. There is a template file on `game_server/environment/docker_template`, create a copy (or rename it) named **exactly** as `server_env`, this is required because docker-compose will look for a file named `server_env` in the directory `game_server/environment/`, thus you **must have** a `game_server/environment/server_env`. Use the template and change the variables values to the values of your preference (since it satisfies the dependencies). Example:

```
$ cp game_server/environment/docker_template game_server/environment/server_env
```

Edit the file changing the `foo` values with valid values for your environment, example:


*game_server/environment/server_env*
```
SECRET_KEY=anythingHere
MYSQL_DATABASE=my_database_name
MYSQL_USER=some_user
MYSQL_PASSWORD=some_password_for_mysql
MYSQL_ROOT_PASSWORD=root_password_for_mysql
MYSQL_HOST=game_server_db
DJANGO_SETTINGS_MODULE=game_server.settings.production
REDIS_HOST=redis
REDIS_PORT=6379
```

**IMPORTANT**: The values for the variables `MYSQL_HOST` and `REDIS_HOST` **must be the same name defined on docker-compose service_name**, at the moment this text is been written, the service name for the MySQL database is defined as `game_server_db` and the Redis service is defines simply as `redis` so, these are the values you **must use**.

![docker-compose services](https://i.ibb.co/QDChxrB/dockercomposeprint.png)


Also, when running with Docker, the `DJANGO_SETTINGS_MODULE` **must always be** `game_server.settings.production`

**HINT**: Never set variables to `localhost` when running with Docker, instead use the raw IP of the machine.

#### Build and run

On the project root, build the service container and run it with:

```
$ make run_docker
```


The API should be available at `http://localhost:11000/graphql/`

<hr />

## Check API response

You may test the API response by requesting the simple version query:

- Example with **Python**:

```py
>>> import requests
>>> url = 'http://localhost:11000/graphql/'
>>> response = requests.post(url, json={'query': '{version}'})
>>> response.json()
{'data': {'version': '0.0.2'}}
>>>
```

- Example with **curl**:

```
$ curl -X POST -H "Content-Type: application/json" --data '{ "query": "{version}" }' http://localhost:11000/graphql/
{"data":{"version":"0.0.2"}}
```

# More information

Take a look at this repository [wiki](https://github.com/brunolcarli/Goblins-Server/wiki) for more detailed information and the API reference containing the available endpoints (query and mutation for GraphQL) and usage examples.