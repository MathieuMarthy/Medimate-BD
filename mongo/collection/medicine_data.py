

class Type:
    generic: str
    complet: str
    wieght: str


class Usage:
    route_administration: str
    condition_prescription_delivery: str


class Composition:
    substance_code: int
    substance_name: str
    substance_dosage: str
    substance_reference: str
    composant_type: str
    sa_ft_num: str


class SecurityInformations:
    start_date: str
    end_date: str
    text: str


class Availbility:
    code_statut: int
    statut: str
    start_date: str
    update_date: str
    end_date: str
    informations_link: str


class SalesInfos:
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
    price: float
    full_price: float


class GenericGroup:
    generic_group_id: int
    generic_group_name: str
    generic_type: str
    num: int
