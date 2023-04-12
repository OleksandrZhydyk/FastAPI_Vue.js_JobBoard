FROM python:3.10

RUN apt update

RUN mkdir "backend"

WORKDIR /backend

COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock

RUN python -m pip install --upgrade pip
#RUN pip install -r ./requirements.txt
RUN pip install pipenv
RUN pipenv install --system --deploy

COPY ./src ./src
COPY ./commands ./commands
RUN chmod a+x ./commands/start_server.sh

CMD ["bash"]