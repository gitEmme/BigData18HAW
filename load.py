import docker
import redis
import json
import codecs
from pprint import pprint
client = docker.from_env() # Connect to Docker using the default socket or the configuration in your environment


container=client.containers()
images=client.images()


# To get the connection to the docker container running redis run on command line: $  docker container inspect redisimg
#Look for the ip address of the container and copy it to host in the Redis( ...) function otherwise You can't connect
# $ docker exec -it redisimg redis-cli -p 6379:6379
r = redis.Redis(host='172.17.0.2', port=6379, db=0)

r.ping() # to check the connection

def open_data():
    data = []
    with codecs.open('plz.json','rU','utf-8') as f:
        for line in f:
           data.append(json.loads(line))    # this way im obtaining a list of Python dictionaries
    for i in data:
        id=i['_id']
        loc=i['loc']
        city=i['city']
        pop=i['pop']
        state=i['state']
        print(state)
