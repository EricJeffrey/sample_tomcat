# Tomcat容器

在alpine-linux容器中运行Tomcat服务器，使用`Apache Benchmark`测试性能并记录数据

## 过程记录

1. 下载alpine的minirootfs并解压
2. 下载Tomcat并解压
3. 编写hooks
   1. prestart - 需要从`stdin`读取pid，故采用C++编写
      ```c++
      string lines[] = {
          "sudo ip link add " + veth1 + " type veth peer name " + veth2,
          "sudo ifconfig " + veth1 + " 10.1.1.1/24 up",
          "sudo ip link set " + veth2 + " netns " + pid_netns,
          "sudo iptables -t nat -A POSTROUTING -s 10.1.1.0/24 ! -d 10.1.1.0/24 -j MASQUERADE",
          "sudo iptables -A PREROUTING -t nat -i ens33 -p tcp --dport 4399 -j DNAT --to 10.1.1.2:8080",
          "sudo iptables -A FORWARD -p tcp -d 10.1.1.1 --dport 8080 -j ACCEPT"
      };
      ```
   2. poststop
      ```sh
      # 删除路由表内的端口映射与网络转发
      sudo iptables -t nat -D PREROUTING -t nat -i ens33 -p tcp --dport 4399 -j DNAT --to 10.1.1.2:8080
      sudo iptables -t filter -D FORWARD -p tcp -d 10.1.1.1 --dport 8080 -j ACCEPT
      sudo iptables -t nat -D POSTROUTING -s 10.1.1.0/24 ! -d 10.1.1.0/24 -j MASQUERADE
      ```
4. 编写启动程序
   ```sh
   # setup network and start /bin/ash
   ifconfig veth985 up
   ifconfig veth985 10.1.1.2
   ifconfig veth985 netmask 255.255.255.0
   route add default gw 10.1.1.1
   echo 'nameserver 202.38.64.56' > /etc/resolv.conf
   echo -e 'http://mirrors.ustc.edu.cn/alpine/v3.10/main\nhttp://mirrors.ustc.edu.cn/alpine/v3.10/community' > /etc/apk/repositories
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
   ```
5. 创建配置文件config.json
   1. 配置待执行的hooks
   ```json
   "hooks": {
       "prestart": [
           {
               "path": "./prestart.out",
               "args": [
                   "prestart.out"
               ]
           }
       ],
       "poststop": [
           {
               "path": "/bin/bash",
               "args": [
                   "bash",
                   "./poststop.sh"
               ]
           }
       ]
   }          
   ```
   2. 配置容器内要启动的程序与环境变量
   ```json
   "args": [
       "/bin/ash",
       "init.sh"
   ],
   "env": [
       "PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/lib/jvm/java-11-openjdk/bin:/usr/lib/jvm/java-11-openjdk/jre/bin",
       "JAVA_HOME=/usr/lib/jvm/java-11-openjdk/",
       "JRE_HOME=/usr/lib/jvm/java-11-openjdk/jre/",
       "TERM=xterm"
   ],
   ```
   3. 其它配置信息 - 权限、文件非只读
6. 运行容器 - `./go.sh`
7. 新终端 - 执行`runc events`，查看进程的属性
   ```sh
   sudo runc events --interval 0.01s helo > perf_analysis/runc_events.txt
   ```
8. 新终端 - 使用ApacheBenchmark测试性能
   ```sh
   ab -c 1000 -n 6000 http://10.1.1.2:8080/ > perf_analysis/ab_out.txt
   ```
9.  分析events的输出 - `parse.py`
