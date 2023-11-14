import logging
import re
import time
from typing import Tuple, Optional, Type, Union

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
        start = time.time()
        for table in self.tables:
            table.format()

        try:
            self._format_code_cis()
        except Exception as e:
            logging.error("error while formating tables", exc_info=True)
        logging.info(f"formating tables done in {time.time() - start} seconds")

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

    def get_mongo_collections(self) -> Medicines:
        start = time.time()
        medicines = Medicines()

        # collection medicine
        for code_cis in self.Bdpm.df["Code CIS"]:
            medicine: Medicine

            bdpm = self._get_line_by_cis(self.Bdpm, code_cis)
            cip = self._get_line_by_cis(self.Cip, code_cis)
            compo = self._get_line_by_cis(self.Compo, code_cis)
            cpd = self._get_line_by_cis(self.Cpd, code_cis)
            gener = self._get_line_by_cis(self.Gener, code_cis)
            asmr = self._get_line_by_cis(self.Asmr, code_cis)
            smr = self._get_line_by_cis(self.Smr, code_cis)
            info = self._get_line_by_cis(self.Info, code_cis)

            lienpage: Optional[pd.DataFrame] = None
            has = self._get_value(asmr, "Code de dossier HAS")
            if has is not None:
                lienpage = self.Lienpage.df.loc[
                    self.Lienpage.df["Code de dossier HAS"] == has
                ]

            # == Type
            title = self._get_value(bdpm, "Dénomination du médicament")
            m_name, m_weight = self._get_medicine_weight(title)

            type_wording = self._get_value(compo, "Désignation de l'élément pharmaceutique")
            if type_wording is None:
                type_wording = title

            m_type, m_true_type = self._get_generic_type(type_wording)

            medicine = medicines.get_or_add_medicine(m_name)
            medicine.set_type(
                MType(
                    m_type,
                    m_true_type,
                    m_weight
                )
            )

            # == Usage
            medicine.set_usage(
                Usage(
                    self._get_value(bdpm, "Voies d'administration"),
                    self._get_value(cip, "Condition de prescription ou de délivrance")
                )
            )

            # == Composition
            medicine.set_composition(
                Composition(
                    self._transform_in(self._get_value(compo, "Code de la substance"), int),
                    self._get_value(compo, "Dénomination de la substance"),
                    self._get_value(compo, "Dosage de la substance"),
                    self._get_value(compo, "Référence de ce dosage"),
                    self._get_value(compo, "Nature du composant"),
                    self._get_value(compo, "Numéro de liaison SA/FT"),
                )
            )

            # == SecurityInformations
            medicine.set_security_informations(
                SecurityInformations(

                )
            )

            # == Availbility
            medicine.set_availability(
                Availbility(

                )
            )

            # == SalesInfos
            medicine.set_sales_info(
                SalesInfos(

                )
            )

            # == GenericGroup
            medicine.set_generic_group(
                GenericGroup(

                )
            )

        logging.info(f"get mongo collections done in {time.time() - start} seconds")
        return medicines

    def _transform_in(self, object: Union[str, int, None], type: Type) -> Union[str, int, None]:
        """Transform an object in a type

        Args:
            object: the object to transform
            type: the type to transform in

        Returns:
            str | int | None: the object transformed
        """
        try:
            resultat = type(object)
            return resultat
        except (ValueError, TypeError):
            return None

    def _get_line_by_cis(self, table: Table, code_cis: int) -> pd.DataFrame:
        """Get the line of a table by CIS Code

        Args:
            table: the table
            code_cis: the CIS Code

        Returns:
            pd.DataFrame: the line of the table
        """
        return table.df.loc[table.df["Code CIS"] == code_cis]

    def _get_value(self, df: pd.DataFrame, column: str) -> Optional[str]:
        """Get the value of a column

        Args:
            df: the dataframe
            column: the column

        Returns:
            str | None: the value of the column or None
        """
        try:
            if df[column].empty:
                return None
            data_list = df[column].iloc
            return data_list[0]
        except KeyError:
            return None


    def _get_medicine_weight(self, medicine_name: str) -> Tuple[str, Optional[str]]:
        """Get the weight of a medicine

        Args:
            medicine_name: the name of the medicine

        Returns:
            str: the name of the medicine
            str | None: the weight of the medicine or None
        """
        name_weight = medicine_name.split(",")[0]

        # find the first digit
        digit_index = re.search(r"\d", name_weight)

        # if no digit, return the name
        if not digit_index:
            return name_weight, None

        return name_weight[:digit_index.start()].strip(), name_weight[digit_index.start():].strip()

    def _get_generic_type(self, string: str) -> Tuple[str, str]:
        """Get the generic type of a medicine

        Args:
            string: the string to analyse

        Returns:
            str: the category of the medicine
            str: the full type string
        """
        string = string.split(",")[-1]
        string = unidecode(string.strip().lower())

        for medi_type in MedicineTypes.types:
            if medi_type in string:
                return medi_type, string

        return "autre", string
