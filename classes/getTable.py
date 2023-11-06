
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

filename_table = {
    "CIS_bdpm.txt": Bdpm,
    "CIS_CIP_bdpm.txt": Cip,
    "CIS_CIP_Dispo_Spec.txt": Dispo,
    "CIS_COMPO_bdpm.txt": Compo,
    "CIS_CPD_bdpm.txt": Cpd,
    "CIS_GENER_bdpm.txt": Gener,
    "CIS_HAS_ASMR_bdpm.txt": Asmr,
    "CIS_HAS_SMR_bdpm.txt": Smr,
    "CIS_InfoImportantes.txt": Info,
    "HAS_LiensPageCT_bdpm.txt": Lienpage
}


def get_table(filename: str) -> Table | None:
    try:
        return filename_table[filename]
    except KeyError:
        return None
