FROM python:3.8-slim

WORKDIR /app

COPY requirements.txt .

RUN python -m pip install --upgrade pip

RUN pip3 install -r requirements.txt --no-cache-dir

COPY blackfox/ .

CMD ["gunicorn", "blackfox.wsgi:application", "--bind", "0:8000"]
