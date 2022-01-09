ARG FROM_IMAGE=docker.elastic.co/elasticsearch/elasticsearch:7.16.2

FROM ${FROM_IMAGE}

RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu
RUN elasticsearch-plugin install -b https://github.com/o19s/elasticsearch-learning-to-rank/releases/download/v1.5.8-es7.16.2/ltr-plugin-v1.5.8-es7.16.2.zip

