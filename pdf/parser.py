import re

from models.trip import TripDocument


class PDFParser:

    DATE_PATTERN = re.compile(r"\d{2}/\d{2}/\d{4}")
    FLIGHT_PATTERN = re.compile(r"^[A-Z]{2,}\d{2,}$")

    def parse(self, words, page_number):

        flight_number = None
        flight_date = None

        # -----------------------------
        # Locate the "FLT" label
        # -----------------------------

        flt_word = None

        for word in words:

            if word[4].upper() == "FLT":
                flt_word = word
                break

        if flt_word is None:
            raise Exception("FLT label not found")

        flt_x = flt_word[0]
        flt_y = flt_word[1]

        candidates = []

        # -----------------------------
        # Find words on the same line
        # and to the right of FLT
        # -----------------------------

        for word in words:

            x = word[0]
            y = word[1]
            text = word[4]

            if abs(y - flt_y) < 5 and x > flt_x:

                if self.FLIGHT_PATTERN.match(text):
                    candidates.append(word)

        if not candidates:
            raise Exception("Flight Number not found")

        # nearest candidate
        flight_number = sorted(candidates, key=lambda w: w[0])[0][4]

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