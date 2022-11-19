FROM python:3.8.6-slim

WORKDIR /app

COPY . .

RUN apt-get update && sudo apt-get install libmagic1
RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt --no-cache-dir

CMD ["gunicorn", "foodgram.wsgi:application", "--bind", "0:8000"]
