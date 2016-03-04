FROM aldryn/base:3

RUN apt-get update && apt-get install -y ruby-compass

WORKDIR /app

ADD requirements.txt /app/requirements.txt

RUN pip install -r /app/requirements.txt

ADD . /app

RUN compass compile -c themes/simple/scss/config.rb
RUN nikola build
