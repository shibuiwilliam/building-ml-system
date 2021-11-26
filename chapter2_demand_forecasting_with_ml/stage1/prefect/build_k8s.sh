#!/bin/sh

set -eu

MANIFEST="./manifests"

kubectl apply -f ${MANIFEST}/namespace.yaml
kubectl apply -f ${MANIFEST}/postgresql.yaml
kubectl apply -f ${MANIFEST}/hasura.yaml
kubectl apply -f ${MANIFEST}/graphql.yaml
kubectl apply -f ${MANIFEST}/towel.yaml
kubectl apply -f ${MANIFEST}/apollo.yaml
kubectl apply -f ${MANIFEST}/ui.yaml
