#!/bin/bash
server="172.19.96.1"
port="1433"

if nc -z "$server" "$port"; then
    echo "Server OK"
else
    echo "No connect"
fi