FROM python:3.8-slim

WORKDIR /app

COPY pizza.py /app

COPY requirements.txt /app

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5000

ENV FLASK_APP=pizza.py

CMD ["flask", "run", "--host=0.0.0.0"]
