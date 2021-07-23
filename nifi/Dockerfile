FROM apache/nifi:1.12.1

USER root
RUN curl -sL https://deb.nodesource.com/setup_14.x | bash -
RUN apt-get update && apt-get install -y python3 python3-pip p7zip-full nodejs clamav

RUN pip3 install tableschema datapackage

ADD ./logback.xml /opt/nifi/nifi-1.12.1/conf

RUN npm install --prefix /scripts semantic_infer


COPY scripts /scripts

RUN chown -R nifi /scripts

RUN chmod -R 750 /scripts/*

RUN freshclam

USER nifi