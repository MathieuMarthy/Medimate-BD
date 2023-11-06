from Scraper import Scraper
from formatTable import TableFormat

from classes.table import Table
from classes.getTable import get_table

# == Scrap
scrapper = Scraper()
urls = scrapper.get_files_to_download()

# == Download
tables: list[Table] = []
for url in urls:
    filename = scrapper.download_file(url)
    tables.append(get_table(filename))


# == Format
tableFormat = TableFormat()
tableFormat.format_tables()

tableFormat.print_tables()
