# Security Surveillence
The information below is purely for confirming the mechanics of deploying ths app

## Day 0/1 - EKS + App + Cfg

- Deploy EKS.<br>
- Connect to Bastion via SSH (key based authentication).<br>
- Install Security App via Helm.<br>
- The public IP (to expose the service) should be passed to the Helm Chart <br>
- Security App container pulled down from dockerhub.<br>

>>tar -xvf md_chart.tar<br>
>>microk8s.kubectl create namespace md-service<br>
>>microk8s.helm install --set service.externalIP=(external ip) --name=md-service --namespace=md-service ./md_chart<br>

## Day N - Update App with new camera

- Connect to Bastion via SSH (key based authentication).<br>
- Update chart version e.g. 0.1.23<br>
- Update chart with new camera IP e.g 192.168.86.100<br>
- Upgrade the chart to push out the updated configmap<br>
- Restart the service to inject the configmap<br>
>>sed -i "/version:/c\version: 0.1.23" md_chart/Chart.yaml<br>
>>sed -i "/camera_ip:/c\  camera_ip: \"192.168.86.100\"" md_chart/values.yaml<br>
>>microk8s.helm upgrade md-service ./md_chart/<br>
>>microk8s.helm list<br>
>>microk8s.kubectl rollout restart deploy/md-service -n md-service<br>

Note: In the future the App could support this via a RESTful interface.

## Lens Integration
>>microk8s.kubectl config view --minify --raw<br>
