#!/bin/bash
ping -c 1 160.242.19.254 | grep -Po '(\d+\.\d+)\/'
