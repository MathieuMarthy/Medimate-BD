import pandas as pd
from classes.bdpm import Bdpm
from classes.cip_bdpm import Cip
from classes.compo_bdpm import Compo
from classes.cpd_bdpm import Cpd
from classes.gener_bdpm import Gener
from classes.asmr_bdpm import Asmr
from classes.info_importantes import Info
from classes.lienpageCT_bdpm import Lienpage
from classes.smr_bdpm import Smr


class TableFormat:

    def __init__(self):
        self.Bdpm = Bdpm()
        self.Cip = Cip()
        self.Compo = Compo()
        self.Cpd = Cpd()
        self.Gener = Gener()
        self.Asmr = Asmr()
        self.Smr = Smr()
        self.Info = Info()
        self.Lienpage = Lienpage()

        self.tables = [
            self.Bdpm,
            self.Cip,
            self.Compo,
            self.Cpd,
            self.Gener,
            self.Asmr,
            self.Smr,
            self.Info,
            self.Lienpage
        ]

    def format_tables(self):
        """Format all the tables"""

        for table in self.tables:
            table.format()

        self._format_code_cis()

    def _format_code_cis(self):
        """Keep only the CIS Codes which are in all the tables"""

        tmp_tables = [table for table in self.tables if table not in [self.Bdpm, self.Lienpage]]

        # We delete the tables which have a CIS Code which is not in the Bdpm table
        for table in tmp_tables:
            table.df = table.df[table.df["Code CIS"].isin(self.Bdpm.df["Code CIS"])]

        # We do the opposite, the CIS Codes which are only in Bdpm are deleted
        df_codes_cis = [table.df["Code CIS"] for table in tmp_tables]

        all_CIS = pd.concat(df_codes_cis)
        all_CIS = all_CIS.drop_duplicates()
        self.Bdpm.df = self.Bdpm.df[self.Bdpm.df["Code CIS"].isin(all_CIS)]

    def print_tables(self):
        for table in self.tables:
            print(table)
