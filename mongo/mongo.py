import logging
import time

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

    def getOrCreateAndParamMedicinesCollection(self):
        db = self.myclient["database"]

        if self.medicines_collection in db.list_collection_names():
            return self.myclient["database"][self.medicines_collection]

        db.create_collection(self.medicines_collection)
        medicines_collection = db[self.medicines_collection]
        medicines_collection.create_index("code_cis")

        logging.info("Created and parametrized medicines collection")

        return medicines_collection

    def pushDataIntoMedicinesCollection(self, data: list[dict]) -> list[int]:
        start = time.time()

        medicines_collection = self.getOrCreateAndParamMedicinesCollection()

        updated_documents_cis = []
        for document in data:
            existing_document = medicines_collection.find_one({"_id": document["code_cis"]})

            if existing_document is not None:
                del existing_document["_id"]

            # Si le document existant est différent du nouveau document, remplacez-le
            if existing_document != document:
                medicines_collection.replace_one(
                    {"_id": document["code_cis"]},  # condition
                    document,  # new document to insert
                    upsert=True  # insert the document if it does not exist
                )
                updated_documents_cis.append(document["code_cis"])

        logging.info(f"Data inserted into medicines collection. Number of inserted documents: {len(updated_documents_cis)}")
        logging.info(f"Time elapsed: {time.time() - start} seconds")

        return updated_documents_cis
