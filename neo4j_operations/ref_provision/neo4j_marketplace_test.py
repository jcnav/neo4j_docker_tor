import pandas as pd



template = """
//skip null values
LOAD CSV WITH HEADERS FROM '{csv_file}}' AS row
WITH row WHERE row.Id IS NOT NULL
MERGE (c:Company {companyId: row.Id});

// clear data
MATCH (n:Company) DELETE n;

//set default for null values
LOAD CSV WITH HEADERS FROM 'file:///companies.csv' AS row
MERGE (c:Company {companyId: row.Id, hqLocation: coalesce(row.Location, "Unknown")})

// clear data
MATCH (n:Company) DELETE n;

//change empty strings to null values (not stored)
LOAD CSV WITH HEADERS FROM 'file:///companies.csv' AS row
MERGE (c:Company {companyId: row.Id})
SET c.emailAddress = CASE trim(row.Email) WHEN "" THEN null ELSE row.Email END
"""


def build_cypher_provision(csv_file):
    csv_file = "file:///companies.csv"


def load_headers_from_csv(csv_file):
    df = pd.read_csv(csv_file)
    print(df)
    print(df.columns)


if __name__ == "__main__":
    headers = {"MarketPlace", "Name", "OnionLink", "Status", "Comment", "Comment2", "Categories"}

    name_file = '../csv/tor_marketplace.csv'
    load_headers_from_csv(name_file)
