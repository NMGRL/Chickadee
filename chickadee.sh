#!/usr/bin/env bash

subcommand=$1

if [[ ${subcommand} == 'dev' ]]; then
    docker-compose --file docker-compose-dev.yml up --build
else
    docker-compose --file docker-compose.yml up --build
fi