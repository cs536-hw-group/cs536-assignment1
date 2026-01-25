import json
import matplotlib.pyplot as plt

#This loads the bash-created json file for the different pings
pings = json.load(open('ping_output.json', 'r'))

#This will load the distances from the distance json
distances = json.load(open('ips_with_distance.json', 'r'))

#shows a grid on the graph
plt.grid(True)

#filters by ip/host
ping_by_ip = {
    p["IP/HOST"]: p
    for p in pings

}

#joins the 2 jsons together to filter
x = []
y = []

for d in distances:
    ip = d["IP/HOST"]

    if ip not in ping_by_ip:
        continue

    ping = ping_by_ip[ip]

    if ping["AVG"] == -1:
        continue

    distance = float(d["DISTANCE (MI)"])
    avg_ping = ping["AVG"]

    x.append(distance)
    y.append(avg_ping)

#creates the scatter plot
# x = [d["DISTANCE (MI)"] for d in distances]
# print(len(x))
# y = [p["AVG"] for p in pings]
# print(len(y))
plt.scatter(x,y)
plt.xlabel("Distance")
plt.ylabel("RTT")
plt.title("Distance v. RTT Scatter Plot")

plt.savefig('Distance_RTT_Scatter.pdf')
plt.show()