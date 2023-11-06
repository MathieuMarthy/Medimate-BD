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

        self.df.drop(columns_to_delete, axis=1)

        self.date_format = "%d/%m/%Y"
        self.apply_func_to_col("Date de la déclaration de commercialisation", self.convert_date)
