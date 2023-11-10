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

        self.df.drop(columns_to_delete, axis=1, inplace=True)

        ## "Libelle de l'ASMR"
        # self.df["Libelle de l'ASMR"].replace("\x92", "'", regex=True, inplace=True)

        ## "Valeur de l'ASMR"
        # for libelle in [
        #     "Commentaires sans chiffrage de l'ASMR",
        #     "Sans objet",
        #     "Non précisée"
        # ]:
        #     self.df["Valeur de l'ASMR"].replace(libelle, "?", inplace=True)

