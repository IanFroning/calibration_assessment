#!/bin/sh
# redirect all output to log file
exec 1>> server.log
exec 2>&1

python src/server.py &
