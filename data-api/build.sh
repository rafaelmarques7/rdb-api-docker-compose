#/bin/bash

sudo docker-compose rm -f
sudo docker-compose pull
sudo docker-compose build --no-cache
sudo docker-compose up 