#!/bin/sh
FILE=Dockerfile
if [ ! -f "$FILE" ]
then
    echo "$FILE does not exist"
    echo "Exit script"
    exit 1
fi
BUILD_DATE=`date -u +'%Y-%m-%dT%H:%M:%SZ'`
VER=`date -u +'%Y%m%d'`
if [ -d .git ]
then
    COMMIT_ID=$(git rev-parse --verify HEAD)
    COMMIT_ID=${COMMIT_ID:0:8}
    VER="${VER}_${COMMIT_ID}"
fi
TAG=${PWD##*/}
sudo docker build --build-arg TITLE=$TAG -t $TAG:$VER .
EXIST=`sudo docker inspect --format "{{ index .Config.Labels \"org.opencontainers.image.title\"}}" $TAG`
if [ "$TAG" == "$EXIST" ]
then
    echo "Container with the same name is found. Remove container."
    sudo docker stop $TAG > /dev/null
    sudo docker rm $TAG
fi
if [ $# -eq 0 ]
then
    PORT=80
    echo "Port argument not provided. Port set to 80 by default"
else
    PORT=$1
fi
sudo docker run -d --name $TAG -p $PORT:80 --restart unless-stopped -e $TAG:$VER
