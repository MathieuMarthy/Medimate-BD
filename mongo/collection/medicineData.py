from dataclasses import dataclass
from typing import Optional


class Serializable:

    def to_json(self) -> Optional[dict]:
        return self.__dict__

    def is_empty(self) -> bool:
        for value in self.__dict__.values():
            if value is not None:
                return False
        return True

@dataclass
class MType(Serializable):
    generic: str
    complet: str
    weight: str


@dataclass
class Usage(Serializable):
    route_administration: str
    condition_prescription_delivery: str
    link_help: str


@dataclass
class Composition(Serializable):
    substance_code: int
    substance_name: str
    substance_dosage: str
    substance_reference: str
    composant_type: str
    sa_ft_num: str


@dataclass
class SecurityInformations(Serializable):
    start_date: str
    end_date: str
    text: str


@dataclass
class Availbility(Serializable):
    code_statut: int
    statut: str
    start_date: str
    update_date: str
    end_date: str
    informations_link: str


@dataclass
class SalesInfos(Serializable):
    administrative_status: str
    holder: str
    surveillance: bool
    CIP7: str
    CIP13: str
    presentation: str
    presentation_status: str
    is_on_sale: bool
    date_marketing_declaration: str
    refund_rate: int
    refund_conditions: str
    price_no_tax: float
    full_price: float


@dataclass
class GenericGroup(Serializable):
    generic_group_id: int
    generic_group_name: str
    generic_type: str
    num: int
