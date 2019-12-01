sudo ip link add veth211 type veth peer name veth985
sudo ifconfig veth211 10.1.1.1/24 up
sudo ip link set veth985 netns 3304
sudo iptables -t nat -A POSTROUTING -s 10.1.1.0/24 ! -d 10.1.1.0/24 -j MASQUERADE
sudo iptables -A PREROUTING -t nat -i ens33 -p tcp --dport 4399 -j DNAT --to 10.1.1.2:8080
sudo iptables -A FORWARD -p tcp -d 10.1.1.1 --dport 8080 -j ACCEPT
