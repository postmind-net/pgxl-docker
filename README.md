# pgxl-docker

PostgreSQL-XL is a new MPP fork of PostgreSQL.

This version is a test of integration of PostgreSQL-XL with Docker, the default configuration file runs 4 data nodes, 1 gtm and 1 coordinator.
The docker configuration is not fully functional and is unsecure (run with docker privilegied mode, no password for postgresql coordinator).

### Build

`fig build`

### Run

`fig up`

### Authors

Matthieu Lagacherie and Yannick Drant, postmind project.
