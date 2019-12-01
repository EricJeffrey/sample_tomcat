sudo iptables -t nat -D PREROUTING -t nat -i ens33 -p tcp --dport 4399 -j DNAT --to 10.1.1.2:8080
sudo iptables -t filter -D FORWARD -p tcp -d 10.1.1.1 --dport 8080 -j ACCEPT
sudo iptables -t nat -D POSTROUTING -s 10.1.1.0/24 ! -d10.1.1.0/24 -j MASQUERADE