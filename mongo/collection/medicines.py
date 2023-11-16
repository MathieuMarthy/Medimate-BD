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
        return f"{self.name} - {self.type_weight}"


class Medicines:
    name: str
    medicines: list[Medicine] = []

    def __init__(self, name):
        self.name = name

    def add_medicine(self, medicine: Medicine):
        self.medicines.append(medicine)

    def get_medicine(self, code_cis: str) -> Optional[Medicine]:
        for medicine in self.medicines:
            if medicine.code_cis == code_cis:
                return medicine

        return None

    def get_medicines(self) -> list[Medicine]:
        return self.medicines


class Groups:
    list_medicines: list[Medicines]

    def add(self, medicines: Medicines):
        self.list_medicines.append(medicines)

    def add_medicine_into_group(self, medicine_to_add: Medicine):
        for medicines in self.list_medicines:
            if medicines.name == medicine_to_add.name:
                medicines.add_medicine(medicine_to_add)
                return

        medicines = Medicines(medicine_to_add.name)
        medicines.add_medicine(medicine_to_add)
        self.list_medicines.append(medicines)

    def get_medicine_by_cis(self, code_cis: str) -> Optional[Medicine]:
        for medicines in self.list_medicines:

            medicine = medicines.get_medicine(code_cis)
            if medicine is not None:
                return medicine

        return None
