#!/bin/sh

kubectl -n mlflow port-forward service/mlflow 5000:5000 &
kubectl -n aianimals port-forward service/api 8000:8000 &
kubectl -n argo port-forward service/argo-server 2746:2746 &
kubectl -n elastic-search port-forward service/elastic-search-es-http 9200:9200 &
kubectl -n elastic-search port-forward service/kibana-kb-http 5601:5601 &
