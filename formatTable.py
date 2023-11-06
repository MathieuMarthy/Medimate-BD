from classes.table import Table


class TableFormat:

    def __init__(self, tables: list[Table]):
        self.tables = tables

    def format_tables(self):
        for table in self.tables:
            table.format()


        #