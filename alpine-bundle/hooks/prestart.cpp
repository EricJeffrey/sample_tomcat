#include <cstdio>
#include <iostream>
#include <string>
#include <unistd.h>

using std::cin;
using std::endl;
using std::string;

FILE *fp_log;
const void fail(const string tmps = "") {
    if (fp_log != nullptr) {
        if (!tmps.empty()) fprintf(fp_log, "%s\n", tmps.c_str());
        fclose(fp_log);
    }
    exit(EXIT_FAILURE);
}

int main(int argc, char const *argv[]) {
    fp_log = fopen("./pre_start.log", "w");

    // write state
    string container_state;
    while (!cin.eof()) {
        string tmp;
        cin >> tmp;
        container_state += tmp;
    }
    fprintf(fp_log, "%s\n", container_state.c_str());
    fclose(fp_log);
    // read pid
    const int sz_container_state = container_state.size();
    if (sz_container_state <= 0) fail("container state size 0");
    int st = 0;
    while (st + 2 < sz_container_state && container_state.substr(st, 3) != "pid")
        st++;
    if (st >= sz_container_state) fail("cannot find 'pid' inside state");
    st = st + 5;
    int ed = st;
    while (ed < sz_container_state && container_state[ed] != ',')
        ed++;
    if (ed >= sz_container_state) fail("cannot find ',' after 'pid' inside state");

    string pid_netns;
    pid_netns = container_state.substr(st, ed - st);
    // generate shell
    string veth1 = "veth211";
    string veth2 = "veth985";
    string lines[] = {
        "sudo ip link add " + veth1 + " type veth peer name " + veth2,
        "sudo ifconfig " + veth1 + " 10.1.1.1/24 up",
        "sudo ip link set " + veth2 + " netns " + pid_netns,
        "sudo iptables -t nat -A POSTROUTING -s 10.1.1.0/24 ! -d 10.1.1.0/24 -j MASQUERADE",
        "sudo iptables -A PREROUTING -t nat -i ens33 -p tcp --dport 4399 -j DNAT --to 10.1.1.2:8080",
        "sudo iptables -A FORWARD -p tcp -d 10.1.1.1 --dport 8080 -j ACCEPT"};

    // write and execute
    string hook_path = "./prestart.sh";
    FILE *fp_sh = fopen(hook_path.c_str(), "w");
    for (auto &&line : lines) {
        fprintf(fp_sh, "%s\n", line.c_str());
    }
    fclose(fp_sh);

    execl("/bin/bash", "bash", hook_path.c_str(), nullptr);
    return 0;
}
