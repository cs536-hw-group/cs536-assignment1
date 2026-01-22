#!/bin/bash

input_file=$1
output_file=$2

iterations=1

## testing
test_ip='160.242.19.254' 
test_host='chch.linetest.nz'
test_continent="Oceania"
test_country="PG"
test_site="Port Moresby"


### Functions

# greps min, avg, max rtt from an ip on $iteration iterations
# called with one arg: ip 
print_ping_data() {
    ip=$1

    vals=$(ping -c $iterations $ip | grep -Po '(\d+\.\d+)\/')

    min=$(echo $vals | awk '{print $1}')
    min=${min::-1}
    echo -e "\t\t\"MIN\": $min," >> $output_file
    avg=$(echo $vals | awk '{print $2}')
    avg=${avg::-1}
    echo -e "\t\t\"AVG\": $avg," >> $output_file
    max=$(echo $vals | awk '{print $3}')
    max=${max::-1}
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

while read line; do
    # TODO
    # -check if line contains IP/HOST, CONTINENT, COUNTRY, SITE and update var
    # run print_ip_data if line contains '}'
    # print count to show program running during iteration
done < $input_file

print_ip_data $test_host $test_continent $test_country $test_site

sed -i '$d' $output_file # used to delete the comma on last object, to preseve the json format
echo -e "\t}" >> $output_file
echo ']' >> $output_file
