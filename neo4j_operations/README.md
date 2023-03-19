# Neo4J Operations

For debugger the docker files partially (without use docker-compose up):
*   docker build -t neo4j_provision .
*   docker run -it -d neo4j_provision

## References:
### Initial Datasets extracted from:
NOTE: Extracted from https://gitlab.com/ciberseg-uah/public/interconection-between-darknets-dataset

Interconnection between darknets (dataset)

Dataset used for the research about the interconnection between darknets made by the UAH.

### Citation

```
@ARTICLE{9291465,
  author={Cilleruelo, Carlos and de-Marcos, Luis and Junquera-Sánchez, Javier and Martínez-Herráiz, Jose-Javier},
  journal={IEEE Internet Computing}, 
  title={Interconnection Between Darknets}, 
  year={2021},
  volume={25},
  number={3},
  pages={61-70},
  doi={10.1109/MIC.2020.3037723}}
```

### Delete DB
Cypher commands

```
MATCH (n)
DETACH DELETE n
```
