#!/bin/sh

set -eu

prefect server create-tenant --name k8s
prefect create project k8s
