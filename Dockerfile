FROM python:3

WORKDIR /opt

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY docker/ .

CMD ["python", "main.py"]