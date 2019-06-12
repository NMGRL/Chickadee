FROM python:3.7-alpine

RUN apk add --no-cache gcc musl-dev linux-headers nginx supervisor

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY nginx.conf /etc/nginx/
COPY flask-site-nginx.conf /etc/nginx/conf.d/
COPY uwsgi.ini /etc/uwsgi/
COPY supervisord.conf /etc/

COPY /app /project
WORKDIR /project


# for production
CMD ["/usr/bin/supervisord"]

# for development only
#ENV PYTHONPATH /project
#CMD ["python", "app/wsgi.py"]