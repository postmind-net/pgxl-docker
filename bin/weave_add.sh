#!/bin/sh

C=$(sudo weave run 10.0.1.$1/24 -t -i pgxldocker_pgxl -v pom:/pom)

