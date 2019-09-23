#!/usr/bin/env bash

#https://kifarunix.com/install-and-configure-filebeat-7-on-ubuntu-18-04-debian-9-8/

wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | sudo apt-key add -
echo "deb https://artifacts.elastic.co/packages/7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list
apt-get install apt-transport-https
apt update
apt install filebeat
systemctl restart filebeat