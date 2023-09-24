from datetime import datetime
from pymongo import MongoClient, DESCENDING

class GenericRepository:
    def __init__(self, db_name, collection_name):
        self.client = MongoClient('mongodb://localhost:27017/')
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def get_last_document(self):
        return self.collection.find_one(sort=[('_id', DESCENDING)])
    
    def list_all_documents(self, filter: dict = {}):
        return list(self.collection.find(filter))
    
    def count_documents(self, filter: dict = {}):
        return self.collection.count_documents(filter)

    def insert_document(self, document):
        self.collection.insert_one(document)

    def insert_many_documents(self, documents):
        self.collection.insert_many(documents)

    def remove_document(self, id):
        self.collection.delete_one({'_id': id})
