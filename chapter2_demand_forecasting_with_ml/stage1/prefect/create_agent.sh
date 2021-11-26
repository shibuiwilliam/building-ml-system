#!/bin/sh

set -eu

AGENT_MANIFEST=manifests/agent.yaml

prefect agent kubernetes install \
    --api http://apollo.prefect.svc.cluster.local:4200 \
    --rbac >${AGENT_MANIFEST}

kubectl apply -f ${AGENT_MANIFEST}
