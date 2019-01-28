#!/bin/bash

if [ $# -lt "2" ]; then
    printf "INVALID syntax\nMust provide organization and URL base (without http:// or https://\n\n"
    exit
fi

export org="$1"
export domain="$2"
export admin_password="$3"

if [ -z "$3" ]; then
    export admin_password="test"
    printf "Administrator password was not provided (3 arg), was set to 'test'\n"
fi


docker-compose up -d

