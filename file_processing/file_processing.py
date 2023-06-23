# -*- coding: utf-8 -*-
import io
import logging
import typing
from abc import ABC, abstractmethod
from dataclasses import dataclass

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
    def read_file(self, file_path: typing.Union[str, bytes]):
        try:
            tables = tabula.read_pdf(
                io.BytesIO(file_path), pages="all", stream=True, lattice=True
            )
        except Exception as e:
            logging.error(e)
            return None
        dataframes = []
        for i in range(1, len(tables)):
            df = pd.DataFrame(tables[i])
            dataframes.append(df)

        # Concatenate all DataFrames into a single DataFrame
        concatenated_df = pd.concat(dataframes, ignore_index=True)

        return concatenated_df


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
    factory: FileReaderFactory

    def process_file(self, file_path):
        reader = self.factory.create_file_reader()
        data = reader.read_file(file_path)
        # Process the data as needed
        return data


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
