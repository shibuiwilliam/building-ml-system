ARG FROM_IMAGE=docker.elastic.co/elasticsearch/elasticsearch:7.16.0

FROM ${FROM_IMAGE}

RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu
