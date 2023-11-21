# Cypher sentences for different test

# ### Tor and I2P relations ###
def get_domain(name, domain_network):
    # Create/Update nodes Origin en la red OriginNetwork
    my_domain = "MERGE (d:Domain {name: \"" + name + "\", network: \"" + domain_network + "\"})"
    # print(my_domain)
    return my_domain


def get_child(name, domain_network, my_parent, parent_network):
    my_child = "MATCH (d:Domain {name: \"" + name + "\", network: \"" + domain_network + "\"}) MERGE (p:Domain {name: \"" + \
               my_parent + "\", network: \"" + parent_network + "\"}" + ") MERGE (p)<-[:CHILD {}]-(d) "
    # print(my_child)
    return my_child


# ### Marketplaces and relations
def create_marketplaces(market, name, link):
    # Create/Update nodes Origin en la red OriginNetwork
    my_domain = "MERGE (d:Domain {MarketPlace: \"" + market + "\", Name: \"" + name + "\", Link: \"" + link + "\"})"
    # print(my_domain)
    return my_domain


def create_domains(name, domain_network):
    # Create/Update nodes Origin en la red OriginNetwork
    my_domain = "MERGE (d:Domain {name: \"" + name + "\", network: \"" + domain_network + "\"})"
    # print(my_domain)
    return my_domain


def create_marketplaces_links(Origin, OriginNetwork, row):
    #print(Origin)
    #print(OriginNetwork)
    #print(row)
    name = Origin
    domain_network = row[1] # OriginNetwork
    my_parent = row[0]
    parent_network = row[1]

    my_child = "MATCH (d:Domain {name: \"" + name + "\", network: \"" + domain_network + "\"}) MERGE (p:Domain {name: \"" + \
                my_parent + "\", network: \"" + parent_network + "\"}" + ") MERGE (p)<-[:CHILD {}]-(d) "
    # print(my_child)
    return my_child

