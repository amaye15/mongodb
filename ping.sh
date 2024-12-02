for port in {1..65535}; do
    curl -s --connect-timeout 1 telnet://amaye15-mongodb.hf.space:$port > /dev/null && echo "Port $port is open"
done
