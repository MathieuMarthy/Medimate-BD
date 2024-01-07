import logging
import os
import time

import pymongo

class Mongo:

    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username

        self.medicines_collection = "medicines"
        self.version_collection = "version"

        self.myclient = pymongo.MongoClient(
            host,
            username=username,
            password=password
        )
        logging.info("Connected to MongoDB")

        self.actualVersion = self.getVersion()
        logging.info(f"Actual version: {self.actualVersion}")


    def getOrCreateAndParamCollection(self, collection_name: str, index: str) -> pymongo.collection.Collection:
        db = self.myclient["database"]

        if collection_name in db.list_collection_names():
            return self.myclient["database"][collection_name]

        db.create_collection(collection_name)
        collection = db[collection_name]
        collection.create_index(index)

        logging.info(f"Created and parametrized {collection_name} collection")

        return collection

    def getMedicinesCollection(self) -> pymongo.collection.Collection:
        return self.getOrCreateAndParamCollection(self.medicines_collection, "code_cis")

    def getVersionCollection(self) -> pymongo.collection.Collection:
        return self.getOrCreateAndParamCollection(self.version_collection, "version")

    def pushDataIntoMedicinesCollection(self, data: list[dict]) -> list[int]:
        logging.info("Pushing data into medicines collection")
        start = time.time()

        medicines_collection = self.getMedicinesCollection()

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

        if len(updated_documents_cis) > 0:
            self.updateVersion(updated_documents_cis)

        return updated_documents_cis

    def getVersion(self) -> int:
        version_collection = self.getVersionCollection()

        document = version_collection.find_one([("version", pymongo.DESCENDING)])

        if document is None:
            document = {"version": 1}
            version_collection.insert_one(document)

        return document["version"]

    def updateVersion(self, updated_documents_cis: list[int]):
        logging.info(f"Updating version to {self.actualVersion + 1}")

        version_collection = self.getVersionCollection()
        self.actualVersion += 1

        version_collection.insert_one({
            "version": self.actualVersion,
            "updated_documents_cis": updated_documents_cis
        })

        logging.info(f"Version updated to {self.actualVersion} with {len(updated_documents_cis)} updated documents")

    def getMedicineByCis(self, cis: str):
        medicines_collection = self.getMedicinesCollection()

        medicine = medicines_collection.find_one({"_id": cis})

        return medicine


mongo = Mongo(
    host=os.getenv("MONGO_HOST"),
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD")
)
