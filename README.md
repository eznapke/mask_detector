# Security Surveillence

## Day 0/1 - EKS + App + Cfg

- Deploy EKS.<br>
- Connect to Bastion via SSH (key based authentication).<br>
- Helm used to install the Security App.<br>
- The public IP (to expose the service) should be passed to the Helm Chart <br>
- Security App container pulled down from dockerhub.<br>

>>tar -xvf md_chart.tar<br>
>>microk8s.kubectl create namespace md-service<br>
>>microk8s.helm install --set service.externalIP=<external ip> --name=md-service --namespace=md-service ./md_chart<br>

## Day N - Update App with new camera
- Connect to Bastion via SSH (key based authentication).<br>
- Update the chart version<br>
>sed -i "/version:/c\version: 0.1.23" md_chart/Chart.yaml<br>

- Update chart with new camera IP and Port<br>
>sed -i "/camera_ip:/c\  camera_ip: \"192.168.86.100\"" md_chart/values.yaml<br>

- Update the configmap for the service<br>
>microk8s.helm upgrade md-service ./md_chart/<br>
>microk8s.helm list<br>

- Push the Update the configmap for t<br>
>microk8s.kubectl rollout restart deploy/md-service -n md-service<br>

## Lens Integration
>microk8s.kubectl config view --minify --raw<br>
