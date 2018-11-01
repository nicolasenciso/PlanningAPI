FROM python:3.6-stretch

RUN mkdir /planning_ms

WORKDIR /planning_ms

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

CMD ["python", "api.py"]

EXPOSE 3002
