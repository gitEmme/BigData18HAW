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
r = redis.Redis(host='172.17.0.2', port=6379, db=0, decode_responses=True)

r.ping() # to check the connection



def open_data(conn,temp):
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
        print(type(i))

        city=temp['city']
        pop=temp['pop']
        state=temp['state']
        conn.hmset('_id:'+id,temp)
        conn.sadd('loc:'+loc,id)
        conn.sadd('city:'+city,id)
        conn.sadd('pop:'+pop,id)
        conn.sadd('state:'+state,id)

def load_to_redis(conn):
    with codecs.open('plz.json','rU','utf-8') as f:
        for line in f:
            temp=json.loads(line)
            #print(type(temp))
            id=str(temp['_id'])
            loc=''
            for t in temp['loc']:
                loc=loc+' '+str(t)
            city=temp['city']
            pop=str(temp['pop'])
            state=temp['state']
            conn.hmset('_id:'+id,temp)
            conn.sadd('loc:'+loc,id)
            conn.sadd('city:'+city,id)
            conn.sadd('pop:'+pop,id)
            conn.sadd('state:'+state,id)




#load_to_redis(r)

def retrieve_loc_state(conn, id):
    res=conn.hmget('_id:'+id,'loc','state')
    print(res)

def retrieve_postcode(conn,city_name):
    res=conn.smembers('city:'+city_name)
    print(res)


retrieve_loc_state(r,'01027')

retrieve_postcode(r,'TUMTUM')