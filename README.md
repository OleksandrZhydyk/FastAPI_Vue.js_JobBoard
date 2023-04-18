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
* Vue.js, Vuex, Vue Router;
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
LOCAL_ORIGIN = YOUR_ORIGIN

USE_S3='True'-FOR_S3_MEDIA_SAVING, ''-FOR_SYSTEM_SAVING
```

* frontend .env
```sh
#Base url for axios
VUE_APP_BACKEND=YOUR_HOST+YOUR_ROOT_PATH
```

2. Run the command for building and running the images in prod mode:
```sh
docker compose up -d --build
```
> For running in dev mode use docker-compose-dev.yml. 


## TODO
- [x] Integrate Alembic migrations
- [x] Async CRUD and main business logic
- [x] Login and permissions 
- [x] Integration async tests (Pytest)
- [x] Add CI (GitHub Actions)
- [x] Add docker compose support
- [x] Make Vue.js, Vuex, Vue Router
- [x] S3 bucket for media files
- [x] Nginx support


![Screenshot from 2023-04-16 11-05-02](https://user-images.githubusercontent.com/108074767/232284619-60cd9383-0106-4686-a247-142c1746fb6e.png)

![Screenshot from 2023-04-16 10-57-56](https://user-images.githubusercontent.com/108074767/232284775-ba8cccfb-82c0-4222-9af2-691d3d9a02fc.png)

![Screenshot from 2023-04-16 10-58-26](https://user-images.githubusercontent.com/108074767/232284996-6a42b9d5-38b9-44f7-8626-4c04616086a8.png)

![Screenshot from 2023-04-16 10-58-46](https://user-images.githubusercontent.com/108074767/232284838-14b4a97e-15de-4745-a8cc-d823b80d3f35.png)

![Screenshot from 2023-04-16 11-01-31](https://user-images.githubusercontent.com/108074767/232285181-d3c913ec-00ed-48d1-a518-3e8e9f9c2b93.png)
