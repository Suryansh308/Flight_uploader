import json
from pathlib import Path


class ProgressManager:

    def __init__(self):

        self.file = Path("progress.json")

        if not self.file.exists():

            self.reset()

    # -------------------------------------------------

    def reset(self):

        data = {
            "current_pdf": "",
            "completed_pages": [],
            "failed_pages": []
        }

        self.file.write_text(
            json.dumps(data, indent=4)
        )

    # -------------------------------------------------

    def load(self):

        return json.loads(
            self.file.read_text()
        )

    # -------------------------------------------------

    def save(self, data):

        self.file.write_text(
            json.dumps(data, indent=4)
        )

    # -------------------------------------------------

    def start_pdf(self, pdf_name):

        data = self.load()

        data["current_pdf"] = pdf_name
        data["completed_pages"] = []
        data["failed_pages"] = []

        self.save(data)

    # -------------------------------------------------

    def complete_page(self, page):

        data = self.load()

        if page not in data["completed_pages"]:

            data["completed_pages"].append(page)

        self.save(data)

    # -------------------------------------------------

    def failed_page(self, page):

        data = self.load()

        if page not in data["failed_pages"]:

            data["failed_pages"].append(page)

        self.save(data)

    # -------------------------------------------------

    def is_completed(self, page):

        data = self.load()

        return page in data["completed_pages"]


progress = ProgressManager()