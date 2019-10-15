#!/bin/bash
app="docker.test"
docker build -t ${app} .
docker-compose -f docker-compose.yml -f docker-compose-infra.yml up