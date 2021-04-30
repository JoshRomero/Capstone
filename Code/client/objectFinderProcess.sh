#!/bin/bash

checkConnection(){
    result=$(ls /etc/NetworkManager/system-connections | wc -l)
    if [ $result -eq 0 ]; then
        return 0
    else
        return 1
    fi
}

checkCredentials(){
    result=$(cat /.creds/currUser.json)
    if [ -z "$result" ]; then
        return 0
    else
        return 1
    fi
}

# MAIN

# set virtual environment
source /home/pi/tflite1/tflite-env/bin/activate

# set environment variables
export CURRENT_STATUS='INACTIVE'

# start access point
echo 'CHECKING CONNECTION...'
checkConnection
if [ $? -eq 0 ]; then
    export FIRST_BOOT=1
    while [ $FIRST_BOOT -eq 1 ]
    do
        sudo wifi-connection
        checkConnection
        if [ $? -eq 1]; then
            export FIRST_BOOT=0
        fi
    done
fi
echo 'CONNECTED!'

checkCredentials
if [ $? -eq 0 ]; then
    python3 piClient-firstBoot.py
fi

python3 piClient-webserver.py