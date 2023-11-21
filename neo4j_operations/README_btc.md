# Using Degree Algorithm with Markets and BTC data

## Data Provision
Execute the program loading csv files
```
example_market_btc.py
```

The csv files (in data subdirectory) are:
* btc_100.csv: Contains BTC accounts and the relative balances
* tor_marketplace.csv: Contains Markets nodes

The cypher sentences are:

* Create markets

```
    MERGE (:DarkMarket {name: \"" + str(market) + "\"})"
```

* Add the BTC nodes

```
    MERGE (:BTC {name: \"" + str(btc) + "\" , balance: " + balance + "})
```

* Create the relations based on a probability function 

```
    MATCH (m:DarkMarket), (c:BTC)
    WITH m, c, rand() AS r
    WHERE r < 0.1  // Establecer la probabilidad de conexión entre un Market y un Cliente (en este caso, 0.1 o 10%)
    CREATE (m)-[:BTC_ACCOUNT {score:c.balance}]->(c)
```




## Cypher Commands

The gds project uses one dynamic name. In this example the name is *Grafo_BTC_Degree*

* Graph creation

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

* Memory required estimation
```
CALL gds.degree.write.estimate('Grafo_BTC_Degree', { writeProperty: 'degree' })
YIELD nodeCount, relationshipCount, bytesMin, bytesMax, requiredMemory
```

* Degree calculation

```
CALL gds.degree.stream('Grafo_BTC_Degree')
YIELD nodeId, score
RETURN gds.util.asNode(nodeId).name AS name, score AS markets
ORDER BY markets DESC, name DESC
```

* Other statistics

```
CALL gds.degree.stats('Grafo_BTC_Degree')
YIELD centralityDistribution
RETURN centralityDistribution.min AS minimumScore, centralityDistribution.mean AS meanScore
```

