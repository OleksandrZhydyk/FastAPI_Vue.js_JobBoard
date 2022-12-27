FROM python:3.10

RUN apt update

RUN mkdir "fastApiProject"

WORKDIR /fastApiProject

COPY ./src ./src
COPY src/main.py ./main.py
COPY ./Pipfile ./Pipfile
COPY ./Pipfile.lock ./Pipfile.lock
COPY ./commands ./commands

RUN python -m pip install --upgrade pip
#RUN pip install -r ./requirements.txt
RUN pip install pipenv
RUN pipenv install --system --deploy

CMD ["bash"]