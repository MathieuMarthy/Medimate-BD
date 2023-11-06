from datetime import datetime

from classes.table import Table


class Asmr(Table):

    def __init__(self):
        super().__init__("CIS_HAS_ASMR_bdpm.txt")
        self.colums_names = [
            "Code CIS", "Code de dossier HAS", "Motif d’évaluation",
            "Date de l’avis de la Commission de la transparence",
            "Valeur de l'ASMR", "Libelle de l'ASMR"
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [
            "Motif d’évaluation",
            "Date de l’avis de la Commission de la transparence",
            "Valeur de l'ASMR", "Libelle de l'ASMR"
        ]

        self.df.drop(columns_to_delete, axis=1)

        self.date_format = "%Y%m%d"
        self.apply_func_to_col(
            "Date de l’avis de la Commission de la transparence",
            self.convert_date
        )
