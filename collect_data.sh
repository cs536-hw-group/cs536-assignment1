#!/bin/bash

# run as ./collect_data.sh [input_file.json] [output_file.json]

input_file=$1
output_file=$2

iterations=100
interval=0.01

## testing
#test_ip_host='ping6-90ms.online.net' 
#test_host='chch.linetest.nz'
#test_continent="Oceania"
#test_country="PG"
#test_site="Port Moresby"


### Functions

# greps min, avg, max rtt from an ip on $iteration iterations
# called with one arg: ip 
print_ping_data() {
    ip=$1

    vals=$(ping -c $iterations -i $interval $ip)

    if [[ $(echo $vals | grep -P '100% packet loss') ]]; then # packets never returned from ping command, set values to -1
        echo $vals
        min=-1
        avg=-1
        max=-1
    elif [[ -z $vals ]]; then # Network is unreachable, no stdout text
        echo $vals
        min=-1
        avg=-1
        max=-1
    else
        vals=$(echo $vals | grep -Po '(\d+\.\d+)\/')

        min=$(echo $vals | awk '{print $1}')
        min=${min::-1}
        avg=$(echo $vals | awk '{print $2}')
        avg=${avg::-1}
        max=$(echo $vals | awk '{print $3}')
        max=${max::-1}
    fi

    echo -e "\t\t\"MIN\": $min," >> $output_file
    echo -e "\t\t\"AVG\": $avg," >> $output_file
    echo -e "\t\t\"MAX\": $max" >> $output_file
}

# prints each part relevant for an ip in json
# does not account for the final object (comma after added for all objects)
# call with 4 args: ip, continent, country, site
print_ip_data() {
    ip=$1 
    continent=$2
    country=$3
    site=$4

    echo -e "\t{" >> $output_file
    echo -e "\t\t\"IP/HOST\": \"$ip\"," >> $output_file
    echo -e "\t\t\"CONTINENT\": \"$continent\"," >> $output_file
    echo -e "\t\t\"COUNTRY\": \"$country\"," >> $output_file
    echo -e "\t\t\"SITE\": \"$site\"," >> $output_file
    print_ping_data $ip
    echo -e "\t}," >> $output_file
}

# takes a line from the json and outputs the value
# currently doesn't pull accurately for the last line of an object due to missing comma (not necessary for this implementation)
# call with 1 arg: line (ex: '"CONTINENT": "Oceania",')
# 1 output, the value in the quotes
capture_value() {
    line=$1

    value=$(echo $line | grep -Po '\s\".*\",')    
    value=${value:2:-2}

    echo $value
}
#testing func
#value=$(capture_value "\"Continent\": \"Oceania\",")
#echo $value

### Iterate and execute on all ip/hosts in $input_file

echo '[' > $output_file

#print_ip_data $test_ip_host $test_continent $test_country $test_site
#exit 0

declare -i cnt=0
echo "Running ping test on ip/hosts"
while read line; do
    if [[ $(echo $line | grep -P 'IP\/HOST') ]]; then
        ip_host=$(capture_value "$line")
    elif [[ $(echo $line | grep -P 'CONTINENT') ]]; then
        continent=$(capture_value "$line")
    elif [[ $(echo $line | grep -P 'COUNTRY') ]]; then
        country=$(capture_value "$line")
    elif [[ $(echo $line | grep -P 'SITE') ]]; then
        site=$(capture_value "$line")
    fi

    # run print_ip_data if line contains '}' (arbitarily chosen line to print data on)
    if [[ $(echo $line | grep -P '}') ]]; then
        print_ip_data $ip_host $continent $country $site
        echo $cnt # show count for current ip being analyzed
        cnt+=1
    fi
done < $input_file

sed -i '$d' $output_file # used to delete the comma on last object, to preseve the json format
echo -e "\t}" >> $output_file
echo ']' >> $output_file

echo "Finished"
