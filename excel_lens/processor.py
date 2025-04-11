"""
processor.py
"""

import io
from typing import List, Dict, Any
from dataclasses import dataclass
import openpyxl
import pandas as pd
from pandas._typing import IntStrT
from PIL import Image


@dataclass
class ExcelSheet:
    """
    docstring
    """

    tables: List[pd.DataFrame]
    images: List[Image.Image]
    urls: List[dict]
    charts: List[Any]


@dataclass
class ExcelFile:
    """
    docstring
    """

    sheets: List[ExcelSheet]


class ExcelDataExtractor:
    """
    docstring
    """

    def __init__(self, excel_file: pd.DataFrame | dict[IntStrT, pd.DataFrame]):
        self.tables = []
        self.tables_dict = {}
        self.table_count = 1

    def run(self):
        self.extract_tables_sep_by_rows()
        self.extract_tables_sep_by_cols()
        self.remove_nan_rows()
        self.remove_nan_cols()
        self.extract_charts()
        self.extract_images()
        self.extract_urls()

    def remove_nan_rows(self, table: pd.DataFrame) -> pd.DataFrame:

        for idx, row in table.iterrows():
            if all(row.isnull()):
                table = table.drop(index=idx, axis=0).reset_index(drop=True)

    def remove_nan_cols(self, table: pd.DataFrame) -> pd.DataFrame:

        for col in table.columns:
            if all(table[col].isnull()):
                table = table.drop(columns=col, axis=1)

    def extract_tables_sep_by_rows(
        self, sheet_data: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:

        tables_dict = {}

        for idx, row in sheet_data.iterrows():

            # If the first row has null values skip
            if (idx == 0) and all(row.isnull()):
                continue

            # If any row is completely null it could be possible that there is a new table after that row
            if all(row.isnull()):
                if not tables_dict:
                    tables_dict[f"table_{table_count}"] = sheet_data.iloc[:idx, :]
                    curr_table_idx = idx
                else:
                    if len(sheet_data.iloc[curr_table_idx:idx, :]) == 1 and all(
                        sheet_data.iloc[curr_table_idx:idx, :].isnull()
                    ):
                        curr_table_idx = idx
                        continue
                    tables_dict[f"table_{table_count+1}"] = sheet_data.iloc[
                        curr_table_idx:idx, :
                    ]
                    curr_table_idx = idx
                    table_count += 1

            if idx == len(sheet_data) - 1:
                tables_dict[f"table_{table_count+1}"] = sheet_data.iloc[
                    curr_table_idx:, :
                ]

    def extract_tables_sep_by_cols(
        self, sheet_data: pd.DataFrame
    ) -> dict[str, pd.DataFrame]:

        tables_dict = {}

        for idx, col in enumerate(sheet_data.columns):

            # If the first row has null values skip
            if (idx == 0) and all(sheet_data[col].isnull()):
                continue

            # If any col is completely null it could be possible that there is a new table after that row
            if all(sheet_data[col].isnull()):
                if not tables_dict:
                    tables_dict[f"table_{table_count}"] = sheet_data[
                        sheet_data.columns[:idx]
                    ]
                    curr_table_idx = idx
                else:
                    print(table_count)
                    tables_dict[f"table_{table_count+1}"] = sheet_data[
                        sheet_data.columns[curr_table_idx:idx]
                    ]
                    curr_table_idx = idx
                    table_count += 1

            if col == sheet_data.columns[-1]:
                tables_dict[f"table_{table_count+1}"] = sheet_data[
                    sheet_data.columns[curr_table_idx:]
                ]

    def extract_urls(
        self, sheet_data: openpyxl.worksheet.worksheet.Worksheet
    ) -> List[str]:

        urls_data = []
        for row in sheet_data.iter_rows():
            for cell in row:
                if cell.hyperlink:
                    urls_data.append({cell.value: cell.hyperlink.target})
        return urls_data

    def extract_images(
        self, sheet_data: openpyxl.worksheet.worksheet.Worksheet
    ) -> List[Image.Image]:

        imgs_data = []
        for image in sheet_data._images:
            img_data = image._data()
            imgs_data.append(Image.open(io.BytesIO(img_data)))
        return imgs_data

    def extract_charts(
        self, sheet_data: openpyxl.worksheet.worksheet.Worksheet
    ) -> List[Any]:

        charts_data = []
        for chart in sheet_data._charts:
            charts_data.append(chart)
        return charts_data
