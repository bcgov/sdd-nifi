FROM apache/nifi:1.11.2

USER root
RUN curl -sL https://deb.nodesource.com/setup_10.x | bash -
RUN apt-get update && apt-get install -y python3 python3-pip p7zip-full nodejs npm

RUN pip3 install tableschema requests numpy pandas messytables datapackage

RUN npm install semantic_infer

ADD ./logback.xml /opt/nifi/nifi-1.11.2/conf

USER nifi

COPY scripts /scripts

