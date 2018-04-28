#import docker
import redis
import json
import codecs
import timeit
#client = docker.from_env() # Connect to Docker using the default socket or the configuration in your environment


#container=client.containers()
#images=client.images()

# To get the connection to the docker container running redis run on command line: $  docker container inspect redisimg
#Look for the ip address of the container and copy it to host in the Redis( ...) function otherwise You can't connect
# $ docker exec -it redisimg redis-cli -p 6379:6379
r = redis.Redis(host='172.17.0.2', port=6379, db=0, decode_responses=True)

#redis://172.17.0.3:6379
r.ping() # to check the connection

def compute_time():
    start = timeit.default_timer()
    stop = timeit.default_timer()
    print('Running time for import : '+ str(stop - start))
def delete_db():
    r.flushall()
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
        print(type(i))

def load_to_redis(conn):
    total_time=0
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
            start = timeit.default_timer()
            conn.hmset('_id:'+id,temp)
            stop = timeit.default_timer()
            conn.sadd('loc:'+loc,id)
            conn.sadd('city:'+city,id)
            conn.sadd('pop:'+pop,id)
            conn.sadd('state:'+state,id)
            #stop = timeit.default_timer()
            total_time+=stop-start
        print('Running time for import : '+ str(total_time))


def retrieve_loc_state(conn, id):
    res=conn.hmget('_id:'+id,'loc','state')
    print(res)

def retrieve_postcode(conn,city_name):
    res=conn.smembers('city:'+city_name)
    print(res)


delete_db()
load_to_redis(r)
retrieve_loc_state(r,'01027')
retrieve_postcode(r,'TUMTUM')
