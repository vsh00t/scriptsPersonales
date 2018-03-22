#!/bin/bash

for i in 2 3 4 5
do
    fecha=`date +%Y.%m.%d --date='-'$i' day'`
    curl -XDELETE localhost:9200/netflow-$fecha
    echo "borrando indices antiguos netflow-$fecha" >> /var/log/borrado.log
done

