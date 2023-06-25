FROM apache/nifi 

USER root 

RUN apt-get update && apt-get install python3 -y

USER nifi

WORKDIR /opt/nifi/nifi-current/

RUN mkdir drivers
COPY apache/mysql-connector-j-8.0.33.jar drivers

# Aumentando memória da JVM para lidar com arquivos maiores.
RUN sed -i 's/512m/2048m/g' conf/bootstrap.conf

RUN bin/nifi.sh set-single-user-credentials user apachenifi123

CMD bin/nifi.sh run

