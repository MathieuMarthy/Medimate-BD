from classes.table import Table
from datetime import datetime


class Dispo(Table):

    def __init__(self):
        super().__init__("CIS_CIP_Dispo_Spec.txt")
        self.colums_names = [
            "Code CIS", "Code CIP7", "CodeStatut", "Statut" # TODO: les dates miseAJour et RemiseDispo sont fusionnées
            "DateDebut", "DateMiseAJour", "DateRemiseDispo",
            "Lien vers la page du site ANSM",
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [
            "Code CIP7"
        ]

        self.df.drop(columns_to_delete, axis=1, inplace=True)

        self.date_format = "%d/%m/%Y"
        for date in ["DateDebut", "DateMiseAJour", "DateRemiseDispo"]:
            self.apply_func_to_col(date, self.convert_date)

        # remove line if "DateRemiseDispo" is already passed
        now = datetime.now()
        self.df = self.df[
            datetime.strptime(self.df["DateRemiseDispo"], "%Y-%m-%d")
            > now
        ]
