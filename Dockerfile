FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --user -r requirements.txt

CMD ["sh", "-c", "python3 -u /app/run.py"]
