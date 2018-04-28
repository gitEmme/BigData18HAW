from neo4j.v1 import GraphDatabase
#to connect to the browser interface http://172.17.0.2:7474/browser/

uri = "bolt://172.17.0.2:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "neo4j"))


def run_statement(d, stat):
    with d.session() as session:
        with session.begin_transaction() as tx:
            tx.run(stat)

def run_query(d,query_statement,stringa):
    with d.session() as session:
        with session.begin_transaction() as tx:
            res=tx.run(query_statement)
            print(stringa)
            for record in res:
                print(record)

