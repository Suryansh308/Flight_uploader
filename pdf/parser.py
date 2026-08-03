import re

from models.trip import TripDocument


class PDFParser:

    DATE_PATTERN = re.compile(r"\d{2}/\d{2}/\d{4}")
    FLIGHT_PATTERN = re.compile(r"^[A-Z]{2,}\d+[A-Z]*$")

    def parse(self, words, page_number):

        flight_number = None
        flight_date = None

        print("\n========== PARSER TOKENS ==========")

        for word in words[:80]:
            print(repr(word[4]))

        print("==================================\n")


        # -----------------------------
# Find Flight Number
# -----------------------------

        IGNORE = {

            "FLT",
            "NO",
            "DATE",
            "HUB",
            "CREW",
            "ORIGIN",
            "DESTINATION",
            "LOCATION",
            "PRINT",
            "TRIPSHEET",

        }

        for word in words:

            text = word[4].upper().strip()

            if text in IGNORE:

                continue

            if self.DATE_PATTERN.fullmatch(text):

                continue

            if self.FLIGHT_PATTERN.fullmatch(text):

                flight_number = text

                break

        if flight_number is None:

            raise Exception(
                "Flight Number not found"
            )

        

        # -----------------------------
        # Find first date
        # -----------------------------

        for word in words:

            if self.DATE_PATTERN.fullmatch(word[4]):
                flight_date = word[4]
                break

        if not flight_date:
            raise Exception("Flight Date not found")

        return TripDocument(
            flight_number=flight_number,
            flight_date=flight_date,
            page_number=page_number
        )