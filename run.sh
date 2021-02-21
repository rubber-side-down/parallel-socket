#!/usr/bin/env bash

for i in "$@"
do
case $i in
    -s=*|--packet-size=*)
    packet_size="${i#*=}"
    shift 
    ;;
    -n=*|--num-packets=*)
    num_packets="${i#*=}"
    shift 
    ;;
    -t=*|--num-threads=*)
    num_threads="${i#*=}"
    shift 
    ;;
    -h=*|--host=*)
    host="${i#*=}"
    shift 
    ;;
    -p=*|--port=*)
    port="${i#*=}"
    shift 
    ;;
    *)
    ;;
esac
done

python3 server.py --host="${host}" \
                  --port="${port}" \
                  --packet-size="${packet_size}" &
server_pid=$!
python3 client.py --packet-size="${packet_size}" \
                  --num-packets="${num_packets}" \
                  --num-threads="${num_threads}" \
                  --host="${host}" \
                  --port="${port}"
kill "${server_pid}"