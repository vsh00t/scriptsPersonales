#!/bin/bash

for i in 2 3 4 5
do
    fecha=`date +%Y.%m.%d --date='-'$i' day'`
    curl -XDELETE localhost:9200/netflow-$fecha
    echo "borrando indices antiguos netflow-$fecha" >> /var/log/borrado.log
done
proceso=`ps -u | grep 9996 | grep -v grep| awk '{print $2}'`
kill -9 $proceso
systemctl restart elasticsearch
systemctl restart logstash
nohup /usr/share/logstash/bin/logstash --modules netflow -M netflow.var.input.udp.port=9996 > /var/log/netflow.log &
