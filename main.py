import logging
import os

from dotenv import load_dotenv

from Scraper import Scraper
from formatTable import TableFormat
from mongo.mongo import Mongo

load_dotenv()

# == logger == #
logging.basicConfig(filename="log.txt",
                    filemode="a",
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    encoding="utf-8",
                    level=logging.INFO)

# == MongoDB == #
mongo = Mongo(
    host=os.getenv("MONGO_HOST"),
    username=os.getenv("MONGO_USERNAME"),
    password=os.getenv("MONGO_PASSWORD")
)

exit()

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
groups.save_to_json_flat_data("mongo/json/medicines_flat.json")
