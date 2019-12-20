FROM apache/nifi:1.10.0

USER root

RUN apt-get install -y python3 python3-pip

RUN pip3 install tableschema requests numpy pandas messytables

ADD ./logback.xml /opt/nifi/nifi-1.10.0/conf

USER nifi

COPY scripts /scripts
RUN ls -l /
