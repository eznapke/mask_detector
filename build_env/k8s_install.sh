#!/usr/bin/env bash
echo "@@@ $(date): Install Kubernetes"
#sudo snap install microk8s --classic --channel=1.17/edge
#sudo snap install microk8s --classic --channel=1.15/stable
sudo snap install microk8s --classic
sleep 60
sudo microk8s.enable ingress dashboard helm
sleep 10
sudo microk8s.enable storage dns
sleep 10
sudo microk8s.helm init
sleep 10
sudo usermod -a -G microk8s $USER
sleep 5
echo "@@@ $(date): Updating the cronjob to run proxy at boot"
crontab -l > mycron
echo "@reboot /home/vagrant/mask_detector/build_env/at_boot.sh" >> mycron
crontab mycron
rm mycron
sleep 10
sudo microk8s.kubectl proxy &
sleep 10
echo "@@@ $(date): Install Complete"
echo "@@@ $(date): Your IP Address is $(hostname  -I | cut -f2 -d' ')"
