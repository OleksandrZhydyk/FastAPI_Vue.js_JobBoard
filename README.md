# FastAPI Job Board

Job board application powered by FastAPI. 
The main goal of this is to learn FastAPI, Vue 
frameworks and correspond tech stack for building the complete app.


The app features:
> All unregistered users in the app can:
1) search for the necessary vacancies using filter by categories and sort them;
2) view the full information about the vacancy;

> Registered users in the app can:
1) All the steps above;
- Applicant:
  - apply for the vacancy;
  - view applied vacancies;
  - edit profile (photo, resume).
- Employer:
  - CRUD of the vacancy;
  - view own archived vacancies;
  - view applicants profiles for vacancies;
  - edit profile.

## Used technologies:
* FastAPI;
* PostgreSQL;
* SQLAlchemy;
* Alembic;
* Pytest;
* Docker, Docker Compose;
* Vue.js;
* AWS S3;
* Nginx

## Installation

1. Clone the repo:
```sh
https://github.com/OleksandrZhydyk/FastApiPractic_JobBoard.git
```

## Usage

For running the app you need:

1. Add app configuration to your .env files in the root of the services:
* backend .env
```sh
#Block FastAPI settings
HOST_NAME=YOUR_HOST_NAME
WSGI_PORT=YOUR_WSGI_PORT
ROOT_PATH=YOUR_FASTAPI_ROOT_PATH
SECRET_KEY=YOUR_SECRET_KEY
ALGORITHM=ALGORITHM_FOR_JWT
ACCESS_TOKEN_EXPIRE_SECONDS=SECONDS
REFRESH_TOKEN_EXPIRE_SECONDS=SECONDS
COOKIE_MAX_AGE=SECONDS

#Block DB connection
POSTGRES_DB=YOUR_POSTGRES_DB
POSTGRES_PASSWORD=YOUR_POSTGRES_PASSWORD
POSTGRES_USER=YOUR_POSTGRES_USER
POSTGRES_HOST=YOUR_POSTGRES_HOST
POSTGRES_PORT=YOUR_POSTGRES_PORT

#Block for S3 as media files manager
AWS_ACCESS_KEY=YOUR_AWS_ACCESS_KEY_FOR_S3
AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_FOR_S3
AWS_STORAGE_BUCKET_NAME=YOUR_AWS_BUCKET_NAME
AWS_MEDIA_LOCATION=YOUR_PATH_TO_AWS_MEDIA_LOCATION
AWS_USER_AGENT=SOME_SECRET_FOR_NGINX,S3_COMMUNICATION

#Block for local system as media files manager
STATIC_ROOT = YOUR_STATIC_ROOT
ORIGIN = YOUR_ORIGIN

USE_S3='True'-FOR_S3_MEDIA_SAVING, ''-FOR_SYSTEM_SAVING
```

* frontend .env
```sh
#Base url for axios
VUE_APP_BACKEND=YOUR_HOST+YOUR_ROOT_PATH
```

2. Run the command for building and running the images:
```sh
docker compose up -d --build
```


## TODO
- [x] Integrate Alembic migrations
- [x] Async CRUD and main business logic
- [x] Login and permissions 
- [x] Integration async tests (Pytest)
- [x] Add CI (GitHub Actions)
- [x] Add docker compose support
- [x] Make Vue.js frontend
- [x] S3 bucket for media files
- [x] Nginx support
