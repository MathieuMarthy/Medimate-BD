from typing import Optional

from mongo.collection.collection import Collection


class Medicine:
    name: str
    type_weight: dict

    def __init__(self, name: str):
        self.name = name
        self.type_weight = {}

    def add_type_weight(self, medicine_type: str, weight: str):
        self.type_weight[medicine_type] = list(set(self.type_weight.get(medicine_type, []) + [weight]))

    def __str__(self):
        return f"{self.name} - {self.type_weight}"


class Medicines(Collection):
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
