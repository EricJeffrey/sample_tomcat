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
            cpu_usage.append(
                int(data_line["cpu"]["usage"]["total"]) / 1000000)
            mem_usage.append(data_line["memory"]["usage"]["usage"] / mb)
            data_line_memraw = data_line["memory"]["raw"]
            act_anon.append(int(data_line_memraw["active_anon"]) / mb)
            pgfault.append(int(data_line_memraw["pgfault"]))
            pgpgin.append(int(data_line_memraw["pgpgin"]))
            pgpgout.append(int(data_line_memraw["pgpgout"]))
            rss.append(int(data_line_memraw["rss"]) / mb)
            pids_current.append(int(data_line["pids"]["current"]))
            x_axis.append(i)
            i += 1


def subplt(rows, index, title, x, y, cls=1):
    plt.subplot(rows, cls, index)
    plt.plot(x, y)
    plt.title(title)


def show():
    plt.figure(figsize=(30, 80))
    rows, cols = 4, 1

    plt.subplot(rows, cols, 1)
    plt.plot(x_axis, cpu_usage)
    plt.title('cpu usage(ms)')

    plt.subplot(rows, cols, 2)
    plt.plot(x_axis, mem_usage)
    plt.title('memory usage(mb)')

    # plt.subplot(rows, cols, 3)
    # plt.plot(x_axis, act_anon)
    # plt.title('memory raw active anon(mb)')

    plt.subplot(rows, cols, 3)
    plt.plot(x_axis, pgfault)
    plt.title('memory raw page fault')

    # plt.subplot(rows, cols, 5)
    # plt.plot(x_axis, pgpgin)
    # plt.title('memory raw pgpgin')

    # plt.subplot(rows, cols, 6)
    # plt.plot(x_axis, pgpgout)
    # plt.title('memory raw pgpgout')

    # plt.subplot(rows, cols, 7)
    # plt.plot(x_axis, rss)
    # plt.title('memory raw rss(mb)')

    plt.subplot(rows, cols, 4)
    plt.plot(x_axis, pids_current)
    plt.title('pids current')
    # plt.show()
    plt.savefig("./events_runc_tomcat.png")


read_data()
show()
