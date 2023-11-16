from typing import Optional

from classes.table import Table


class Cip(Table):

    def __init__(self):
        super().__init__("CIS_CIP_bdpm.txt")
        self.colums_names = [
            "Code CIS", "Code CIP7", "Libellé de la présentation",
            "Statut administratif de la présentation",
            "Etat de commercialisation",
            "Date de la déclaration de commercialisation",
            "Code CIP13", "Agrément aux collectivités",
            "Taux de remboursement", "Prix sans honoraire",
            "Prix",
            "Honoraire", "Conditions de remboursement",
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [
            "Agrément aux collectivités"
        ]

        self.df.drop(columns_to_delete, axis=1, inplace=True)

        self.date_format = "%d/%m/%Y"
        self.apply_func_to_col("Date de la déclaration de commercialisation", self.convert_date)

    @staticmethod
    def get_is_on_sale(string: Optional[str]) -> bool:
        if string:
            return string == "Déclaration de commercialisation"
        return False


    @staticmethod
    def get_refund_rate(string: Optional[str]) -> Optional[int]:
        if string:
            return int(string.replace("%", "").strip())
        return None
