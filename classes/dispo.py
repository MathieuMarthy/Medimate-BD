from typing import Optional, Tuple
from datetime import datetime

from classes.table import Table

class Dispo(Table):

    def __init__(self):
        super().__init__("CIS_CIP_Dispo_Spec.txt")
        self.colums_names = [
            "Code CIS", "Code CIP7", "CodeStatut", "Statut",
            "DateDebut", "DateRemiseDispo", "DateMiseAJour",
            "Lien vers la page du site ANSM",
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [
            "Code CIP7"
        ]

        self.df.drop(columns_to_delete, axis=1, inplace=True)

        self.df.dropna(inplace=True)

        ## seperation of "DateMiseAJour" and "DateRemiseDispo"
        # self.df["DateMiseAJour"], self.df["DateRemiseDispo"] = zip(
        #     *self.df["DateRemiseDispo"].map(self._split_date)
        # )

        self.date_format = "%d/%m/%Y"
        for date in ["DateDebut", "DateMiseAJour", "DateRemiseDispo"]:
            self.apply_func_to_col(date, self.convert_date)

        # remove line if "DateRemiseDispo" is already passed
        now = datetime.now()
        datetime_dispo = self.df["DateRemiseDispo"].apply(self._string_to_date)
        self.df = self.df[
            datetime_dispo > now
        ]

    def _string_to_date(self, date: str) -> datetime:
        return datetime.strptime(date, "%Y-%m-%d")

    def _split_date(self, date: str) -> Tuple[Optional[str], str]:
        if len(date) > 10:
            return date[:10], date[10:]
        return None, date
