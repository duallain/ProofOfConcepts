#!/usr/bin/env bash

helm repo add stable https://kubernetes-charts.storage.googleapis.com
helm repo update 

helm install stable/external-dns --generate-name 
