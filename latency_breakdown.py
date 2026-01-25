import json
import subprocess
import random
import platform
import re
import matplotlib.pyplot as plt


# Function selects servers from server list file
def get_servers_by_index(filename="listed_iperf3_servers.json", indices=None):
    try:
        with open(filename, 'r') as f:
            data = json.load(f)
            
        # pick 5 random unique indices if no indices provided
        if indices is None:
            indices = random.sample(range(len(data)), min(5, len(data)))
            print(f"Selected random indices: {indices}")

        selected_ips = []
        for idx in indices:
            # get IP/HOST field for indices
            server_info = data[idx]
            ip = server_info.get("IP/HOST")
            if ip:
                selected_ips.append(ip)
        
        return selected_ips

    except FileNotFoundError:
        print(f"Error: {filename} not found.")
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


# Function runs traceroute and parses output
def run_traceroute(destination):
    system_os = platform.system().lower()
    if system_os != "windows":
        # -n disables DNS resolution (makes it faster)
        # -q 1 sends only one packet
        # -w makes it wait only 2 seconds for each step
        cmd = ["traceroute", "-n", "-q", "1", "-w", "2", destination]
    else:
        # -d disables DNS resulution on windows
        cmd = ["tracert", "-d", destination]
    
    print(f"running traceroute to {destination}")
    try:
        # run traceroute with timeout set to 30s to prevent hanging
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
        lines = result.stdout.splitlines()
    except Exception as e:
        print(f"Traceroute failed/timed out for {destination}: {e}")
        return []

    hop_data = []
    for line in lines:
        # regex to find hop number and RTT for output of form "3  10.0.0.1  15.5 ms")
        match = re.search(r'^\s*(\d+).+?(\d+\.?\d*)\s*ms', line)
        if match:
            hop_num = int(match.group(1))
            rtt = float(match.group(2))
            hop_data.append((hop_num, rtt))
    
    return hop_data


def main():
    # pick 5 random servers from list
    # can specify indices here, example: get_servers_by_index("listed_iperf3_servers", [0, 5, 10, 15, 20])
    selected_ips = get_servers_by_index("listed_iperf3_servers.json")
    
    if not selected_ips:
        return

    results = {}
    for ip in selected_ips:
        data = run_traceroute(ip)
        if data:
            results[ip] = data

    if not results:
        print("No traceroute data collected. Ensure traceroute is installed.")
        return

    print(results)

    # part b: stacked bar chart (server/ip vs. hop latencies)
    plt.figure(figsize=(12, 7))
    
    for ip, hops in results.items():
        incremental_latencies = []
        prev_rtt = 0
        for _, rtt in hops:
            # calculate the diference between this hop and last hop (hop dealta)
            diff = max(0, rtt - prev_rtt)
            incremental_latencies.append(diff)
            prev_rtt = rtt
        
        bottom = 0
        for i, val in enumerate(incremental_latencies):
            # stack the bars
            plt.bar(ip, val, bottom=bottom)
            bottom += val
    
    plt.title("Latency Breakdown per Hop (Stacked)")
    plt.ylabel("Cumulative RTT (ms)")
    plt.xlabel("Destination IP / Hostname")
    plt.xticks(rotation=15)
    plt.tight_layout()
    plt.savefig('2b_latencies_to_each_hop.pdf')
    plt.show()

    # part c: scatter plot (hop count vs. RTT)
    plt.figure(figsize=(10, 6))
    for ip, hops in results.items():
        max_hop = hops[-1][0]   # last hop number
        final_rtt = hops[-1][1] # last RTT
        plt.scatter(max_hop, final_rtt, s=50)
        plt.text(max_hop + 0.2, final_rtt, ip, fontsize=9, verticalalignment='center')

    plt.title("Total Hop Count vs. Final RTT")
    plt.xlabel("Total Number of Hops")
    plt.ylabel("Final Destination RTT (ms)")
    plt.grid(True, linestyle='--', alpha=0.6)
    plt.savefig('2c_hop_count_vs_rtt.pdf')
    plt.show()


if __name__ == "__main__":
    main()
