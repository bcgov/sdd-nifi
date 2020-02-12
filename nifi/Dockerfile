FROM apache/nifi:1.10.0

USER root

RUN apt-get update && apt-get install -y python3 python3-pip p7zip-full

RUN pip3 install tableschema requests numpy pandas messytables datapackage

ADD ./logback.xml /opt/nifi/nifi-1.10.0/conf

USER nifi

COPY scripts /scripts

