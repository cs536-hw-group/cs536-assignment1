#! /bin/bash

# run as ./run_files.sh [input_file.json]

echo "This is the main script calling the other scripts"

input_file=$1

#this calls the collect_data shell script that pings all of the IPs
./collect_data.sh "$input_file" ping_output.json

#this calls the shell script that calculates all of the distances for the IPs
python geoLocator.py "$input_file"

#this calls the python program that plots the Distance v RTT scatter plot
python jsonToPlot.py ping_output.json iperf_with_geo.json

