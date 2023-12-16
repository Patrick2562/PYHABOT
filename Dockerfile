FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

COPY classes ./classes
COPY integrations ./integrations
COPY run.py .

CMD ["python3", "-u", "/app/run.py", "telegram"]
