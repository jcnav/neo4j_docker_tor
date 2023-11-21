# Graph Catalog
(https://neo4j.com/docs/graph-data-science/current/management-ops/graph-catalog-ops/)

## Projections
Can be projected by:
* Native Projection
* Cypher P.
* Legacy Cypher P.
You can add additional graphs to the catalog

## Inspection
Operations:
* gds.graph.list   (list)
* gds.graph.exists (check if a named graph is stored)

## Modifying the catalog
Update operations:
* gds.alpha.graph.nodeLabel.mutate          (adds a new node label)
* gds.beta.graph.relationships.toUndirected (converts relationships from directed to undirected)

## Exporting from the graph catalog
Export operations:
* gds.graph.nodeProperty.stream            Streams a single node property stored in a named graph.
* gds.graph.nodeProperties.stream          Streams node properties stored in a named graph.
* gds.beta.graph.relationships.stream      Streams relationship topologies stored in a named graph.
* gds.graph.relationshipProperty.stream    Streams a single relationship property stored in a named graph.
* gds.graph.relationshipProperties.stream  Streams relationship properties stored in a named graph.
* gds.graph.nodeProperties.write           Writes node properties stored in a named graph to Neo4j.
* gds.graph.relationship.write             Writes relationships stored in a named graph to Neo4j.
* gds.graph.export                         Exports a named graph into a new offline Neo4j database.
* gds.beta.graph.export.csv                Exports a named graph into CSV files.

## Removing from the graph catalog
Removal operations
* gds.graph.drop                 Drops a named graph from the catalog.
* gds.graph.nodeProperties.drop  Removes node properties from a named graph.
* gds.graph.relationships.drop   Deletes relationships of a given relationship type from a named graph.

# Graph Management

## List graphs

```
CALL gds.graph.list()
YIELD graphName
```

## Running algorithms with other users' graphs

```
CALL gds.wcc.stats('graphB')
YIELD componentCount
```


```
CALL gds.wcc.stats('graphA', { username: 'alice' })
YIELD componentCount
```

## Dropping other users' graphs

```
CALL gds.graph.drop('graphA', true, '', 'bob')
YIELD graphName
```

# Degree Centrality

## Syntax

```
CALL gds.degree.stream(
  graphName: String,
  configuration: Map
) YIELD
  nodeId: Integer,
  score: Float
```

## Examples

```
CREATE
  (alice:User {name: 'Alice'}),
  (bridget:User {name: 'Bridget'}),
  (charles:User {name: 'Charles'}),
  (doug:User {name: 'Doug'}),
  (mark:User {name: 'Mark'}),
  (michael:User {name: 'Michael'}),

  (alice)-[:FOLLOWS {score: 1}]->(doug),
  (alice)-[:FOLLOWS {score: -2}]->(bridget),
  (alice)-[:FOLLOWS {score: 5}]->(charles),
  (mark)-[:FOLLOWS {score: 1.5}]->(doug),
  (mark)-[:FOLLOWS {score: 4.5}]->(michael),
  (bridget)-[:FOLLOWS {score: 1.5}]->(doug),
  (charles)-[:FOLLOWS {score: 2}]->(doug),
  (michael)-[:FOLLOWS {score: 1.5}]->(doug)
```

```
MERGE (:DarkMarket {name: \"" + str(market) + "\"})"
Cambiar por
MERGE (" + str(market) + ":DarkMarket {name: \"" + str(market) + "\"})"

MATCH (m:DarkMarket), (c:BTC)
WITH m, c, rand() AS r
WHERE r < 0.1  // Establecer la probabilidad de conexión entre un Market y un Cliente (en este caso, 0.1 o 10%)
CREATE (m)-[:BTC_ACCOUNT {score:c.balance}]->(c)
```


```
CALL gds.graph.project(
  'myGraph',
  'User',
  {
    FOLLOWS: {
      orientation: 'REVERSE',
      properties: ['score']
    }
  }
)
```

```
CALL gds.graph.project(
  'Grafo_BTC_Degree',
  'BTC',
  {
    BTC_ACCOUNT: {
      properties: ['score']
    }
  }
)
```

## Memory Estimation

```
CALL gds.degree.write.estimate('myGraph', { writeProperty: 'degree' })
YIELD nodeCount, relationshipCount, bytesMin, bytesMax, requiredMemory
```

```
CALL gds.degree.write.estimate('Grafo_BTC_Degree', { writeProperty: 'degree' })
YIELD nodeCount, relationshipCount, bytesMin, bytesMax, requiredMemory
```

## Stream

```
CALL gds.degree.stream('myGraph')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score AS followers
ORDER BY followers DESC, name DESC
```
```
CALL gds.degree.stream('Grafo_BTC_Degree')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score AS markets
ORDER BY markets DESC, name DESC
```
## Stats

```
CALL gds.degree.stats('myGraph')
YIELD centralityDistribution
RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore
```

## Mutate

```
CALL gds.degree.mutate('myGraph', { mutateProperty: 'degree' })
YIELD centralityDistribution, nodePropertiesWritten
RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten
```

## Write

```
CALL gds.degree.write('myGraph', { writeProperty: 'degree' })
YIELD centralityDistribution, nodePropertiesWritten
RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore, nodePropertiesWritten
```

## Weighted Degree Centrality example

```
CALL gds.degree.stream(
   'myGraph',
   { relationshipWeightProperty: 'score' }
)
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score AS weightedFollowers
ORDER BY weightedFollowers DESC, name DESC
```

## Setting an orientation

* NATURAL (default) corresponds to computing the out-degree of each node.
* REVERSE corresponds to computing the in-degree of each node.
* UNDIRECTED computes and sums both the out-degree and in-degree of each node.

```
CALL gds.degree.stream(
   'myGraph',
   { orientation: 'REVERSE' }
)
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score AS followees
ORDER BY followees DESC, name DESC
```





