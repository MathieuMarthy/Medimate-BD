from classes.table import Table


class Bdpm(Table):

    def __init__(self):
        super().__init__("CIS_bdpm.txt")
        self.colums_names = [
            "Code CIS", "Dénomination du médicament",
            "Forme pharmaceutique", "Voies d'administration",
            "Statut administratif de l’AMM", "Type de procédure d'AMM",
            "Etat de commercialisation", "Date d’AMM (format JJ/MM/AAAA)",
            "StatutBdm : «Alerte»/ «disponibilité »", "Numéro de l’autorisation européenne",
            "Titulaire(s)", "Surveillance renforcée (triangle noir) Oui/Non",
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [
            "Type de procédure d'AMM", "Date d’AMM (format JJ/MM/AAAA)",
            "StatutBdm : «Alerte»/ «disponibilité »", "Numéro de l’autorisation européenne",
            "Etat de commercialisation"
        ]

        self.df.drop(columns_to_delete, axis=1)

        # on garde que les médicaments qui sont commercialisés et autorisé
        self.df = self.df.loc[
            (self.df["Etat de commercialisation"] == "Commercialisée") &
            (self.df["Statut administratif de l’AMM"] == "Autorisation active")]
