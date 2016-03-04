FROM python:2.7-onbuild

RUN apt-get update && apt-get install -y ruby-compass
RUN compass compile -c themes/simple/scss/config.rb
RUN nikola build

CMD ["twistd", "-n", "web", "--port", "80", "--path", "/usr/src/app/output"]
