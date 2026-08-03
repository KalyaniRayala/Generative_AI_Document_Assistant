import fitz


class PDFLoader:

    def load_pdf(self, file_path: str) -> str:

        text = ""

        with fitz.open(file_path) as document:

            for page in document:

                page_text = page.get_text()

                if page_text:
                    text += page_text + "\n"

        return text