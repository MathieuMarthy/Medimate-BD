from classes.table import Table


class Compo(Table):

    def __init__(self):
        super().__init__("CIS_COMPO_bdpm.txt")
        self.colums_names = [
            "Code CIS", "Désignation de l'élément pharmaceutique",
            "Code de la substance", "Dénomination de la substance",
            "Dosage de la substance", "Référence de ce dosage",
            "Nature du composant", "Numéro de liaison SA / FT",
            "autres"
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [

        ]

        self.df.drop(columns_to_delete, axis=1)
