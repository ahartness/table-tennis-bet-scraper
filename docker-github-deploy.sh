#!/bin/bash

docker build -f dockerfile.gitjob -t github-python-worker .

docker container kill github-python-worker
docker container rm github-python-worker

docker run -d --name=github-python-worker github-python-worker

docker exec -it github-python-worker sh -c "git config --global user.email 'hartness.andrew@gmail.com'"
docker exec -it github-python-worker sh -c "git config --global user.name 'Andrew Hartness'"
