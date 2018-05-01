import pymongo
import json
import codecs
import pprint
import timeit

client=pymongo.MongoClient('172.17.0.2')


def open_data():
    data = []
    with codecs.open('plz.json','rU','utf-8') as f:
        for line in f:
            data.append(json.loads(line))
    return data
def delete_db():
    client.drop_database('cities')
    #print(client.get_database())
def import_data():
    documents=open_data()
    for i in documents[:3]:
        print(i)
    db=client.cities
    plz_collection=db.plz
    start = timeit.default_timer()
    plz_collection.insert_many(documents)
    stop = timeit.default_timer()
    print('Running time for import : '+str(stop - start))
    #print(plz_collection)

def print_all():
    print(client.cities.plz)
    for c in client.cities.plz.find():
        pprint.pprint(c)

def get_loc_city(postcode):
    for c in client.cities.plz.find({'_id': postcode},{'loc':1,'city':1,'_id':0}):
        print('location and city for the postcode '+postcode+': ')
        print(c)
def get_postcode(city):
    for c in client.cities.plz.find({'city': city},{'_id':1}):
        print('Postcode '+city+': '+c['_id'])


delete_db()
import_data()  # run once to create database and collection
#print_all()    # check inserted data
get_loc_city('99034')   # TUMTUM postcode
get_postcode('TUMTUM')
get_postcode('HAMBURG')


