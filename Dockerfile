FROM python:3.7-alpine

#ENV FLASK_APP app.py
#ENV FLASK_RUN_HOST 0.0.0.0
#ENV STATIC_URL /static
#ENV STATIC_PATH /app/static

RUN apk add --no-cache gcc musl-dev linux-headers nginx supervisor

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

#RUN rm /etc/nginx/sites-enabled/default
RUN rm -r /root/.cache

COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

COPY /app /project
WORKDIR /project

CMD ["/usr/bin/supervisord"]
#EXPOSE 80 443
#CMD ["flask", "run"]
