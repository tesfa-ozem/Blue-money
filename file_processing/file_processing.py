# -*- coding: utf-8 -*-
import io
import logging
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass
from PyPDF2 import PdfReader
from .file_utilities import decrypt_pdf

import openpyxl
import pandas as pd
import tabula


@dataclass
class FileReader(ABC):
    @abstractmethod
    def read_file(self, file_path):
        pass


@dataclass
class PDFFileReader(FileReader):
    async def read_file(self, file_bytes: typing.Union[str, bytes]):
        try:
            pdf_reader = PdfReader(io.BytesIO(file_bytes))
            if pdf_reader.is_encrypted:
                # Decrypt the PDF using the provided password
                file_bytes = await decrypt_pdf(pdf_reader, "474833")

            first_table = tabula.read_pdf(
                io.BytesIO(file_bytes),
                pages=1,
                stream=True,
                lattice=True,
                guess=False,
                area=[336.8, 0.0, 740.0, 595.0],
            )
            tables = tabula.read_pdf(
                io.BytesIO(file_bytes),
                pages="all",
                stream=True,
                lattice=True,
                guess=False,
                area=[5.8, 0.0, 740.0, 595.0],
            )
        except Exception as e:
            logging.error(e)
            return None
        dataframes = []
        dataframes.append(first_table[0])
        for i in range(2, len(tables)):
            df = pd.DataFrame(tables[i])
            dataframes.append(df)

        # Concatenate all DataFrames into a single DataFrame
        concatenated_df = pd.concat(dataframes, ignore_index=True)
        df_columns = concatenated_df.columns.tolist()
        new_column_names = [
            "reference",
            "time",
            "details",
            "status",
            "paid_in",
            "paid_out",
            "balance",
        ]
        new_column_names_object = dict(zip(df_columns, new_column_names))
        renamed_df = concatenated_df.rename(columns=new_column_names_object)
        processed_df = renamed_df.applymap(
            lambda x: x.replace("\r", "") if isinstance(x, str) else x
        )
        clean_df = processed_df.drop("Unnamed: 0", axis=1)
        clean_df.fillna("0.0", inplace=True)
        return clean_df


@dataclass
class CSVFileReader(FileReader):
    def read_file(self, file_path):
        return pd.read_csv(file_path)


@dataclass
class XLSXFileReader(FileReader):
    def read_file(self, file_path):
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active
        data = []
        for row in sheet.iter_rows(values_only=True):
            data.append(row)
        return pd.DataFrame(data)


@dataclass
class FileReaderFactory(ABC):
    @abstractmethod
    def create_file_reader(self) -> FileReader:
        pass


@dataclass
class PDFFileReaderFactory(FileReaderFactory):
    def create_file_reader(self) -> FileReader:
        return PDFFileReader()


@dataclass
class CSVFileReaderFactory(FileReaderFactory):
    def create_file_reader(self) -> FileReader:
        return CSVFileReader()


@dataclass
class XLSXFileReaderFactory(FileReaderFactory):
    def create_file_reader(self) -> FileReader:
        return XLSXFileReader()


@dataclass
class FileProcessor:
    file_type: str
    file_factory = {
        "application/pdf": PDFFileReaderFactory(),
        "text/csv": CSVFileReaderFactory(),
        "application/vnd.ms-excel": XLSXFileReaderFactory(),
    }

    def process_file(self, file_path):
        factory = self.file_factory.get(self.file_type)
        reader = factory.create_file_reader()
        df = reader.read_file(file_path)
        # Process the data as needed
        return df


# # Usage example
# file_path = "path/to/your/file.pdf"  # Replace with the actual file path
# file_extension = file_path.split(".")[-1].lower()

# if file_extension == "pdf":
#     factory = PDFFileReaderFactory()
# elif file_extension == "csv":
#     factory = CSVFileReaderFactory()
# elif file_extension == "xlsx":
#     factory = XLSXFileReaderFactory()
# else:
#     raise ValueError("Unsupported file type.")

# processor = FileProcessor(factory)
# data = processor.process_file(file_path)
# print(data)
