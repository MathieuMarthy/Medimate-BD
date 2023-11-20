import json
import logging
import numpy as np
from typing import Optional

from mongo.collection.medicineData import *


class Medicine:
    name: str
    code_cis: str
    code_has: str
    type: MType
    sales_info: SalesInfos
    usage: Usage
    composition: Composition
    security_informations: SecurityInformations
    availability: Availbility
    generic_group: GenericGroup

    def __init__(self, name: str):
        self.name = name

    def set_name(self, new: str):
        self.name = new

    def set_code_cis(self, new: str):
        self.code_cis = new

    def set_code_has(self, new: str):
        self.code_has = new

    def set_type(self, new: MType):
        self.type = new

    def set_sales_info(self, new: SalesInfos):
        self.sales_info = new

    def set_usage(self, new: Usage):
        self.usage = new

    def set_composition(self, new: Composition):
        self.composition = new

    def set_security_informations(self, new: SecurityInformations):
        self.security_informations = new

    def set_availability(self, new: Availbility):
        self.availability = new

    def set_generic_group(self, new: GenericGroup):
        self.generic_group = new

    def __str__(self):
        return f"{self.name} - {self.code_cis}: {self.type}"

    def to_json(self) -> dict:
        data_json = {}

        for att, value in self.__dict__.items():
            if isinstance(value, Serializable):
                if value.is_empty():
                    data_json[att] = None
                else:
                    data_json[att] = value.to_json()

            else:
                data_json[att] = value

        return data_json


class Medicines:
    name: str
    medicines: list[Medicine]

    def __init__(self, name):
        self.name = name
        self.medicines = []

    def add_medicine(self, medicine: Medicine):
        self.medicines.append(medicine)

    def get_medicine(self, code_cis: str) -> Optional[Medicine]:
        for medicine in self.medicines:
            if medicine.code_cis == code_cis:
                return medicine

        return None

    def get_medicines(self) -> list[Medicine]:
        return self.medicines

    def to_json(self) -> dict:
        data_dict = {}
        for medicine in self.medicines:
            data_dict[medicine.code_cis] = medicine.to_json()

        return data_dict

    def __str__(self):
        return f"{self.name}: {len(self.medicines)}"


class Groups:
    list_medicines: list[Medicines]

    def __init__(self):
        self.list_medicines = []

    def add(self, medicines: Medicines):
        self.list_medicines.append(medicines)

    def add_medicine_into_group(self, medicine_to_add: Medicine):
        for medicines in self.list_medicines:
            if medicines.name == medicine_to_add.name:
                medicines.add_medicine(medicine_to_add)
                return

        self._create_new_medicines(medicine_to_add)

    def _create_new_medicines(self, medicine: Medicine):
        new_medicines = Medicines(medicine.name)
        new_medicines.add_medicine(medicine)
        self.list_medicines.append(new_medicines)

    def get_one_medicine_by_cis(self, code_cis: str) -> Optional[Medicine]:
        for medicines in self.list_medicines:

            medicine = medicines.get_medicine(code_cis)
            if medicine is not None:
                return medicine

        return None

    def get_one_medicines(self, name: str) -> Optional[Medicines]:
        name = name.upper()
        for medicines in self.list_medicines:
            if medicines.name == name:
                return medicines

        return None

    def to_json(self) -> dict:
        data_json = {}

        for medicines in self.list_medicines:
            data_json[medicines.name] = medicines.to_json()

        return data_json

    def save_to_json(self, filepath: str):
        try:
            json.dump(self.to_json(), open(filepath, "w", encoding="utf-8"), indent=4)
        except Exception:
            logging.error("error while trying save groups", exc_info=True)
