from pymongo import MongoClient
from faker import Faker
import random
from datetime import datetime
from pprint import pprint

user = 'loadtester'
password = 'loadtesterpassword'
MONGODB_URL = 'mongodb+srv://{user}:{password}@loadtest-xltug.mongodb.net/test?retryWrites=true'.format(user=user, password=password)

fake = Faker()

def main():
    conn = create_connection(MONGODB_URL)
    collection = conn['loaddb']['loadcollection']
    create_indexes(collection)
    gen_load(collection)

def create_connection(MongoDB_URL):
    return MongoClient(MongoDB_URL)
        
def create_indexes(collection):
    collection.create_index("To")
    
def gen_load(collection):
    while True:
        collection.insert(new_document())
        collection.find_one(new_to())
        collection.update_one(new_to(), new_update())
        collection.delete_one(new_from())

def new_document():
    doc = {
        "From": fake.first_name(),
        "To": fake.first_name(),
        "Hearts": random.randint(1,5),
        "Message": fake.text(max_nb_chars=100),
        "Date": fake.date_time_between_dates(datetime_start=datetime(2017,1,1),
                                             datetime_end=datetime(2019,1,1)),
        "State": fake.state_abbr()
        }
    return doc

def new_to():
    match = {
        "To": fake.first_name()
        }
    return match

def new_from():
    match = {
        "From": fake.first_name()
        }
    return match

def new_update():
    update = {
        "$set": {
            "Hearts": random.randint(1,5)
            }
        }
    return update

if __name__ == '__main__':
    main()
