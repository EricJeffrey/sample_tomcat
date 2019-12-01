# setup network and start /bin/ash
ifconfig veth985 up
ifconfig veth985 10.1.1.2
ifconfig veth985 netmask 255.255.255.0
route add default gw 10.1.1.1
echo 'nameserver 202.38.64.56' > /etc/resolv.conf
echo -e 'http://mirrors.ustc.edu.cn/alpine/v3.10/main\nhttp://mirrors.ustc.edu.cn/alpine/v3.10/community' > /etc/apk/repositories
# echo 'Installing Python3'
# apk add python3
# cd home/
# echo 'Starting Python3-Http.server'
# nohup python3 -m http.server 8000 > foo.txt &
echo 'installing openjdk...'
apk add openjdk11
echo 'jdk installed, starting tomcat-9.0.29'
./tomcat-9.0.29/bin/startup.sh
/bin/ash
echo 'stopping'
apk del openjdk11
echo 'jdk uninstalled'
route del default gw 10.1.1.1
ip link del veth985
echo 'bye'
