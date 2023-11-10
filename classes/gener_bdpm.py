from classes.table import Table


class Gener(Table):

    def __init__(self):
        super().__init__("CIS_GENER_bdpm.txt")
        self.colums_names = [
            "Identifiant du groupe générique",
            "Libellé du groupe générique",
            "Code CIS", "Type de générique",
            "Numéro de tri", "autres"
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [

        ]

        self.df.drop(columns_to_delete, axis=1, inplace=True)
