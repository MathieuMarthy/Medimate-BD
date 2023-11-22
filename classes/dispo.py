from typing import Optional, Tuple
from datetime import datetime

import pandas as pd

from classes.table import Table


class Dispo(Table):

    def __init__(self):
        super().__init__("CIS_CIP_Dispo_Spec.txt")
        self.colums_names = [
            "Code CIS", "Code CIP7", "CodeStatut", "Statut",  # TODO: les dates miseAJour et RemiseDispo sont fusionnées
            "DateDebut", "DateMiseAJour", "DateRemiseDispo",  #
            "Lien vers la page du site ANSM",
        ]

        self.open_csv(1)

    def format(self):
        columns_to_delete = [
            "Code CIP7"
        ]

        self.df.drop(columns_to_delete, axis=1, inplace=True)

        self.date_format = "%d/%m/%Y"
        for date in ["DateDebut", "DateMiseAJour", "DateRemiseDispo"]:
            self.apply_func_to_col(date, self.convert_date)

        # remove line if "DateRemiseDispo" is already passed
        df = pd.DataFrame()
        df["DateRemiseDispo"] = pd.to_datetime(self.df["DateRemiseDispo"], errors="coerce")

        now = datetime.now()
        self.df = self.df[df["DateRemiseDispo"] >= now]


    def _split_date(self, date: str) -> Tuple[Optional[str], str]:
        if len(date) > 10:
            return date[:10], date[10:]
        return None, date



