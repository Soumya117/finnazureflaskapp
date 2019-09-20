FROM tiangolo/uwsgi-nginx-flask:python3.6-alpine3.7
RUN apk update
RUN apk add libffi-dev libxml2-dev libxslt-dev openssl-dev
RUN pip3 install prometheus_client
RUN apk add make automake gcc g++ subversion python3-dev
RUN pip install flask_prometheus_metrics
RUN apk --update add bash vim
ENV STATIC_URL /static
ENV STATIC_PATH /var/www/app/static
COPY ./app/requirements.txt /var/www/requirements.txt
RUN pip install -r /var/www/requirements.txt