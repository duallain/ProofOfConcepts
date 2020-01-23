#!/usr/bin/env bash

helm repo add appscode https://charts.appscode.com/stable/
helm repo update
helm search repo appscode/voyager --version v12.0.0-rc.1

export provider=aws
helm install voyager-operator appscode/voyager --version v12.0.0-rc.1 \
  --namespace kube-system \
  --set cloudProvider=$provider
