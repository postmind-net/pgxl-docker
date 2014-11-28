# pgxl-docker

[Postgre-XL](http://www.postgres-xl.org/) is a new MPP fork of [PostgreSQL](http://www.postgresql.org).

This version is a test of Postgre-XL with Docker, the default configuration file runs several data nodes, 1 gtm and 1 coordinator.
The docker configuration is not fully functional and is unsecure (run with docker privilegied mode, no password for postgresql coordinator).

We have written a [tutorial](http://www.postmind.net/pgxl_docker-en.html) explaining the use of this docker configuration.

### Authors

Matthieu Lagacherie and Yannick Drant
