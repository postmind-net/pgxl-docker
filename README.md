# pgxl-docker

[PostgreSQL-XL](http://www.postgres-xl.org/) is a new MPP fork of [PostgreSQL](www.postgresql.org).

This version is a test of PostgreSQL-XL with Docker, the default configuration file runs 4 data nodes, 1 gtm and 1 coordinator.
The docker configuration is not fully functional and is unsecure (run with docker privilegied mode, no password for postgresql coordinator).

### Build

`fig build`

### Run

`fig up`

### Authors

Matthieu Lagacherie and Yannick Drant, postmind project.
