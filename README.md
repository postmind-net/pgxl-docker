# pgxl-docker

[Postgre-XL](http://www.postgres-xl.org/) is a new MPP fork of [PostgreSQL](http://www.postgresql.org).

This version is a test of Postgre-XL with Docker, the default configuration file runs 4 data nodes, 1 gtm and 1 coordinator.
The docker configuration is not fully functional and is unsecure (run with docker privilegied mode, no password for postgresql coordinator).

### Implementation

The latest GIT version of Postgres-XL is used. The daemons are started with [supervisord](http://supervisord.org/).

### Build

`fig build`

### Run

`fig up`

### Authors

Matthieu Lagacherie and Yannick Drant.
