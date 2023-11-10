from classes.table import Table


class Cpd(Table):

    def __init__(self):
        super().__init__("CIS_CPD_bdpm.txt")
        self.colums_names = [
            "Code CIS",
            "Condition de prescription ou de délivrance",
        ]

        self.open_csv()

    def format(self):
        columns_to_delete = [

        ]

        self.df.drop(columns_to_delete, axis=1, inplace=True)
