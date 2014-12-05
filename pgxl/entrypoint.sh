#!/bin/bash

if [ $# == 0 ]; then
	help_text;
elif [ $1 == "supervisor" ]; then
	sudo sysctl -p
	sudo /usr/bin/supervisord;
elif [ $1 == "key" ]; then
	sudo chown -R pom:pom /pom
	mkdir /pom/.ssh
	ssh-keygen -t rsa -C "pom@pgxl" -f /pom/.ssh/id_rsa -q -N ""
	cp /pom/.ssh/id_rsa.pub /pom/.ssh/authorized_keys
	chmod 700 /pom/.ssh && chmod 600 /pom/.ssh/*
elif [ $1 == "shell" ]; then
	/bin/bash;
elif [ $1 == "ip" ]; then
    echo "$PGXL_1_PORT_5432_TCP_ADDR";
fi;


