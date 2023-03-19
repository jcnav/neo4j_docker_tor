# Neo4j Docker Tor

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

## Fix Problem "error during connect: this error may indicate that the docker daemon is not running:"

In Windows depending on the user could be necessary:
* Start manually docker-desktop (sometimes you must start with the Administrator profile)
* If the problem persists open one PowerShell console and execute & 'C:\Program Files\Docker\Docker\DockerCli.exe' -SwitchDaemon

