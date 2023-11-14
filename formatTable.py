import logging
import re
from typing import Tuple

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
from classes.table import Table
from mongo.collection.collection import Collection
from mongo.collection.medicineTypes import MedicineTypes
from mongo.collection.medicine_data import *
from mongo.collection.medicines import Medicines, Medicine
from unidecode import unidecode


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

        logging.info("formating tables")
        for table in self.tables:
            table.format()

        try:
            self._format_code_cis()
        except Exception as e:
            logging.error("error while formating tables", exc_info=True)

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

    def get_mongo_collections(self) -> list[Collection]:
        medicines = Medicines()

        # collection medicine
        for code_cis in self.Bdpm.df["Code CIS"]:
            medicine: Medicine

            # Type
            bdpm = self._get_line_by_cis(self.Bdpm, code_cis)
            title = bdpm["Dénomination du médicament"]

            m_name, m_weight = self._get_medicine_weight(title)
            m_type, m_true_type = self._get_generic_type(title)

            medicine = medicines.get_or_add_medicine(m_name)
            medicine.set_type(Type(m_type, m_weight, m_true_type))

            # Usage
            medicine.set_usage(Usage())

            # Composition
            medicine.set_composition(Composition())

            # SecurityInformations
            medicine.set_security_informations(SecurityInformations())

            # Availbility
            medicine.set_availability(Availbility())

            # SalesInfos
            medicine.set_sales_info(SalesInfos())

            # GenericGroup
            medicine.set_generic_group(GenericGroup())

        return [medicines]

    def _get_line_by_cis(self, table: Table, code_cis: int):
        return table.df.loc[table.df["Code CIS"] == code_cis]

    def _get_medicine_weight(self, medicine_name: str):
        name_weight = medicine_name.split(",")[0]

        # find the first digit
        digit_index = re.search(r"\d", name_weight)

        # if no digit, return the name
        if not digit_index:
            return name_weight, None

        return name_weight[:digit_index.start()].strip(), name_weight[digit_index.start():].strip()

    def _get_generic_type(self, string: str) -> Tuple[str, str]:

        # solution injectable
        # perfusion
        # effervescent
        string = string.split(",")[-1]
        string = unidecode(string.strip().lower())

        for medi_type in MedicineTypes.types:
            if medi_type in string:
                return medi_type, string

        return "autre", string
