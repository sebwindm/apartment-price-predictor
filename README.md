# Project overview:

The apartment price predictor scrapes apartment offerings from the web and allows the user to predict the price/rent for an apartment, given certain features like number of rooms and the size of the apartment.

Production ready project components:
* Webscraper (Python): done
* Database (PostgreSQL) and docker host setup: done
* Database cleanup script (Python) (to remove duplicates after scraping): done
* Price prediction (Python): done (currently using linear regression, at some later point maybe a neural network)


To do until release:
* Front end (HTML/CSS): 70% done
* Back end/web server (Django): 1% done


Planned improvements after release:
* prediction using a neural network
* more input features other than living area and price
* more cities


# Docker

## Build

```bash
docker build -t appartment-webscraper .
```

## Run

```bash
docker run -v ~/appartment-webscraper:/root -e DATA_DIR=/root -it appartment-webscraper
```
