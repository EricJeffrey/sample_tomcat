sleep 3
ab -c 1000 -n 1000 http://10.1.1.2:8080/ > ab_out.txt
sleep 4
ab -c 800 -n 6000 http://10.1.1.2:8080/ > ab_out.txt
sleep 3