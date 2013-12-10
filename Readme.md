
I opted for different API responses and url format for the system. I assume that server is running at [http://battle.harpb.com/](http://battle.harpb.com/) to provide clickable urls.

# Install
Requirements:

- python-mysqldb
- npm
- nodejs
- nginx

Specific for Ubuntu machine:

1. Clones the githup repository and install pip requirements. 
    > fab prod setup
2. Uses apt-get to install system level modules and then pip for python modules 
    > fab prod build_pyenv
3. Run django migrations and then runs nginx with django under gevent
    > fab prod refresh




# Api Urls
The specification has `POST /users/<userid>` as an API endpoint while `GET /users/<userid>` as a webapp, which is overloading the endpoint with responsibility. I believe in separating out api and application endpoints.

All of the api endpoints are available via the `/api/` endpoint. The battle api has versioning. The currently version is 1, so the api endpoint is `/api/v1/`. Rather than `user`, the client is called a `player`. The player api is available via `/api/v1/player/`.

1. Battles
    - List: [`/api/v1/battle/`](http://battle.harpb.com/api/v1/battle/)
    - By id: [`/api/v1/battle/1/`](http://battle.harpb.com/api/v1/battle/1/)
    - Started AFTER Dec. 10, 2013: [`/api/v1/battle/?start__gte=2013-12-10`](http://battle.harpb.com/api/v1/battle/?start__gte=2013-12-10)
	- Ended Before Dec. 11, 2013: [`/api/v1/battle/?end__lte=2013-12-11`](http://battle.harpb.com/api/v1/battle/?end_lte=2013-12-11)
	- On Dec. 10 2013:  [`/api/v1/battle/?start__gte=2013-12-10&end__lte=2013-12-11`](http://battle.harpb.com/api/v1/battle/?start__gte=2013-12-10&end_lte=2013-12-11)
2. Players
	- List: [`/api/v1/player/`](http://battle.harpb.com/api/v1/player/)
	- By id: [`/api/v1/player/1/`](http://battle.harpb.com/api/v1/player/1/)
	- Filter by nickname: [`/api/v1/player/?nickname=harp`](http://battle.harpb.com/api/v1/player/?nickname=harp)

## Create and Update
When an object created successfully via `POST`, the return status code is `201`. The specification has `PUT /users/<userid>`, which is not appropriate for our use case. In a PUT, client is require to provide all fields. If a field is not provided, the form results in an error. I opted to use `PATCH /api/v1/player/<id>/`, which means only the specified field will be updated with the provided value and other fields are untouched.

## Handling Errors
The specification says to include in the response if there was an error or not without exposing the actual error. In an API, the error should be indicated via status_code. This allows HTTP clients to provide existing mechanism to handle success and error of a POST and PATCH.

# Angular webapp

1. Shows battles and players stats using the API.
2. Create a new battle and player via the App usin the API		
3. Form validation is done on the backend using Django form and the API returns the errors, which are displayed on the front-end
		

# Django App
1. The player's stats are available via `/player/<id>/` rather than `/users/<userid>`. I am just using Django (not API or AngularJS app) in order to show my ease with using Django for presenting data - [`/player/1/`](http://battle.harpb.com/player/1/)

2. To search by nickname: [`/player/search/?nickname=harp`](http://battle.harpb.com/player/search/?nickname=harp). If the user does not exists or nickname is not provided, redirect to battle dashboard.
3. There is no endpoint to display battle logs for a specified time range because the functionality is available via dashboard and API.
		

# Testing
1. To run all tests, following pattern must be specified:
    > $ python manage.py test -p *tests.py
