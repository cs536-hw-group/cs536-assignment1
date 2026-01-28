#!/bin/bash

# run as ./run_files.sh [input_file.json]
set -euo pipefail

echo "This is the main script calling the other scripts"

input_file=$1

if [[ ! -f "$input_file" ]]; then
  echo "Input file does not exist: $input_file"
  exit 1
fi

#this calls the collect_data shell script that pings all of the IPs
echo "ping_output: "
./collect_data.sh "$input_file" ping_output.json

#this calls the shell script that calculates all of the distances for the IPs
echo "iperf_with_geo output: "
python3 geoLocator.py ping_output.json iperf_with_geo.json

#this calls the python program that plots the Distance v RTT scatter plot
python3 jsonToPlot.py ping_output.json iperf_with_geo.json

#this calls the python script that runs traceroute for part 2 and graphs for 2b and 2c
python3 latency_breakdown.py -i "$input_file"
