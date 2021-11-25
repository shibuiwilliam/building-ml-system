#!/bin/sh

set -eu

kubectl -n prefect port-forward service/apollo 4200:4200 &
kubectl -n prefect port-forward service/ui 8080:8080 &
