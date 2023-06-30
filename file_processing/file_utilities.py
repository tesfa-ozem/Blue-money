# -*- coding: utf-8 -*-
import io
from PyPDF2 import PdfWriter
from strawberry.file_uploads import Upload


async def decrypt_pdf(pdf_reader, password: str):
    try:
        # Create a new in-memory byte stream to hold the decrypted PDF content
        decrypted_content = io.BytesIO()

        # Decrypt the PDF file using the provided password
        if pdf_reader.decrypt(password):
            # Create a new PyPDF2 PdfFileWriter object for the decrypted content
            pdf_writer = PdfWriter()

            # Copy all the pages from the decrypted
            # PDF to the PdfFileWriter object
            for page_number in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_number]
                pdf_writer.add_page(page)

            # Write the decrypted content to the decrypted_content byte stream
            pdf_writer.write(decrypted_content)

            # Set the position of the byte stream to the beginning
            decrypted_content.seek(0)

            # Create a custom Upload object with necessary attributes

            return decrypted_content.getvalue()
        else:
            raise Exception("The password is incorrect.")

    except Exception as e:
        # Handle any exceptions that occur during decryption
        # e.g., invalid PDF format, decryption error, etc.
        raise Exception("Failed to decrypt PDF: " + str(e))


def validate_pdf_file(file: Upload):
    # Validate file type
    allowed_file_types = [
        "text/csv",
        "application/vnd.ms-excel",
        "application/pdf",
    ]
    if file.content_type not in allowed_file_types:
        return Exception(
            "Invalid file type. Only CSV \
            and XLSX files are accepted."
        )

    # Validate file size
    max_file_size = 5 * 1024 * 1024  # 5 MB
    if file.size > max_file_size:
        return Exception("File size exceeds the limit of 5MB.")
