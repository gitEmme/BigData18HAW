from neo4j.v1 import GraphDatabase
#to connect to the browser interface http://172.17.0.3:7474/browser/

uri = "bolt://172.17.0.3:7687"
driver = GraphDatabase.driver(uri, auth=("neo4j", "password"))

def create_labeled(d,name):
    with d.session() as session:
        with session.begin_transaction() as tx:
            tx.run("CREATE (s:Module {name: $name})", name=name)

def create_nodes():
    lista=['Calculus 1','Calculus 2','Linear Algebra','Discrete Mathematics','Programming','Computer Architecture','Law for Computer Science',
           'English for Computer Science','English B2','Physics 1','Database Systems','Operating Systems','Algorithms and Data Structures',
           'NoSQL Big Data','Distributed Systems','Project Big Data','German Language','Security in distributed Systems','Robot Vision','Business English',
           'Seminar Software & Sound','Practical Network Security']
    for item in lista:
        create_labeled(driver,item)

def run_statement(d, stat):
    with d.session() as session:
        with session.begin_transaction() as tx:
            tx.run(stat)

#### in each statement a.name is the class from which connection start a--> and in the list are specified the classes to connect a to
def set_connections():  # to use just once
    calculus1="MATCH (a:Module), (b:Module) WHERE a.name='Calculus 1' AND b.name IN ['Calculus 2','Physics 1','Project Big Data','Robot Vision'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    linearalgebra="MATCH (a:Module), (b:Module) WHERE a.name='Linear Algebra' AND b.name IN ['Programming','Robot Vision','Algorithms and Data Structures'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    discretemath="MATCH (a:Module), (b:Module) WHERE a.name='Discrete Mathematics' AND b.name IN ['Calculus 1','Linear Algebra','Programming','Computer Architecture','Algorithms and Data Structures','Project Big Data'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    programming="MATCH (a:Module), (b:Module) WHERE a.name='Programming' AND b.name IN ['Computer Architecture','Database Systems','Operating Systems','Algorithms and Data Structures','NoSQL Big Data','Distributed Systems','Project Big Data','Security in distributed Systems','Robot Vision','Practical Network Security'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    english="MATCH (a:Module), (b:Module) WHERE a.name='English B2' AND b.name IN ['Seminar Software & Sound','English for Computer Science','Business English'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    calculus2="MATCH (a:Module), (b:Module) WHERE a.name='Calculus 2' AND b.name IN ['Physics 1'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    operatingsys="MATCH (a:Module), (b:Module) WHERE a.name='Operating Systems' AND b.name IN ['Distributed Systems'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    distributedsys="MATCH (a:Module), (b:Module) WHERE a.name='Distributed Systems' AND b.name IN ['Security in distributed Systems'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    databases="MATCH (a:Module), (b:Module) WHERE a.name='Database Systems' AND b.name IN ['NoSQL Big Data'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    algorithms="MATCH (a:Module), (b:Module) WHERE a.name='Algorithms and Data Structures' AND b.name IN ['Programming'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    german="MATCH (a:Module), (b:Module) WHERE a.name='German Language' AND b.name IN ['NoSQL Big Data','Distributed Systems','Project Big Data','Security in distributed Systems','Robot Vision','Seminar Software & Sound','Practical Network Security'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    security="MATCH (a:Module), (b:Module) WHERE a.name='Security in distributed Systems' AND b.name IN ['Practical Network Security'] CREATE (a)-[r:REQUIRED_FOR]->(b)"
    run_statement(driver, calculus1)
    run_statement(driver, english)
    run_statement(driver, linearalgebra)
    run_statement(driver,discretemath)
    run_statement(driver, programming)
    run_statement(driver, calculus2)
    run_statement(driver, operatingsys)
    run_statement(driver, distributedsys)
    run_statement(driver, databases)
    run_statement(driver,algorithms)
    run_statement(driver, german)
    run_statement(driver, security)


def run_query(d,query_statement,stringa):
    with d.session() as session:
        with session.begin_transaction() as tx:
            res=tx.run(query_statement)
            print(stringa)
            for record in res:
                print(record)

#####################QUERIES#########################################################
query_end_nodes="MATCH (b:Module) WHERE NOT (b)-[]->() RETURN b"
query_required_bigdata="MATCH (a:Module),(b:Module) WHERE b.name='NoSQL Big Data' AND (a)-[]->(b) RETURN a"


create_nodes() # use it only once to create nodes
set_connections()

run_query(driver,query_end_nodes,'End nodes:')
run_query(driver,query_required_bigdata,'Required for Big Data:')