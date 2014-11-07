#!/bin/bash
set -e

export PATH=$PATH:/opt/pgxl/bin

sudo sysctl -p
if [ -z "$(ls -A "$PGDATA")" ]; then
	sudo chown -R pom:pom /pom
	pgxc_ctl init all	
fi

pgxc_ctl start all
tail -f /pom/pgxc/nodes/coord/pg_log/coordinator.log
pgxc_ctl stop all
