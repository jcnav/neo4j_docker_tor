import pandas as pd
import os

from neo4j import GraphDatabase
from loguru import logger


def execute_transactions(transaction_execution_commands):
    data_base_connection = GraphDatabase.driver(uri=URI, auth=(USER, PASS))
    # ope_provision = Neo4jConnection(URI, USER, PASS)

    my_session = data_base_connection.session()
    print("------------Node Provision--------------")
    # print(transaction_execution_commands)
    print("----------Provision Complete--------------")

    for i in transaction_execution_commands:
        # print(i)
        my_session.run(i)


def load_transaction_list(name_csv):
    data_frame = pd.read_table(name_csv, delimiter=",")
    # print(data_frame.head())
    transaction_list = data_frame.values.tolist()
    return transaction_list


def create_marketplaces(market):
    my_market = "MERGE (:DarkMarket {name: \"" + str(market) + "\"})"
    # print(my_market)
    return my_market


def build_relations_random():
    command = """
    MATCH (m:DarkMarket), (c:Email)
    WITH m, c, rand() AS r
    WHERE r < 0.1  // Establecer la probabilidad de conexión entre un Market y un Cliente (en este caso, 0.1 o 10%)
    CREATE (m)-[:VENDOR]->(c)
    """
    execution_queue = [command]
    execute_transactions(execution_queue)


def build_create_emails(transaction_list):
    transaction_execution_commands = []
    for i in transaction_list:
        email = str(i[0])
        transaction_execution_commands.append(create_emails(email))
    execute_transactions(transaction_execution_commands)


def create_emails(email):
    print(email)
    my_email = "MERGE (:Email {name: \"" + str(email) + "\"})"
    # print(my_email)
    return my_email


def load_fields_marketplaces(row):
    MarketPlace = str(row[0])
    Name        = str(row[1])
    OnionLink   = str(row[2])
    Status      = str(row[3])
    Comment     = str(row[4])
    Comment2    = str(row[5])
    Categories  = str(row[6])
    return MarketPlace, Name, OnionLink, Status, Comment, Comment2, Categories


def build_create_markets(transaction_list):
    transaction_execution_commands = []
    print("--- Lista de markets ---")
    print(transaction_list)
    print("------------------------")

    for i in transaction_list:
        MarketPlace, Name, OnionLink, Status, Comment, Comment2, Categories = load_fields_marketplaces(i)
        print(MarketPlace)
        transaction_execution_commands.append(create_marketplaces(MarketPlace))
    execute_transactions(transaction_execution_commands)


def main_markets_email():
    emails = load_transaction_list(CSV_EMAILS)
    dark_markets = load_transaction_list(CSV_MARKETPLACES)

    build_create_markets(dark_markets)
    build_create_emails(emails)
    build_relations_random()


if __name__ == "__main__":

    tmp_uri = "bolt://localhost:7687"
    # tmp_uri = "bolt://neo4j_db:7687"
    tmp_pass = 'crawler8'
    tmp_user = 'neo4j'
    tmp_file_email = '../csv/emails_100.csv'
    tmp_file_market = '../csv/tor_marketplace.csv'

    URI = os.environ.get('URI', tmp_uri)                    # Endpoint for bolt connection
    USER = os.environ.get('USER', tmp_user)                 # DB User
    PASS = os.environ.get('PASS', tmp_pass)                 # DB Pass
    LIMIT = int(os.environ.get('LIMIT', '100000'))          # Limit for node/relationships created
    CSV_EMAILS = os.environ.get('CSV_NODES', tmp_file_email)
    CSV_MARKETPLACES = os.environ.get('CSV_MARKETPLACES', tmp_file_market)

    main_markets_email()
