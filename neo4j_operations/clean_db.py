import pandas as pd
import os

from neo4j import GraphDatabase


def load_transaction_list(name_csv):
    data_frame = pd.read_table(name_csv, delimiter=",")
    # print(data_frame.head())
    transaction_list = data_frame.values.tolist()
    return transaction_list


def execute_transactions(transaction_execution_commands):
    data_base_connection = GraphDatabase.driver(uri=URI, auth=(USER, PASS))
    # ope_provision = Neo4jConnection(URI, USER, PASS)

    my_session = data_base_connection.session()
    print("------------Node Provision--------------")
    print(transaction_execution_commands)
    print("----------Provision Complete--------------")

    for i in transaction_execution_commands:
        my_session.run(i)


def get_domain(name, domain_network):
    my_domain = "MERGE (d:Domain {name: \"" + name + "\", network: \"" + domain_network + "\"})"
    # print(my_domain)
    return my_domain


def get_child(name, domain_network, my_parent, parent_network):
    # Deprecated CREATE UNIQUE, at least replaced by MERGE
    # my_child = "MATCH (d:Domain {name: \"" + name + "\", network: \"" + domain_network + "\"}) MERGE (p:Domain {name: \"" + \
    #           my_parent + "\", network: \"" + parent_network + "\"}" + ") CREATE UNIQUE (p)<-[:CHILD {}]-(d) "
    my_child = "MATCH (d:Domain {name: \"" + name + "\", network: \"" + domain_network + "\"}) MERGE (p:Domain {name: \"" + \
               my_parent + "\", network: \"" + parent_network + "\"}" + ") MERGE (p)<-[:CHILD {}]-(d) "
    # print(my_child)
    return my_child


def upload_step_by_step(transaction_list):
    transaction_execution_commands = []

    ext_count = 0
    for i in transaction_list:
        name = str(i[0])
        domain_network = str(i[1])
        my_parent = str(i[2])
        parent_network = str(i[3])

        transaction_execution_commands.append(get_domain(name, domain_network))
        transaction_execution_commands.append(get_child(name, domain_network, my_parent, parent_network))
        ext_count += 1
        if ext_count == LIMIT:
            break;

    execute_transactions(transaction_execution_commands)


def main():
    data_base_connection = GraphDatabase.driver(uri=URI, auth=(USER, PASS))

    my_session = data_base_connection.session()

    command = """
    MATCH (n)
    DETACH DELETE n
    """
    print("------------Cleaning Database--------------")
    print(command)

    my_session.run(command)

    print("---------- Database Cleaned----------------")


if __name__ == "__main__":

    # URI = "bolt://localhost:7687"
    # URI = "bolt://neo4j_db:7687"
    # USER = "neo4j"
    # PASS = "crawler8"
    # CSV_NODES = "./i2p_results.csv"
    URI = os.environ.get('URI', 'bolt://neo4j_db:7687')     # Endpoint for bolt connection
    USER = os.environ.get('USER', 'neo4j')                  # DB User
    PASS = os.environ.get('PASS', 'crawler8')               # DB Pass
    LIMIT = int(os.environ.get('LIMIT', '100000'))          # Limit for node/relationships created
    CSV_NODES = os.environ.get('CSV_NODES', './i2p_results.csv')

    main()
