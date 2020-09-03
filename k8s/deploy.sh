#!/usr/bin/env bash

external_ip=$(hostname  -I | cut -f1 -d' ')

echo "@@@ $(date): Create the Namespace"
microk8s.kubectl create namespace md-service

echo "@@@ $(date): Create the Configmaps"
microk8s.kubectl create configmap md-service-config --from-env-file=cfg/k8s_md_service_config.properties -n md-service

echo "@@@ $(date): Deploy the Services"
microk8s.kubectl create -f cfg/k8s_md_service_deployment.yaml -n md-service

echo "@@@ $(date): Expose the Services"
microk8s.kubectl expose deployment md-service --type=LoadBalancer --name=md-service -n md-service
microk8s.kubectl patch service md-service  -p '{"spec": {"type": "LoadBalancer", "externalIPs":["'"$external_ip"'"]}}' -n md-service
