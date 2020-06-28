FROM python:3

WORKDIR /opt

COPY docker/ .

RUN pip install -r requirements.txt

CMD ["python", "webscraper.py"]