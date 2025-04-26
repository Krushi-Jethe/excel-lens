# pylint disable = protected-access

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
    tables: Dict[str, pd.DataFrame]
    urls: Dict[str, str]

    @property
    def ntables(self) -> int:
        """
        Returns the number of tables present in a sheet.

        Returns:
            int: Number of tables.
        """
        return len(self.tables)


@dataclass
class ExcelFile:
    """
    docstring
    """

    raw: Dict[str, pd.DataFrame]
    sheets: Dict[str, ExcelSheet]

    @property
    def nsheets(self) -> int:
        """
        Returns the number of sheets present in the file.

        Returns:
            int: Number of sheets
        """
        return len(self.sheets)

    @property
    def sheet_names(self) -> List[str]:
        """
        Returns a list of sheet names present in the Excel File.

        Returns:
            List[str]: List of sheet names
        """
        return list(self.sheets.keys())

    def get_sheet(self, sheet_name: str) -> ExcelSheet:
        """
        Fetches sheet data

        Args:
            sheet_name (str): Name of the sheet

        Returns:
            ExcelSheet: Data present in the sheet
        """
        if sheet_name not in self.sheets:
            return ValueError(
                f"Sheet: {sheet_name} not found. Available sheets {self.sheet_names}"
            )
        return self.sheets[sheet_name]

    def __getitem__(self, sheet_name: str) -> ExcelSheet:
        return self.get_sheet(sheet_name)


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
            | str
            | Dict[IntStrT, pd.DataFrame]
            | Tuple[
                pd.DataFrame | Dict[IntStrT, pd.DataFrame],
                openpyxl.workbook.workbook.Workbook,
            ]
        ),
    ) -> ExcelFile:
        """
        Processes the data present in an excel file based on the input provided.

        Accepts inputs:
         - A pandas dataframe (to extract only tables data from single sheet)
         - Path to the excel file
         - Dictionary containing sheet name as keys and data present in that sheet as pandas
           dataframe for value. Output obtained from pd.read_excel(<YOUR_PATH_HERE>,sheet_name=None)
           Extracts only table data.
         - Tuple containing dictionary having sheet name and data as key value pairs and openpyxl
           workbook. File read using pandas should be the 1st element of the tuple and the one
           read by openpyxl should be second.

        Calls various methods to process data:
         - extract_tables_sep_by_rows
         - extract_tables_sep_by_cols
         - remove_nan_rows
         - remove_nan_cols
         - extract_urls
         - extract_images
         - extract_charts

        Args:
            excel_file (pd.DataFrame  |
                        str  |
                        Dict[IntStrT, pd.DataFrame]  |
                        Tuple[pd.DataFrame  |
                        Dict[IntStrT, pd.DataFrame],
                        openpyxl.workbook.workbook.Workbook]): Excel file to extract data from.

        Returns:
            ExcelFile: Processed data after extracting all tables, urls, images and
                       charts in ExcelFile dataclass.
        """

        if isinstance(excel_file, str):
            pandas_sheets = pd.read_excel(excel_file, sheet_name=None)
            openpyxl_sheets = openpyxl.load_workbook(excel_file)
            raw_excel_tables = pandas_sheets.copy()
        elif isinstance(excel_file, tuple):
            pandas_sheets = excel_file[0]
            openpyxl_sheets = excel_file[1]
            raw_excel_tables = pandas_sheets.copy()
        elif isinstance(excel_file, Dict):
            pandas_sheets = excel_file
            openpyxl_sheets = None
            raw_excel_tables = pandas_sheets.copy()
        else:
            pandas_sheets = {"sheet_1": excel_file}
            openpyxl_sheets = None
            raw_excel_tables = pandas_sheets.copy()

        sheet_names = raw_excel_tables.keys()

        extracted_sheets_dict = {}
        for sheet in sheet_names:

            row_tables = self.extract_tables_sep_by_rows(pandas_sheets[sheet])
            row_tables = {
                table_name: self.remove_nan_cols(table)
                for table_name, table in row_tables.items()
            }
            row_tables = {
                table_name: self.remove_nan_rows(table)
                for table_name, table in row_tables.items()
            }

            col_tables = self.extract_tables_sep_by_cols(pandas_sheets[sheet])
            col_tables = {
                table_name: self.remove_nan_cols(table)
                for table_name, table in col_tables.items()
            }
            col_tables = {
                table_name: self.remove_nan_rows(table)
                for table_name, table in col_tables.items()
            }

            if openpyxl_sheets:
                charts = self.extract_charts(openpyxl_sheets[sheet])
                images = self.extract_images(openpyxl_sheets[sheet])
                urls = self.extract_urls(openpyxl_sheets[sheet])
            else:
                charts, images, urls = [], [], []

            curr_extracted_sheet = ExcelSheet(
                charts=charts, images=images, tables=row_tables, urls=urls
            )
            extracted_sheets_dict[sheet] = curr_extracted_sheet

        extracted_excel_file = ExcelFile(
            raw=raw_excel_tables, sheets=extracted_sheets_dict
        )

        return extracted_excel_file

    def remove_nan_rows(self, table: pd.DataFrame) -> pd.DataFrame:
        """
        Scans the entire dataframe and gets rid of rows containing
        no entries/NaNs.

        Args:
            table (pd.DataFrame): Pandas dataframe from which we wish to
                                  remove rows containing all values as NaN.

        Returns:
            pd.DataFrame: Dataframe after removing NaN rows.
        """

        rows_to_drop = []

        for idx, row in table.iterrows():
            if all(row.isnull()):
                rows_to_drop.append(idx)

        table = table.drop(index=rows_to_drop, axis=0).reset_index(drop=True)

        return table

    def remove_nan_cols(self, table: pd.DataFrame) -> pd.DataFrame:
        """
        Scans the entire dataframe and gets rid of columns containing
        no entries/NaNs.

        Args:
            table (pd.DataFrame): Pandas dataframe from which we wish to
                                  remove columns containing all values as NaN.

        Returns:
            pd.DataFrame: Dataframe after removing NaN columns.
        """

        cols_to_drop = []

        for col in table.columns:
            if all(table[col].isnull()):
                cols_to_drop.append(col)

        table = table.drop(columns=cols_to_drop, axis=1).reset_index(drop=True)

        return table

    def extract_tables_sep_by_rows(
        self, sheet_data: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """


        Args:
            sheet_data (pd.DataFrame): An excel sheet as a pandas dataframe.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing dynamically assigned
                                     table names as keys and values as the table data
                                     which is a pandas dataframe
        """

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
                tables_dict[
                    f"table_{table_count+1}" if tables_dict else f"table_{table_count}"
                ] = sheet_data.iloc[curr_table_idx:, :]

        return tables_dict

    def extract_tables_sep_by_cols(
        self, sheet_data: pd.DataFrame
    ) -> Dict[str, pd.DataFrame]:
        """


        Args:
            sheet_data (pd.DataFrame): An excel sheet as a pandas dataframe.

        Returns:
            Dict[str, pd.DataFrame]: Dictionary containing dynamically assigned
                                     table names as key and values as the table data
                                     which is a pandas dataframe
        """

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
                tables_dict[
                    f"table_{table_count+1}" if tables_dict else f"table_{table_count}"
                ] = sheet_data[sheet_data.columns[curr_table_idx:]]
        return tables_dict

    def extract_urls(
        self, sheet_data: openpyxl.worksheet.worksheet.Worksheet
    ) -> Dict[str, str]:
        """
        Given an openpyxl worksheet the function returns all urls
        present in the sheet as key, value pairs where the value is
        the actual link and the key is the display name.

        Args:
            sheet_data (openpyxl.worksheet.worksheet.Worksheet): sheet from which urls
                                                                 needs to extracted.

        Returns:
            Dict[str, str]:
        """

        urls_data = {}
        for row in sheet_data.iter_rows():
            for cell in row:
                if cell.hyperlink:
                    urls_data[cell.value] = cell.hyperlink.target
        return urls_data

    def extract_images(
        self, sheet_data: openpyxl.worksheet.worksheet.Worksheet
    ) -> List[Image.Image]:
        """
        Given an openpyxl worksheet the function returns all images
        present in the sheet.

        Args:
            sheet_data (openpyxl.worksheet.worksheet.Worksheet): sheet from which images
                                                                 needs to extracted.

        Returns:
            List[Image.Image]: List containing PIL images.
        """

        imgs_data = []
        for image in sheet_data._images:
            img_data = image._data()
            imgs_data.append(Image.open(io.BytesIO(img_data)))
        return imgs_data

    def extract_charts(
        self, sheet_data: openpyxl.worksheet.worksheet.Worksheet
    ) -> List[Any]:
        """
        Given an openpyxl worksheet the function returns all charts
        present in the sheet

        Args:
            sheet_data (openpyxl.worksheet.worksheet.Worksheet): sheet from which charts
                                                                 needs to extracted.

        Returns:
            List[Any]: List containing charts data.
        """

        charts_data = []
        for chart in sheet_data._charts:
            charts_data.append(chart)
        return charts_data

    def generate_charts(self, charts_data: List[Any]) -> List[Image.Image]:
        """
        Uses charts data obtained from openpyxl and creates the charts using
        matplotlib which is then stored in a list after converting the matplotlib
        image to PIL image format.

        Args:
            charts_list (List[Any]): Charts data extracted from openpyxl.

        Returns:
            List[Image.Image]: List containing images of charts present.
        """

        charts_list = []

        for chart in charts_data:
            # code here
            charts_list.append("placeholder")

        return charts_list
