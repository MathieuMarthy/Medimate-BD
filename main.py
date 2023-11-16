import logging

from Scraper import Scraper
from formatTable import TableFormat
from mongo.collection.medicines import Medicines

# == logger == #
logging.basicConfig(filename="log.txt",
                    filemode="a",
                    format="%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s",
                    datefmt="%H:%M:%S",
                    encoding="utf-8",
                    level=logging.INFO)

# == Scrap == #
# scrapper = Scraper()
# urls = scrapper.get_files_to_download()
#
# # == Download == #
# for url in urls:
#     scrapper.download_file(url)


# == Format == #
tableFormat = TableFormat()
tableFormat.format_tables()


# == Transform into mongo collection == #
groups = tableFormat.get_medicines()

print(groups.get_one_medicines("salut"))
