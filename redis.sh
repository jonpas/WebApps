#!/bin/bash

if [ "$1" = "run" ]; then
    docker run --name webapps-redis -p 6379:6379 -d redis:5.0
elif [ "$1" = "stop" ]; then
    docker stop webapps-redis && docker rm webapps-redis
else
    echo "Expected argument: [run | stop]"
fi
