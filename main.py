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
from formatTable import TableFormat

tables: list[Table] = [
    Bdpm(),
    Cip(),
    Compo(),
    Cpd(),
    Gener(),
    Asmr(),
    # Smr(),
    Info(),
    Lienpage()
]

tableFormat = TableFormat(tables)
tableFormat.format_tables()
