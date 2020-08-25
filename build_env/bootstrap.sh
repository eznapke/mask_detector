#!/usr/bin/env bash

echo "@@@ $(date): Bootstrap started..."

echo "@@@ $(date): Update Software Database"
sudo apt-get update -qq

echo "@@@ $(date): Install docker"
sudo apt-get install -qq docker docker-compose

echo "@@@ $(date): Install Firefox"
sudo apt-get install -qq firefox

echo "@@@ $(date): Update SSH Service..."
sudo sed -i 's/PasswordAuthentication no/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo service ssh restart

echo "@@@ $(date): GIT...clone the pm_k8s_service"
git clone https://gitlab.mana.ericssondevops.com/EPABME/pm_k8s_service
sudo chmod 777 -R /home/vagrant/pm_k8s_service/

echo "@@@ $(date): Bootstrap complete..."
