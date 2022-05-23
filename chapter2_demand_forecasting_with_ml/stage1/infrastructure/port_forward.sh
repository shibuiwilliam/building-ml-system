#!/bin/sh

kubectl -n mlflow port-forward service/mlflow 5000:5000 &
kubectl -n argo port-forward service/argo-server 2746:2746 &
