#!/bin/bash

read -p "Enter the key: " key
read -p "Enter the value: " value

base_url="http://localhost:31380/api"

curl -X POST "${base_url}/cache?key=${key}&value=${value}"
echo
curl "${base_url}/cache?key=${key}"
echo


