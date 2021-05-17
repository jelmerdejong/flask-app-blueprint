# syntax = docker/dockerfile:experimental

FROM tiangolo/uwsgi-nginx-flask:python3.7
COPY requirements.txt /tmp
RUN pip install --upgrade pip
RUN --mount=type=cache,mode=0755,target=/home/ubuntu/.cache/pip pip install -r /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt && \
	rm /tmp/requirements.txt    
RUN pwd && ls -al
COPY . /app
WORKDIR /app
ENV APP_SETTINGS=config.ProductionConfig
ENV SECRET_KEY=seckey
ENV SQLALCHEMY_DATABASE_URI=sqlite:///testcode.db

RUN python3 /app/manage.py db upgrade
ENV UWSGI_INI /app/uwsgi.ini
# custom static folder
ENV STATIC_PATH /app/project/static 
ENV UWSGI_BUFFER_SIZE=32768

# https://stackoverflow.com/questions/58018300/using-a-pip-cache-directory-in-docker-builds
