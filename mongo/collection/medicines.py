from typing import Optional

from mongo.collection.medicine_data import *


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
        self.type_weight = {}

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
        return f"{self.name} - {self.type_weight}"


class Medicines:
    medicines: list[Medicine] = []

    def _get_medicine_by_name(self, name) -> Optional[Medicine]:
        for medicine in self.medicines:
            if medicine.name == name:
                return medicine
        return None

    def get_or_add_medicine(self, medicine_name: str) -> Medicine:
        medicine = self._get_medicine_by_name(medicine_name)

        if not medicine:
            medicine = Medicine(medicine_name)
            self.medicines.append(medicine)

        return medicine

    def get_medicine(self, medicine_name: str) -> Optional[Medicine]:
        for medicine in self.medicines:
            if medicine.name == medicine_name.upper():
                return medicine

        return None
