FROM python:3

WORKDIR /usr/src/app

ARG PORT
ARG MAX_FILE_LENGTH
ARG TIMEOUT

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt /usr/src/app/requirements.txt
RUN pip install -r requirements.txt

COPY . /usr/src/app/

EXPOSE ${PORT}

CMD ["python", "server.py"]