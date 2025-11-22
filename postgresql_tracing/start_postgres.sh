#!/bin/bash

# Starts a dev build of postgresql in the container
/usr/local/pgsql/bin/pg_ctl -D /usr/local/pgsql/data -l logfile start
/usr/local/pgsql/bin/createdb test

# Running a wait here because pg_ctl will exit and run the server in the background. Sleep
# is just used to keep the container alive.
sleep infinity