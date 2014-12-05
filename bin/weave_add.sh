#!/bin/sh

C=$(sudo weave run 10.0.1.$1/24 -v `pwd`/pom:/pom -t -i pgxldocker_pgxl)

