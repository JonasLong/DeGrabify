#!/bin/bash

cron="$1"
db="$2"
shift 2
server_args="$@"

cd crawler
./run.sh "$cron" "-d $db" &
cd ../server
python -u server.py "-d" $db $server_args &

wait -n
exit $?