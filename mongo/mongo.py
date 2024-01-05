import pymongo

class Mongo:

    def __init__(self, host: str, username: str, password: str):
        self.host = host
        self.username = username

        self.myclient = pymongo.MongoClient(
            host,
            username=username,
            password=password
        )

        db_test = self.myclient["test"]
        if "ouais" not in db_test.list_collection_names():
            collec = db_test.create_collection("ouais")
        else:
            collec = db_test["ouais"]
        collec.insert_many([{"Solary": "C'est un bon gars"}, {"M8": "c'est un pas bon gars"}])
