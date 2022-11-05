ARG FROM_IMAGE=elasticsearch:8.1.3

FROM ${FROM_IMAGE}

RUN elasticsearch-plugin install analysis-kuromoji
RUN elasticsearch-plugin install analysis-icu

