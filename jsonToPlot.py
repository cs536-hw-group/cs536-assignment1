import json
import matplotlib.pyplot as plt

#This loads the bash-created json file for the different pings
pings = json.load(open('ping_output.json', 'r'))

#This will load the distances from the distance json
distances = json.load(open('ping_output.json', 'r'))

#shows a grid on the graph
plt.grid(True)

#creates the scatter plot
plt.scatter(distances["Distance"], pings["AVG"])
plt.xlabel("Distance")
plt.ylabel("RTT")
plt.title("Distance v. RTT Scatter Plot")
plt.show()