ARG FROM_IMAGE=docker.elastic.co/elasticsearch/elasticsearch:8.1.2

FROM ${FROM_IMAGE}

RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu

