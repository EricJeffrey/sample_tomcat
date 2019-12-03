import json
import matplotlib.pyplot as plt

'''
data{
    cpu.usage.total
    memory.usage.usage
    memory.raw.active_anon
    memory.raw.pgfault
    memory.raw.pgpgin
    memory.raw.pgpgout
    memory.raw.rss
    pids.current
    --- below ignore ---
    memory.raw.total_active_anon
    memory.raw.total_pgfault
    memory.raw.total_pgpgin
    memory.raw.total_pgpgout
    memory.raw.total_rss
}
'''
# read fixed json data
# plot.x = 1,2,3,4...
# plot.y = data[value"]
# split to

interval = 0.05
x_axis = []
cpu_usage = []
mem_usage = []
act_anon = []
pgfault = []
pgpgin = []
pgpgout = []
rss = []
pids_current = []


def read_data():
    i = 1
    with open("./runc_events.txt", encoding="utf-8", mode="r") as fp:
        lines = fp.readlines()
        mb = 1024 * 1024
        for line in lines:
            if line == "":
                break
            data_line = json.loads(line)["data"]
            usage_percent_tmp = data_line["cpu"]["usage"]["total"] / \
                1000000000 / ((i + 30) * interval) * 100
            cpu_usage.append(usage_percent_tmp)
            mem_usage.append(data_line["memory"]["usage"]["usage"] / mb)
            data_line_memraw = data_line["memory"]["raw"]
            act_anon.append(int(data_line_memraw["active_anon"]) / mb)
            pgfault.append(int(data_line_memraw["pgfault"]))
            pgpgin.append(int(data_line_memraw["pgpgin"]))
            pgpgout.append(int(data_line_memraw["pgpgout"]))
            rss.append(int(data_line_memraw["rss"]) / mb)
            pids_current.append(int(data_line["pids"]["current"]))
            x_axis.append(i * interval)
            i += 1


def subplt(rows, index, title, x, y, cls=1):
    plt.subplot(rows, cls, index)
    plt.plot(x, y)
    plt.title(title)


def show():
    plt.figure(figsize=(10, 30))
    rows, cols = 4, 1

    subplt(rows, 1, 'cpu usage(%)', x_axis, cpu_usage)
    subplt(rows, 2, 'memory usage(mb)', x_axis, mem_usage)
    subplt(rows, 3, 'memory raw page fault', x_axis, pgfault)
    subplt(rows, 4, 'pids', x_axis, pids_current)

    # plt.show()
    plt.savefig("./events_runc_tomcat.png")


read_data()
show()
