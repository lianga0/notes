#! /usr/bin/bash

cd /opt/spark-3.3.2-bin-without-hadoop

sbin/start-history-server.sh

while true;
do
    count=`ps aux | grep -v 'grep' | grep -c 'org.apache.spark.deploy.history.HistoryServer'`
    if [ $count -eq 0 ]; then
            exit 1
    else
            now=`date +%F\ %T`
            echo "[$now] spark history server is online..."
    fi
    sleep 10
done