#!/usr/bin/env bash

echo "@@@ $(date): Bootstrap started..."

echo "@@@ $(date): Update Software Database"
sudo apt-get update -qq

echo "@@@ $(date): Install docker"
sudo apt-get install -qq docker docker-compose

echo "@@@ $(date): Update SSH Service..."
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo service ssh restart

echo "@@@ $(date): Install Complete"
echo "@@@ $(date): Your IP Address is $(hostname  -I | cut -f2 -d' ')"
