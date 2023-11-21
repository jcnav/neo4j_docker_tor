import pandas as pd
import os

from neo4j import GraphDatabase
# from common.cypher_neo4j_connection import Neo4jConnection
from neo4j_operations.cypher.cypher_sentences import get_domain, get_child
from neo4j_operations.cypher.cypher_sentences import create_marketplaces_links, create_domains


def load_transaction_list(name_csv):
    data_frame = pd.read_table(name_csv, delimiter=",")
    print(data_frame.head())
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


def upload_step_by_step(transaction_list):
    transaction_execution_commands = []

    ext_count = 0
    for i in transaction_list:
        name = str(i[0])                # Origin
        domain_network = str(i[1])      # OriginNetwork
        my_parent = str(i[2])           # Destination
        parent_network = str(i[3])      # DestinationNetwork

        transaction_execution_commands.append(get_domain(name, domain_network))
        transaction_execution_commands.append(get_child(name, domain_network, my_parent, parent_network))

        # Maximum Values
        ext_count += 1
        if ext_count == LIMIT:
            break;

    execute_transactions(transaction_execution_commands)


def load_fields_marketplaces(row):
    MarketPlace = str(row[0])
    Name        = str(row[1])
    OnionLink   = str(row[2])
    Status      = str(row[3])
    Comment     = str(row[4])
    Comment2    = str(row[5])
    Categories  = str(row[6])
    return MarketPlace, Name, OnionLink, Status, Comment, Comment2, Categories


def load_fields_tor(row):
    Origin             = str(row[0])
    OriginNetwork      = str(row[1])
    Destination        = str(row[2])
    DestinationNetwork = str(row[3])
    return Origin, OriginNetwork, Destination, DestinationNetwork


def upload_step_by_step_marketplaces(transaction_list):
    transaction_execution_commands = []
    ext_count = 0

    for i in transaction_list:
        MarketPlace, Name, OnionLink, Status, Comment, Comment2, Categories = load_fields_marketplaces(i)
        print(MarketPlace)

        transaction_execution_commands.append(get_marketplaces(MarketPlace, Name, OnionLink))
        # Maximum Values
        ext_count += 1
        if ext_count == LIMIT:
            break;

    execute_transactions(transaction_execution_commands)


def generate_random_numbers(max_valor, cantidad_numeros):
    import numpy as np

    mu = 10     # Media de la distribución gaussiana
    sigma = 3   # Desviación estándar de la distribución gaussiana

    # Generar números aleatorios con distribución gaussiana
    numeros_gaussianos = np.random.normal(mu, sigma, cantidad_numeros)

    # Redondear los números generados a enteros y asegurarse de que estén dentro del rango [0, 20]
    numeros_enteros = [min(max(int(numero), 0), max_valor) for numero in numeros_gaussianos]

    print(numeros_enteros)
    return numeros_enteros


def upload_step_by_step_marketplaces_links(transaction_list_marketplace, transaction_list_nodes):
    len_marketplaces = len(transaction_list_marketplace)
    len_nodes = len(transaction_list_nodes)
    random_match_marketplaces = generate_random_numbers(len_marketplaces, len_nodes)

    transaction_execution_commands = []
    ext_count = 0

    for i in transaction_list_marketplace:
        Origin, OriginNetwork, Destination, DestinationNetwork = load_fields_tor(i)
        print(random_match_marketplaces[ext_count])
        transaction_execution_commands.append(create_marketplaces_links(Origin, OriginNetwork, transaction_list_marketplace[random_match_marketplaces[ext_count]]))
        transaction_execution_commands.append(create_domains(Origin, OriginNetwork))
        # Maximum Values
        ext_count += 1
        if ext_count == LIMIT:
            break;

    execute_transactions(transaction_execution_commands)


def main_i2p_tor():
    transaction_list = load_transaction_list(CSV_NODES)
    print(transaction_list)
    upload_step_by_step(transaction_list)


def main_marketplaces():
    # Create MarketPlaces
    transaction_list_marketplace = load_transaction_list(CSV_MARKETPLACES)
    upload_step_by_step_marketplaces(transaction_list_marketplace)
    # Create Nodes and Links with MarketPLaces
    transaction_list_nodes = load_transaction_list(CSV_NODES)
    upload_step_by_step_marketplaces_links(transaction_list_marketplace, transaction_list_nodes)


if __name__ == "__main__":

    tmp_uri = "bolt://localhost:7687"
    # tmp_uri = "bolt://neo4j_db:7687"
    tmp_pass = 'crawler8'
    tmp_user = 'neo4j'
    tmp_file_nodes = './/csv//tor_results.csv'
    tmp_file_market = './/csv//tor_marketplace.csv'

    URI = os.environ.get('URI', tmp_uri)                    # Endpoint for bolt connection
    USER = os.environ.get('USER', tmp_user)                 # DB User
    PASS = os.environ.get('PASS', tmp_pass)                 # DB Pass
    LIMIT = int(os.environ.get('LIMIT', '100000'))          # Limit for node/relationships created
    CSV_NODES = os.environ.get('CSV_NODES', tmp_file_nodes)
    CSV_MARKETPLACES = os.environ.get('CSV_MARKETPLACES', tmp_file_market)
    # main_i2p_tor()
    main_marketplaces()

