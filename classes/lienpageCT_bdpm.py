from classes.table import Table


class Lienpage(Table):

    def __init__(self):
        super().__init__("HAS_LiensPageCT_bdpm.txt")
        self.colums_names = [
            "Code de dossier HAS",
            "Lien vers les pages d’avis de la CT"
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [

        ]

        self.df.drop(columns_to_delete, axis=1)