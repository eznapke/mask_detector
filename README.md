# Security Surveillance
The information below is purely for confirming the mechanics of deploying the Security App.<br>

## Day 0/1 - EKS + App + Cfg

- Deploy EKS.<br>
- Connect to Bastion via SSH (key based authentication).<br>
- Install Security App via Helm.<br>
- The public IP (to expose the service) should be passed to the Helm Chart <br>
- Security App container is pulled down from DockerHub.<br>

>>git clone https://gitlab.mana.ericssondevops.com/EPABME/mask_detector.git<br>
>>cd /mask_detector/helm<br>
>>kubectl create namespace md-service<br>
>>helm install --set service.externalIP=(external ip) --name=md-service --namespace=md-service ./md_chart<br>

## Day N - Re-direct App to use new camera

- Connect to Bastion via SSH (key based authentication).<br>
- Update chart version e.g. 0.1.23<br>
- Update chart with new camera IP e.g 192.168.86.100<br>
- Upgrade the chart to push out the updated configmap<br>
- Restart the service to inject the configmap<br>
>>sed -i "/version:/c\version: 0.1.23" md_chart/Chart.yaml<br>
>>sed -i "/camera_ip:/c\  camera_ip: \"192.168.86.100\"" md_chart/values.yaml<br>
>>helm upgrade md-service ./md_chart/<br>
>>kubectl rollout restart deploy/md-service -n md-service<br>
>>helm list<br>

Note: In the future the App will suppoort this via a RESTful interface.


## Tip n Tricks
>>helm install --set service.externalIP=$(hostname -I | cut -f1 -d' ') --debug --dry-run md_chart/<br>
>>helm install --set service.externalIP=$(hostname -I | cut -f1 -d' ') --name=md-service --namespace=md-service ./md_chart<br>

>>helm history md-service<br>
>>helm delete --purge md-service<br>

## Lens Integration
>>kubectl config view --minify --raw<br>
