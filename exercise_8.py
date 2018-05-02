import pymongo
import json
import codecs
import pprint
import timeit
import datetime
import re
import ast

client=pymongo.MongoClient('172.17.0.2')

def prepare_data():
    temp=[]
    data=[]
    with codecs.open('sinndeslebens.txt','rU','utf-8') as f:
        for line in f:
            line = re.sub(r'name', '\'name\'', line)
            line = re.sub(r'gruendung', '\'gruendung\'', line)
            line = re.sub(r'farben', '\'farben\'', line)
            line = re.sub(r'Tabellenplatz', '\'Tabellenplatz\'', line)
            line = re.sub(r'nike', '\'nike\'', line)
            temp.append(line)
        f.close()
        for item in temp:
            data.append(ast.literal_eval(item))
        #print(data)
        final=[]
        for item in data:
            t=item['gruendung']
            item['gruendung']=datetime.date(t[0],t[1],t[2]).isoformat()
            final.append(item)

        with codecs.open('final_sinndeslebens.json', 'w', 'utf-8') as out:
            for item in final:
                json.dump(item,out)
                out.write('\n')
        out.close()
        with codecs.open('final_sinndeslebens.json', 'rU', 'utf-8') as f:
            for l in f:
                pprint.pprint(json.loads(l))
        f.close()


#prepare_data()


def open_data():
    data = []
    with codecs.open('final_sinndeslebens.json', 'rU', 'utf-8') as f:
        for l in f:
            data.append(json.loads(l))
    f.close()
    return data

def print_db():
    for c in client.fussball.teams.find():
        pprint.pprint(c)

def import_data():
    documents=open_data()
    db=client.fussball
    plz_collection=db.teams
    start = timeit.default_timer()
    plz_collection.insert_many(documents)
    stop = timeit.default_timer()
    print('Running time for import : '+str(stop - start))
    print_db()

def find_name(name):
    print('Teams with name ' + name + ': ')
    for c in client.fussball.teams.find({'name': name},{'_id':0}):
        print(c)

def find_nike_schwarz():
    print('Teams nike with schwarz: ')
    for c in client.fussball.teams.find({'nike':'j','farben':'schwarz'},{'_id':0}):
        print(c)

def find_nike_grunn_weiss():
    print('Teams nike with gruen and weiss: ')
    for c in client.fussball.teams.find({'nike':'j','farben':{ "$all" :['gruen','weiss']}},{'_id':0}):
           print(c)

def find_nike_grunn_or_weiss():
    print('Teams nike with gruen or weiss: ')
    for c in client.fussball.teams.find({'nike':'j','farben':{ "$in" :['gruen','weiss']}},{'_id':0}):
            print(c)

def max_tabellenPlatz():
    print('Teams max Tabellenplatz: ')
    c=client.fussball.teams.find_one({},{'_id':0},sort=[('Tabellenplatz', pymongo.DESCENDING)])
    print(c)
#############################   TO DO
def no_platz(): #chech this task better
    print('Teams with no place: ')
    for c in client.fussball.teams.find({'Tabellenplatz':'null'},{'_id':0}):
        print(c)

def oldest_nike_team():
    c=client.fussball.teams.find_one({'nike':'j'},{'name':1,'gruendung':1,'_id':0},sort=[('gruendung',pymongo.DESCENDING)])
    print('Oldest nike team: ')
    print(c)
##########################   TO DO
def update():   # to do!!! example of how to modify a field in a document
    client.fussball.teams.update({"username": "janedoe"},
                     {"$set": {"email": "janedoe74@example2.com", "score": 1}}, safe=True)
def delete_db():
    client.drop_database('fussball')

#delete_db()
#import_data()
find_name('Augsburg')
find_nike_schwarz()
find_nike_grunn_weiss()
find_nike_grunn_or_weiss()
max_tabellenPlatz()
no_platz()
oldest_nike_team()