# mask_detector

microk8s.kubectl config view --minify --raw

# To install Mask Detector
# Note : <external ip> should be configured with Public IP assigned to EKS
tar -xvf md_chart.tar
microk8s.kubectl create namespace md-service
microk8s.helm install --set service.externalIP=<external ip> --name=md-service --namespace=md-service ./md_chart

# To modify camera ip/port
sed -i "/version:/c\version: 0.1.23" md_chart/Chart.yaml
sed -i "/camera_ip:/c\  camera_ip: \"192.168.86.100\"" md_chart/values.yaml
microk8s.helm upgrade md-service ./md_chart/
microk8s.helm list
microk8s.kubectl rollout restart deploy/md-service -n md-service
