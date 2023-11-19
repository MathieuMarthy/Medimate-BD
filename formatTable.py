import logging
import re
import time
from typing import Tuple, Optional, Type, Union

import pandas as pd
import uwutilities as uwu
from numpy import int64, NaN, nan, NAN

from classes.dispo import Dispo
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
from mongo.collection.medicineTypes import MedicineTypes
from mongo.collection.medicineData import *
from mongo.collection.medicines import Medicine, Groups
from unidecode import unidecode


class TableFormat:

    def __init__(self):
        self.Bdpm = Bdpm()
        self.Cip = Cip()
        self.Compo = Compo()
        self.Dispo = Dispo()
        self.Cpd = Cpd()
        self.Gener = Gener()
        self.Asmr = Asmr()
        # self.Smr = Smr()
        self.Info = Info()
        self.Lienpage = Lienpage()

        self.tables = [
            self.Bdpm,
            self.Cip,
            self.Compo,
            self.Cpd,
            self.Gener,
            self.Asmr,
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
        except Exception:
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

        all_cis = pd.concat(df_codes_cis)
        all_cis = all_cis.drop_duplicates()
        self.Bdpm.df = self.Bdpm.df[self.Bdpm.df["Code CIS"].isin(all_cis)]

    def print_tables(self):
        for table in self.tables:
            print(table)

    def get_medicines(self) -> Groups:
        start = time.time()
        groups = Groups()

        bar = uwu.Bar(self.Bdpm.df.shape[0])
        # collection medicine
        for code_cis in self.Bdpm.df["Code CIS"]:
            bar.next()
            medicine: Medicine

            bdpm = self._get_line_by_cis(self.Bdpm, code_cis)
            cip = self._get_line_by_cis(self.Cip, code_cis)
            compo = self._get_line_by_cis(self.Compo, code_cis)
            dispo = self._get_line_by_cis(self.Dispo, code_cis)
            cpd = self._get_line_by_cis(self.Cpd, code_cis)
            gener = self._get_line_by_cis(self.Gener, code_cis)
            asmr = self._get_line_by_cis(self.Asmr, code_cis)
            info = self._get_line_by_cis(self.Info, code_cis)

            lienpage: Optional[pd.DataFrame] = None
            has = self._get_value(asmr, "Code de dossier HAS")
            if has is not None:
                lienpage = self.Lienpage.df.loc[
                    self.Lienpage.df["Code de dossier HAS"] == has
                    ]

            title = self._get_value(bdpm, "Dénomination du médicament")
            m_name, m_weight = self._get_medicine_weight(title)

            type_wording = self._get_value(compo, "Désignation de l'élément pharmaceutique")
            if type_wording is None:
                type_wording = title

            m_type, m_true_type = self._get_generic_type(type_wording)

            # == Type
            medicine = Medicine(m_name)
            medicine.set_type(
                MType(
                    m_type,
                    m_true_type,
                    m_weight
                )
            )

            # == Usage
            link_help = None
            if lienpage is not None:
                link_help = self._get_value(lienpage, "Lien vers les pages d’avis de la CT")
            medicine.set_usage(
                Usage(
                    self._get_value(bdpm, "Voies d'administration"),
                    self._get_value(cpd, "Condition de prescription ou de délivrance"),
                    link_help
                )
            )

            # == Codes
            medicine.set_code_cis(code_cis)
            if has is not None:
                medicine.set_code_has(has)

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
                    self._get_value(info, "Date de début de l’information"),
                    self._get_value(info, "Date de fin de l’information de sécurité"),
                    self._get_value(info, "Texte à afficher et lien vers l’information de sécurité")
                )
            )

            # == Availbility
            medicine.set_availability(
                Availbility(
                    self._transform_in(self._get_value(dispo, "CodeStatut"), int),
                    self._get_value(dispo, "Statut"),
                    self._get_value(dispo, "DateDebut"),
                    self._get_value(dispo, "DateMiseAJour"),
                    self._get_value(dispo, "DateRemiseDispo"),
                    self._get_value(dispo, "Lien vers la page du site ANSM"),
                )
            )

            # == SalesInfos
            medicine.set_sales_info(
                SalesInfos(
                    self._get_value(bdpm, "Statut administratif de(s) la présentation(s)"),
                    self._get_value(bdpm, "Titulaire(s)"),
                    self._get_value(bdpm, "Surveillance renforcée (triangle noir) Oui/Non", Bdpm.get_surveillance),
                    self._transform_in(self._get_value(cip, "Code CIP7"), int),
                    self._transform_in(self._get_value(cip, "Code CIP13"), int),
                    self._get_value(cip, "Libellé de la présentation"),
                    self._get_value(cip, "Statut administratif de la présentation"),
                    self._get_value(cip, "Etat de commercialisation", Cip.get_is_on_sale),
                    self._get_value(cip, "Date de la déclaration de commercialisation"),
                    self._get_value(cip, "Taux de remboursement", Cip.get_refund_rate),
                    self._get_value(cip, "Conditions de remboursement"),
                    self._transform_in(self._get_value(cip, "Prix sans honoraire"), float),
                    self._transform_in(self._get_value(cip, "Prix"), float),
                )
            )

            # == GenericGroup
            medicine.set_generic_group(
                GenericGroup(
                    self._transform_in(self._get_value(gener, "Identifiant du groupe générique"), int),
                    self._get_value(gener, "Libellé du groupe générique"),
                    self._get_value(gener, "Type de générique"),
                    self._transform_in(self._get_value(gener, "Numéro de tri"), int),
                )
            )

            groups.add_medicine_into_group(medicine)
        bar.stop()

        logging.info(f"data restructuring took {time.time() - start} seconds")
        return groups

    def _transform_in(self, object_to_transform: Union[str, int, None], target_type: Type) -> Union[str, int, None]:
        """Transform an object in a type

        Args:
            object_to_transform: the object to transform
            target_type: the type to transform in

        Returns:
            str | int | None: the object transformed
        """
        try:
            resultat = target_type(object_to_transform)
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

    def _get_value(self, df: pd.DataFrame, column: str, apply_after_extract: Optional[callable] = None) -> any:
        """Get the value of a column

        Args:
            df: the dataframe
            column: the column
            apply_after_extract: a function to apply after the extract

        Returns:
            any: the value of the column or None
        """
        try:
            if df[column].empty:
                return None

            data = df[column].iloc[0]
            if data in [nan, NaN, NAN]:
                return None

            if isinstance(data, int64):
                data = int(data)

            if isinstance(data, str):
                data = data.strip()

            if apply_after_extract:
                return apply_after_extract(data)

            return data
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
