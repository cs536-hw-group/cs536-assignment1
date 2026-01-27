import json
import sys
import matplotlib.pyplot as plt

def main():
    #This takes in the two json files as command line arguments
    if len(sys.argv) < 3:
        print(f"usage: {sys.argv[0]} MESSAGE", file=sys.stderr)
        sys.exit(-1)
    ping_json = sys.argv[1]
    distance_json = sys.argv[2]

    #This loads the bash-created json file for the different pings
    pings = json.load(open(ping_json, 'r'))

    #This will load the distances from the distance json
    distances = json.load(open(distance_json, 'r'))

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

        #filters out non-responsive IP addresses
        if ping["AVG"] == -1:
            continue

        distance = float(d["DISTANCE (MI)"])
        avg_ping = ping["AVG"]

        x.append(distance)
        y.append(avg_ping)

    #creates the scatter plot
    plt.scatter(x,y)
    plt.xlabel("Distance")
    plt.ylabel("RTT")
    plt.title("Distance v. RTT Scatter Plot")

    plt.savefig('Distance_RTT_Scatter.pdf')
    plt.show()

if __name__ == '__main__':
    main()