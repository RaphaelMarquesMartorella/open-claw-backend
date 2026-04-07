FROM python:3.12.3-slim

WORKDIR /app

ADD ./app /app

COPY ./requirements.txt /etc

RUN pip install -r /etc/requirements.txt

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
