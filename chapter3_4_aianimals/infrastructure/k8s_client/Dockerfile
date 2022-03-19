ARG FROM_IMAGE=ubuntu:latest

FROM ${FROM_IMAGE}

RUN apt -y update && \
    apt -y install curl && \
    rm -rf /var/lib/apt/lists/* && \
    curl -LO "https://storage.googleapis.com/kubernetes-release/release/$(curl -s https://storage.googleapis.com/kubernetes-release/release/stable.txt)/bin/linux/amd64/kubectl" && \
    chmod +x ./kubectl && \
    mv ./kubectl /usr/local/bin/kubectl
