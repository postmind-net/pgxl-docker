#!/bin/bash

if [ $# == 0 ]; then
	help_text;
elif [ $1 == "supervisor" ]; then
	sudo sysctl -p
	sudo /usr/bin/supervisord;
elif [ $1 == "shell" ]; then
	/bin/bash;
elif [ $1 == "ip" ]; then
    echo "$PGXL_1_PORT_5432_TCP_ADDR";
fi;


