# Page Replacement Policy Simulator

This repository implements a page replacement policy simulator to measure how certain page replacement policies do under certain synthetic and real world workloads. 


### src/
This contains the simulator itself. It is written in python with `src/main.py` running the simulations. Multiple page replacement policies have been implemented and multiple workloads can be pulled in. 


### postgresql_tracing/
This contains a Docker file that was used build a container to gather page accesses within the PostgreSQL instance running on it. The container builds PostgreSQL from source, builds systemtap from source, and starts PostgreSQL. You can than use your choice of benchmark to load the database while running systemtap interactively in the container. WARNING: The container does run in privileged mode. So maybe don't take this code and use it anywhere else. 

This directory also contains the page access patterns gathered from PostgreSQL in the `postgresql_tracing/data/` directory. The corresponding Benchbase configurations can be found in the `postgresql_tracing/` directory as well. 