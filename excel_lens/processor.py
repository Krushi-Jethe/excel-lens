"""
processor.py
"""

import io
from typing import List, Tuple, Dict, Any
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

    charts: List[Any]
    images: List[Image.Image]
    tables: List[Dict[str,pd.DataFrame]]
    urls: List[dict]


@dataclass
class ExcelFile:
    """
    docstring
    """

    raw: Dict[str, pd.DataFrame]
    sheets: List[ExcelSheet]


class ExcelDataExtractor:
    """
    docstring
    """

    def __init__(
        self,
    ):

        self.tables = []
        self.tables_dict = {}
        self.table_count = 1

    def extract(
        self,
        excel_file: (
            pd.DataFrame
            | dict[IntStrT, pd.DataFrame]
            | str
            | Tuple[
                pd.DataFrame | dict[IntStrT, pd.DataFrame],
                openpyxl.workbook.workbook.Workbook,
            ]
        ),
    ) -> ExcelFile:

        extracted_excel_sheets = []

        if isinstance(excel_file, str):
            pandas_sheets = pd.read_excel(excel_file, sheet_name=None)
            openpyxl_sheets = openpyxl.load_workbook(excel_file)
            raw_excel_tables = pandas_sheets.copy()
        elif isinstance(
            excel_file,
            Tuple[
                pd.DataFrame | dict[IntStrT, pd.DataFrame],
                openpyxl.workbook.workbook.Workbook,
            ],
        ):
            pandas_sheets = excel_file[0]
            openpyxl_sheets = excel_file[1]
            raw_excel_tables = pandas_sheets.copy()
        elif isinstance(excel_file, dict[IntStrT, pd.DataFrame]):
            pandas_sheets = excel_file
            openpyxl_sheets = None
            raw_excel_tables = pandas_sheets.copy()
        else:
            pandas_sheets = {"sheet_1": excel_file}
            openpyxl_sheets = None
            raw_excel_tables = pandas_sheets.copy()

        sheet_names = raw_excel_tables.keys()

        extracted_sheets_list = []
        for sheet in sheet_names:

            row_tables = self.extract_tables_sep_by_rows(pandas_sheets[sheet])
            row_tables = {table_name: self.remove_nan_cols(table) for table_name, table in row_tables.items()}
            row_tables = {table_name: self.remove_nan_rows(table) for table_name, table in row_tables.items()}

            col_tables = self.extract_tables_sep_by_cols(pandas_sheets[sheet])
            col_tables = {table_name: self.remove_nan_cols(table) for table_name, table in col_tables.items()}
            col_tables = {table_name: self.remove_nan_rows(table) for table_name, table in col_tables.items()}

            if openpyxl_sheets:
                charts = self.extract_charts(openpyxl_sheets[sheet])
                images = self.extract_images(openpyxl_sheets[sheet])
                urls = self.extract_urls(openpyxl_sheets[sheet])
            else:
                charts = []
                images = []
                urls = []

            curr_extracted_sheet = ExcelSheet(charts=charts, images=images, tables=row_tables, urls=urls)
            extracted_sheets_list.append(curr_extracted_sheet)

        extracted_excel_file = ExcelFile(raw=raw_excel_tables, sheets=extracted_sheets_list)

        return extracted_excel_file

    def remove_nan_rows(self, table: pd.DataFrame) -> pd.DataFrame:
        rows_to_drop = []

        for idx, row in table.iterrows():
            if all(row.isnull()):
                rows_to_drop.append(idx)

        table = table.drop(index=rows_to_drop, axis=0).reset_index(drop=True)

        return table

    def remove_nan_cols(self, table: pd.DataFrame) -> pd.DataFrame:

        cols_to_drop = []
        for col in table.columns:
            if all(table[col].isnull()):
                cols_to_drop.append(col)
    
        table = table.drop(columns=cols_to_drop, axis=1).reset_index(drop=True)

        return table

    def extract_tables_sep_by_rows(
        self, sheet_data: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:

        tables_dict = {}
        table_count = 1
        curr_table_idx = 0

        for idx, row in sheet_data.iterrows():

            # If the first row has null values skip
            if (idx == 0) and all(row.isnull()):
                continue

            # If any row is completely null it could be possible
            # that there is a new table after that row
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

        return tables_dict

    def extract_tables_sep_by_cols(
        self, sheet_data: pd.DataFrame
    ) -> dict[str, pd.DataFrame]:

        tables_dict = {}
        table_count = 1
        curr_table_idx = 0

        for idx, col in enumerate(sheet_data.columns):

            # If the first row has null values skip
            if (idx == 0) and all(sheet_data[col].isnull()):
                continue

            # If any col is completely null it could be possible
            # that there is a new table after that row
            if all(sheet_data[col].isnull()):
                if not tables_dict:
                    tables_dict[f"table_{table_count}"] = sheet_data[
                        sheet_data.columns[:idx]
                    ]
                    curr_table_idx = idx
                else:
                    tables_dict[f"table_{table_count+1}"] = sheet_data[
                        sheet_data.columns[curr_table_idx:idx]
                    ]
                    curr_table_idx = idx
                    table_count += 1

            if col == sheet_data.columns[-1]:
                tables_dict[f"table_{table_count+1}"] = sheet_data[
                    sheet_data.columns[curr_table_idx:]
                ]
        return tables_dict

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
