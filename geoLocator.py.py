import json
import sys
import socket
import requests
import math
import time

def haversine(lat1, lon1, lat2, lon2):
    R = 3958.8  # Earth radius in miles

    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = math.sin(dlat/2)**2 + math.cos(lat1)*math.cos(lat2)*math.sin(dlon/2)**2
    c = 2 * math.asin(math.sqrt(a))

    return R * c

#input_file = "ipAddresses.csv"
#output_file = "iperf_with_geo.csv"
input_file = sys.argv[1]
output_file = "iperf_with_geo.json"
results = []
lawson_long = -86.916956
lawson_lat = 40.427611

# Read the CSV and resolve each domain
with open(input_file, newline="") as f:
    data = json.load(f)

#preload into results array
for entry in data:
    results.append({
        "IP/HOST": entry.get("IP/HOST", ""),
        "PORT": entry.get("PORT", ""),
        "OPTIONS": entry.get("OPTIONS", ""),
        "GB/S": entry.get("GB/S", ""),
        "CONTINENT": entry.get("CONTINENT", ""),
        "COUNTRY": entry.get("COUNTRY", ""),
        "SITE": entry.get("SITE", ""),
        "PROVIDER": entry.get("PROVIDER", ""),
        "LATITUDE": "",
        "LONGITUDE": "",
        "DISTANCE": ""
    })

    noLoc = len(results)
    rounds = 0

    while noLoc>0 and rounds < 5:
        for entry in results:
            if entry["LATITUDE"]!="" and entry["LONGITUDE"]!="":
                continue

            host = entry["IP/HOST"]

            #change any domains given to their ip address so all rows start with ip addresses
            if any(char.isalpha() for char in host):
                try:
                    ip = socket.gethostbyname(host)
                except Exception:
                    ip = "RESOLUTION_FAILED"
                    noLoc-=1
            else:
                ip = host
            
            
            if ( ip != "RESOLUTION_FAILED"):
                url = f"https://free.freeipapi.com/api/json/{ip}"

                response = requests.get(url).json()
                #print(data)

                latitude = response.get("latitude")
                longitude = response.get("longitude")
                print(longitude," ",latitude)

                if latitude is None or longitude is None:
                    time.sleep(60)
                    continue
                

                entry["LATITUDE"] = latitude
                entry["LONGITUDE"] = longitude
                entry["DISTNACE"] = haversine(lawson_lat, lawson_long, latitude, longitude)
                noLoc-=1
 
        rounds+=1
        
        

# Write the updated CSV
#print(rows)
with open(output_file, "w") as f:
    json.dump(results, f, indent=2)

print("Done. Output saved to:", output_file)
