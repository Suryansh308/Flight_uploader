from pathlib import Path

import fitz  # PyMuPDF


class PDFExtractor:

    def __init__(self, pdf_path):

        self.pdf_path = Path(pdf_path)

        self.doc = fitz.open(self.pdf_path)

        self.page_count = len(self.doc)

    # ----------------------------------------------------------
    # Extract Words
    # ----------------------------------------------------------

    def get_page_words(self, page_index):

        page = self.doc.load_page(page_index)

        return page.get_text("words")

    # ----------------------------------------------------------
    # Save One Page as PDF
    # ----------------------------------------------------------

    def save_page_pdf(self, page_index):

        output_dir = self.pdf_path.parent / "split_pages"

        output_dir.mkdir(exist_ok=True)

        output_file = (
            output_dir /
            f"{self.pdf_path.stem}_page_{page_index + 1}.pdf"
        )

        new_pdf = fitz.open()

        new_pdf.insert_pdf(
            self.doc,
            from_page=page_index,
            to_page=page_index
        )

        new_pdf.save(output_file)

        new_pdf.close()

        return output_file

    # ----------------------------------------------------------
    # Get Trip Data
    # ----------------------------------------------------------

    def get_trip(self, page_index, parser):

        words = self.get_page_words(page_index)

        trip = parser.parse(
            words=words,
            page_number=page_index + 1
        )

        # Attach the actual PDF that belongs to this page
        trip.pdf_file = self.save_page_pdf(page_index)

        return trip

    # ----------------------------------------------------------
    # Close
    # ----------------------------------------------------------

    def close(self):

        if self.doc:

            self.doc.close()