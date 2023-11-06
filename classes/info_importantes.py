import os
import re

from classes.table import Table


def find_file_name() -> str | None:
    files = os.listdir("csv")

    motif = re.compile(r'^CIS_InfoImportantes.*$')

    for file in files:
        if motif.match(file):
            return file

    return None


class Info(Table):

    def __init__(self):
        super().__init__(find_file_name())
        self.colums_names = [
            "Code CIS", "Date de début de l’information",
            "Date de fin de l’information de sécurité",
            "Texte à afficher et lien vers l’information de sécurité",
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [

        ]

        self.df.drop(columns_to_delete, axis=1)
        self.apply_func_to_col("Texte à afficher et lien vers l’information de sécurité", self.extract_link)

    def extract_link(self, txt: str) -> str:
        return re.findall(r"(?<=href=')[^']*", txt)[0]
