import logging

import pymongo

class Mongo:

    def __init__(self, host: str, username: str, password: str):
        self.medicines_collection = "medicines"
        self.host = host
        self.username = username

        self.myclient = pymongo.MongoClient(
            host,
            username=username,
            password=password
        )
        logging.info("Connected to MongoDB")


    def pushDataIntoMedicinesCollection(self, data: list[dict]):
        db = self.myclient["database"]
        medicines_collection = db[self.medicines_collection]

        medicines_collection.insert_many(data)
        logging.info("Data inserted into medicines collection")
