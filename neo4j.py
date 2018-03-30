import py2neo

from py2neo import Node, Relationship, Graph, authenticate

# I had to re-set the docker imag with the extre flag --env=NEO4J_AUTH=none to avoid authentification problems
authenticate("172.17.0.2:7474", "neo4j", "neo4j")
docker_graph=Graph("http://172.17.0.2:7474/db/data/")

