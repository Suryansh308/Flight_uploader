import re

from models.trip import TripDocument


class PDFParser:

    DATE_PATTERN = re.compile(
        r"\d{2}/\d{2}/\d{4}"
    )

    FLIGHT_PATTERN = re.compile(
        r"^[A-Z]{2,}\d+[A-Z]*$"
    )

    # ---------------------------------------------------------
    # Parse Page
    # ---------------------------------------------------------

    def parse(
        self,
        words,
        page_number
    ):

        flight_number = None
        flight_date = None

        # -----------------------------------------------------
        # Debug: Show OCR / PDF Tokens
        # -----------------------------------------------------

        print(
            "\n========== PARSER TOKENS =========="
        )

        for word in words:

            try:

                print(
                    repr(word[4])
                )

            except Exception:

                continue

        print(
            "=================================="
        )

        # -----------------------------------------------------
        # Ignore Common Non-Flight Tokens
        # -----------------------------------------------------

        IGNORE = {

            "FLT",
            "FLTNO",
            "FLT NO",
            "NO",
            "DATE",
            "HUB",
            "CREW",
            "ORIGIN",
            "ORIGIN:",
            "DESTINATION",
            "DESTINATION:",
            "LOCATION",
            "PRINT",
            "TRIPSHEET",
            "TRIP SHEET",
            "TRIP",
            "SHEET",
        }

        # -----------------------------------------------------
        # Find Flight Number
        # -----------------------------------------------------

        for word in words:

            try:

                text = (
                    word[4]
                    .upper()
                    .strip()
                )

            except Exception:

                continue

            #
            # Ignore known labels
            #

            if text in IGNORE:

                continue

            #
            # Ignore dates
            #

            if self.DATE_PATTERN.fullmatch(
                text
            ):

                continue

            #
            # Flight number pattern
            #

            if self.FLIGHT_PATTERN.fullmatch(
                text
            ):

                flight_number = text

                break

        # -----------------------------------------------------
        # Flight Number Validation
        # -----------------------------------------------------

        if flight_number is None:

            raise Exception(
                "Flight Number not found"
            )

        # -----------------------------------------------------
        # Find Flight Date
        # -----------------------------------------------------

        for word in words:

            try:

                text = (
                    word[4]
                    .strip()
                )

            except Exception:

                continue

            if self.DATE_PATTERN.fullmatch(
                text
            ):

                flight_date = text

                break

        # -----------------------------------------------------
        # Flight Date Validation
        # -----------------------------------------------------

        if not flight_date:

            raise Exception(
                "Flight Date not found"
            )

        # -----------------------------------------------------
        # Successful Parse
        # -----------------------------------------------------

        print(
            f"✅ {flight_number} | "
            f"{flight_date}"
        )

        return TripDocument(
            flight_number=flight_number,
            flight_date=flight_date,
            page_number=page_number
        )