from classes.table import Table


class Dispo(Table):

    def __init__(self):
        super().__init__("CIS_CIP_Dispo_Spec.txt")
        self.colums_names = [
            "Code CIS", "Code CIP7", "CodeStatut", "DateDebut",
            "DateMiseAJour", "DateRemiseDispo",
            "Lien vers la page du site ANSM",
        ]

        raise NotImplemented("Il faut changer le format des dates")
        self.open_csv()

    def format(self):
        columns_to_delete = [

        ]

        self.df.drop(columns_to_delete, axis=1)
