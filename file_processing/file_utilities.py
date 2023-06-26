# -*- coding: utf-8 -*-
import io
from PyPDF2 import PdfWriter


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
