# -*- coding: utf-8 -*-
import io

from PyPDF2 import PdfReader, PdfWriter
from strawberry.file_uploads import Upload


async def decrypt_pdf(upload_file: Upload, password: str) -> Upload:
    # Create a new in-memory byte stream to hold the decrypted PDF content
    decrypted_content = io.BytesIO()

    # Read the contents of the Upload as bytes
    file_bytes = await upload_file.read()

    # Load the PDF content into a PyPDF2 PdfReader object
    pdf_reader = PdfReader(io.BytesIO(file_bytes))

    # Check if the PDF file is encrypted

    # Decrypt the PDF file using the provided password
    if pdf_reader.decrypt(password):
        # Create a new PyPDF2 PdfFileWriter object for the decrypted content
        pdf_writer = PdfWriter()

        # Copy all the pages from the decrypted PDF to the PdfFileWriter object
        for page_num in range(len(pdf_reader.pages)):
            pdf_writer.addPage(pdf_reader.getPage(page_num))

        # Write the decrypted content to the decrypted_content byte stream
        pdf_writer.write(decrypted_content)

        # Set the position of the byte stream to the beginning
        decrypted_content.seek(0)

        # Create a new UploadFile object with the decrypted content
        decrypted_upload_file = Upload(
            filename=upload_file.filename, content_type=upload_file.content_type
        )
        decrypted_upload_file.file.write(decrypted_content)

        return decrypted_upload_file
    else:
        raise Exception("The password is incorrect.")

    # If the PDF is not encrypted, return the original UploadFile object
    return upload_file
