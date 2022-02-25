ARG FROM_IMAGE=python:3.9.7-slim

FROM ${FROM_IMAGE}

ARG LOCAL_DIR=base_text_processing

ENV PROJECT_DIR opt
WORKDIR /${PROJECT_DIR}
COPY ${LOCAL_DIR}/requirements.txt /${PROJECT_DIR}/
RUN apt-get -y update && \
    apt-get -y install \
    apt-utils \
    gcc \
    git \
    curl \
    file \
    sudo \
    build-essential \
    swig \
    mecab \
    libmecab-dev \
    mecab-ipadic-utf8 && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/* && \
    git clone https://github.com/neologd/mecab-ipadic-neologd.git && \
    cd mecab-ipadic-neologd && \
    bin/install-mecab-ipadic-neologd -n -y && \
    cd /${PROJECT_DIR} && \
    mv /usr/lib/x86_64-linux-gnu/mecab/dic/mecab-ipadic-neologd /var/lib/mecab/dic && \
    sed -i 's/debian/mecab-ipadic-neologd/' /etc/mecabrc && \
    cp /etc/mecabrc /usr/local/etc/ && \
    pip install --no-cache-dir -r requirements.txt
