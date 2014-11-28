#!/bin/bash
set -e

export PATH=$PATH:/opt/pgxl/bin

sudo sysctl -p

ssh-keygen -f "/pom/.ssh/known_hosts" -R localhost

if [ -z "$(ls -A "$PGDATA")" ]; then
	sudo chown -R pom:pom /pom
	pgxc_ctl init all	
fi


function shutdown()
{
    echo "Shutting down PostgreSQL"
    pgxc_ctl stop all
}

# Allow any signal which would kill a process to stop PostgreSQL
trap shutdown HUP INT QUIT ABRT KILL ALRM TERM TSTP

pgxc_ctl start all
tail -f /pom/pgxc/nodes/coord/pg_log/coordinator.log
