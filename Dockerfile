FROM tiangolo/uwsgi-nginx-flask:python3.6

WORKDIR /app
COPY app.py quotes.json ./

CMD ./app.py