from pathlib import Path
from csv import writer
from datetime import datetime


class Report:

    def __init__(self):

        self.folder = Path("logs")

        self.folder.mkdir(exist_ok=True)

        self.file = self.folder / "upload_report.csv"

        if not self.file.exists():

            with open(
                self.file,
                "w",
                newline="",
                encoding="utf-8"
            ) as f:

                csv = writer(f)

                csv.writerow([
                    "Timestamp",
                    "Page",
                    "Flight",
                    "Date",
                    "Status",
                    "Remarks"
                ])

    # -------------------------------------------------

    def add(

        self,

        page,

        flight,

        date,

        status,

        remarks=""

    ):

        with open(

            self.file,

            "a",

            newline="",

            encoding="utf-8"

        ) as f:

            csv = writer(f)

            csv.writerow([

                datetime.now().strftime(

                    "%d-%m-%Y %H:%M:%S"

                ),

                page,

                flight,

                date,

                status,

                remarks

            ])


report = Report()