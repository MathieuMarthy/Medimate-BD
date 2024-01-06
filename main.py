import json
import logging
import os
import time

from config import script_path
from Scraper import Scraper
from formatTable import TableFormat
from mongo.mongo import Mongo


# == logger == #
log_filepath = os.path.join(script_path, "log.txt")
logging.basicConfig(filename=log_filepath,
                    filemode="a",
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    encoding="utf-8",
                    level=logging.INFO)

def main():
    # == MongoDB == #
    mongo = Mongo(
        host=os.getenv("MONGO_HOST"),
        username=os.getenv("MONGO_USERNAME"),
        password=os.getenv("MONGO_PASSWORD")
    )

    # == Scrap == #
    scrapper = Scraper()
    urls = scrapper.get_files_to_download()

    # == Download == #
    for url in urls:
        scrapper.download_file(url)

    # == Format == #
    tableFormat = TableFormat()
    tableFormat.format_tables()

    # == Transform into mongo collection == #
    groups = tableFormat.get_medicines()
    filePath = os.path.join(script_path, "mongo/json/medicines_flat.json")
    groups.save_to_json_flat_data(filePath)

    # == Push data into mongo == #
    data = json.load(open(filePath, "r"))
    mongo.pushDataIntoMedicinesCollection(data)

if __name__ == "__main__":
    while True:
        try:
            main()
        except Exception as e:
            logging.error(e)
            continue

        logging.info("Sleeping...")
        time.sleep(12 * 60 * 60)  # 12 hours
