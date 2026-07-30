import fitz


class PDFLoader:

    def load_pdf(self, file_path: str):

        document = fitz.open(file_path)

        text = ""

        for page in document:
            text += page.get_text()

        document.close()

        return text