### Computation nodes


**Installation**  

Only one container may be installed in each provided node.  
Each node is required to have a distinct IP address that must be accessible from the main server. Each installation will
automatically notify the main server of the existance of a new node.

All the following installation options are equally valid:



* *Docker-compose*

Log into the server.  
Requirements: docker, docker-compose

An unique identification ID must be assigned to each node by the user. If there is already a computing node with this same ID, the container will
automatically shut off.

```bash
# Installation
cd ./computation-nodes

# URL_BASE: URL of the main server, not the computing node
URL_BASE=example.com INFLUXDB_WRITE_USER=writer INFLUXDB_WRITE_USER_PASSWORD=writer \
		 MONGO_INITDB_ROOT_USERNAME=root MONGO_INITDB_ROOT_USERNAME=root \
		 UNIQUE_ID=node1 docker-compose up -d 
```








**Usage**  
Each working node is provided with a routing API that will automatically process incoming jobs depending on their nature. A single node can execute
multiple jobs at the same time.
