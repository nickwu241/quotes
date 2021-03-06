FROM tiangolo/uwsgi-nginx-flask:python3.6

WORKDIR /app
COPY quotes quotes
COPY static static
COPY app.py messenger.py ./

CMD ./app.py
