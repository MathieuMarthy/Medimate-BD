from abc import ABC
from datetime import datetime
from typing import Union, Optional

import pandas as pd
from uwutilities import String_tools


class Table(ABC):
    encoding: str
    file_name: str
    df: pd.DataFrame
    colums_names: list[str]
    date_format: str

    def __init__(self, file_name: str) -> None:
        self.encoding = "latin-1"
        self.file_name = file_name

    def open_csv(self):
        """Open csv file and save it in a pandas dataframe"""
        self.df = pd.read_csv(f"csv/{self.file_name}", sep="\t", encoding=self.encoding, names=self.colums_names)

    def format(self):
        """Format the dataframe"""
        pass

    def print_colums(self):
        """Print the columns of the dataframe"""
        print(self.df.columns)

    def apply_func_to_col(self, target: str, func: callable):
        """Apply a function to a column of the dataframe

        Args:
            target (str): column name
            func (callable): function to apply
        """
        self.df[target] = self.df[target].apply(lambda row: func(row))

    def convert_date(self, date_str: Union[int, str]) -> Optional[str]:
        """Convert a date from a format to another

        Args:
            date_str (int | str): the date to convert 
            date_format (str): the format of the date

        Returns:
            str: the converted date
        """
        if date_str is None:
            return None

        try:
            date = datetime.strptime(str(date_str), self.date_format)
            return date.strftime("%Y-%m-%d")
        except ValueError:
            return None

    def __str__(self):
        return f"{self.__class__.__name__}: {self.df.shape[0]} élément{String_tools.singular_or_plural(self.df.shape[0])}"
