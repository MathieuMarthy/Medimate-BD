import logging

from Scraper import Scraper
from formatTable import TableFormat

# == logger == #
logging.basicConfig(filename="log.txt",
                    filemode="a",
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    level=logging.INFO)
"""
# == Scrap == #
scrapper = Scraper()
urls = scrapper.get_files_to_download()

# == Download == #
for url in urls:
    scrapper.download_file(url)
"""

# == Format == #
tableFormat = TableFormat()
tableFormat.format_tables()

# == Transform into mongo collections == #
collections = tableFormat.get_mongo_collections()
print(collections)
