#!/bin/bash

git pull

docker build -t table-tennis-scraper .

docker container kill python-worker
docker container rm python-worker

docker run -d --name=python-worker table-tennis-scraper
