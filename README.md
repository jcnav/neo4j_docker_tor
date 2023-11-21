# Neo4j Docker Tor

This project provides an example of CTI architecture made of:
* **CSV example files:** Contains nodes, properties and relationships generated from Tor network data
* **docker-compose definitions**: docker-compose.yml handle teh following services
  * Neo4j database (container)
  * NeoDash dashboard (container)
  * neo4j_provision_xxx: Data provision for Neo4j loading csv files
  * delete_db: Delete database

## Start the environment

* Start the environment. 
  docker-compose up

* Enter in the dashboard
  http://localhost:5005/

  Define this new query for "amazing" results  
  MATCH (n)-[e]->(m) RETURN n,e,m LIMIT 1000



* Enter in Neo4J
  http://localhost:7474

* Delete DB
  docker-compose up --build delete_db

* Provision of the i2p nodes
  docker-compose up --build neo4j_provision_i2p

* Provision of the Tor nodes
  docker-compose up --build neo4j_provision_tor

## Temporary Content (Master Work Defense)
Additional content for educational purposes

Main docker-compose divided in: 
* dc_operations.yml: Operations
* dc_production.yml: "Containers"

## Fix Problem "error during connect: this error may indicate that the docker daemon is not running:"

In Windows depending on the user could be necessary:
* Start manually docker-desktop (sometimes you must start with the Administrator profile)
* If the problem persists open one PowerShell console and execute & 'C:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon

## Useful commands for Neo4J
* Delete DB

```
MATCH (n) DETACH DELETE n
```
Other option is delete the subdirectory neo4j_db/data. With this option the graph definitions will be already removed

* Show results 

```
MATCH (n)-[e]->(m) RETURN n,e,m LIMIT 1000
```

