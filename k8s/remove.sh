#!/usr/bin/env bash

microk8s.kubectl delete services md-service -n md-service
microk8s.kubectl delete deployment md-service -n md-service
microk8s.kubectl delete configmap md-service-config -n md-service
microk8s.kubectl delete namespace md-service

