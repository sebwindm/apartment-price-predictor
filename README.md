# Docker

## Build

```bash
docker build -t appartment-webscraper .
```

## Run

```bash
docker run -v ~/appartment-webscraper:/root -e DATA_DIR=/root -it appartment-webscraper
```