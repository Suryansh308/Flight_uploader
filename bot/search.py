from datetime import datetime

from utils.matcher import matcher

from bot.selectors import (
    TABLE,
    TABLE_ROWS,
    NEXT_PAGE,
    PREVIOUS_PAGE,
)


class TripFinder:

    def __init__(self, page):

        self.page = page

        # Portal is newest -> oldest
        self.current_page = 1

    # ---------------------------------------------------------
    # Wait For Table
    # ---------------------------------------------------------

    def wait_for_table(self):

        self.page.locator(
            TABLE
        ).wait_for(
            state="visible",
            timeout=30000
        )

    # ---------------------------------------------------------
    # Get Visible Rows
    # ---------------------------------------------------------

    def get_rows(self):

        self.wait_for_table()

        rows = self.page.locator(
            TABLE_ROWS
        )

        visible_rows = []

        total = rows.count()

        for i in range(total):

            row = rows.nth(i)

            try:

                if row.is_visible():

                    visible_rows.append(row)

            except Exception:

                continue

        return visible_rows

    # ---------------------------------------------------------
    # Read Flight Number
    # ---------------------------------------------------------

    # ---------------------------------------------------------
# Read Flight Number
# ---------------------------------------------------------

    def get_flight(self, row):

        cells = row.locator("td")

        text = cells.nth(7).text_content()

        if text:

            return text.strip()

        return ""


    # ---------------------------------------------------------
    # Read Flight Date
    # ---------------------------------------------------------

    def get_date(self, row):

        cells = row.locator("td")

        text = cells.nth(8).text_content()

        if text:

            return text.strip()

        return ""    # ---------------------------------------------------------
    # Parse Date
    # ---------------------------------------------------------

    def parse_date(self, value):

        if not value:

            return None

        value = value.strip()

        formats = [
            "%d/%m/%Y",
            "%d-%m-%Y",
            "%d/%m/%y",
            "%d-%m-%y",
        ]

        for fmt in formats:

            try:

                return datetime.strptime(
                    value,
                    fmt
                ).date()

            except ValueError:

                continue

        return None

    # ---------------------------------------------------------
    # Select Row
    # ---------------------------------------------------------

    def click_checkbox(self, row):

        checkbox = row.locator(
            ".cccheck"
        )

        checkbox.wait_for(
            state="visible",
            timeout=10000
        )

        checkbox.click()

        self.page.wait_for_timeout(
            500
        )

    # ---------------------------------------------------------
    # Print Rows
    # ---------------------------------------------------------

    def print_rows(self):

        rows = self.get_rows()

        print()

        print("=" * 60)

        print(
            f"Visible Rows : {len(rows)}"
        )

        print("=" * 60)

        for index, row in enumerate(
            rows,
            start=1
        ):

            try:

                print(
                    f"{index}. "
                    f"{self.get_flight(row)} | "
                    f"{self.get_date(row)}"
                )

            except Exception:

                print(
                    f"{index}. Unable to read"
                )

        print("=" * 60)

    # ---------------------------------------------------------
    # Is First Page
    # ---------------------------------------------------------

    def is_first_page(self):

        try:

            button = self.page.locator(
                PREVIOUS_PAGE
            )

            return button.is_disabled()

        except Exception:

            return True

    # ---------------------------------------------------------
    # Is Last Page
    # ---------------------------------------------------------

    def is_last_page(self):

        try:

            button = self.page.locator(
                NEXT_PAGE
            )

            return button.is_disabled()

        except Exception:

            return True

    # ---------------------------------------------------------
    # Previous Page
    # ---------------------------------------------------------

    def previous_page(self):

        if self.is_first_page():

            return False

        print(
            f"← Page "
            f"{self.current_page - 1}"
        )

        self.page.locator(
            PREVIOUS_PAGE
        ).click()

        self.wait_for_table()

        self.page.wait_for_timeout(
            800
        )

        if self.current_page > 1:

            self.current_page -= 1

        return True

    # ---------------------------------------------------------
    # Next Page
    # ---------------------------------------------------------

    def next_page(self):

        if self.is_last_page():

            return False

        print(
            f"→ Page "
            f"{self.current_page + 1}"
        )

        self.page.locator(
            NEXT_PAGE
        ).click()

        self.wait_for_table()

        self.page.wait_for_timeout(
            800
        )

        self.current_page += 1

        return True

    # ---------------------------------------------------------
    # Reset To First Page
    # ---------------------------------------------------------

    def reset(self):

        if self.current_page == 1:

            return

        print(
            "\nResetting to first page..."
        )

        while self.current_page > 1:

            moved = self.previous_page()

            if not moved:

                break

        self.wait_for_table()

        self.page.wait_for_timeout(
            800
        )

        self.current_page = 1

        print(
            "✅ Reset Complete"
        )

    # ---------------------------------------------------------
    # Search Current Page
    # ---------------------------------------------------------

    def search_current_page(
        self,
        flight_number,
        flight_date
    ):

        rows = self.get_rows()

        print(
            f"\nVisible Rows : "
            f"{len(rows)}"
        )

        target_date = self.parse_date(
            flight_date
        )

        if target_date is None:

            print(
                f"❌ Invalid target date: "
                f"{flight_date}"
            )

            return {
                "found": False,
                "passed_target": False,
                "best_score": 0.0,
                "best_flight": "",
                "best_date": ""
            }

        best_row = None
        best_score = 0.0
        best_flight = ""
        best_date = ""

        page_has_target_date = False
        page_has_older_date = False
        parsed_dates = []

        # -----------------------------------------------------
        # Inspect EVERY row first
        # -----------------------------------------------------

        for index, row in enumerate(
            rows,
            start=1
        ):

            try:

                portal_flight = (
                    self.get_flight(row)
                )

                portal_date = (
                    self.get_date(row)
                )

                print(
                    f"Row {index} | "
                    f"{portal_flight} | "
                    f"{portal_date}"
                )

                row_date = self.parse_date(
                    portal_date
                )

                if row_date is None:

                    print(
                        f"  ⚠️ Unable to parse "
                        f"portal date: "
                        f"{portal_date}"
                    )

                    continue

                parsed_dates.append(
                    row_date
                )

                # -------------------------------------------------
                # Date comparison
                # -------------------------------------------------

                if row_date == target_date:

                    page_has_target_date = True

                elif row_date < target_date:

                    page_has_older_date = True

                    # Older than target:
                    # don't compare flight number.
                    continue

                else:

                    # Newer than target.
                    # Still inspect the page, but it cannot match.
                    continue

                # -------------------------------------------------
                # Exact target date -> compare flight
                # -------------------------------------------------

                score = matcher.similarity(
                    portal_flight,
                    flight_number
                )

                print(
                    f"  Similarity : "
                    f"{portal_flight}"
                    f" <-> "
                    f"{flight_number}"
                    f" = "
                    f"{score:.2f}"
                )

                if score > best_score:

                    best_score = score

                    best_row = row

                    best_flight = (
                        portal_flight
                    )

                    best_date = (
                        portal_date
                    )

            except Exception as e:

                print(
                    f"Row {index} skipped."
                )

                print(e)

        # -----------------------------------------------------
        # Best candidate found
        # -----------------------------------------------------

        if best_row is not None:

            print(
                "\nBest Candidate"
            )

            print(
                f"Portal Flight : "
                f"{best_flight}"
            )

            print(
                f"Portal Date   : "
                f"{best_date}"
            )

            print(
                f"OCR Flight    : "
                f"{flight_number}"
            )

            print(
                f"Target Date   : "
                f"{flight_date}"
            )

            print(
                f"Similarity    : "
                f"{best_score:.2f}"
            )

            # -------------------------------------------------
            # Existing matcher threshold = 0.90
            # -------------------------------------------------

            if best_score >= matcher.threshold:

                print(
                    "\n✅ Matching Trip Found"
                )

                self.click_checkbox(
                    best_row
                )

                return {
                    "found": True,
                    "passed_target": False,
                    "best_score": best_score,
                    "best_flight": best_flight,
                    "best_date": best_date
                }

            print(
                "\n⚠️ Candidate found, "
                "but similarity is below "
                f"{matcher.threshold:.2f}"
            )

        # -----------------------------------------------------
        # Determine whether target date has been passed
        # -----------------------------------------------------

        passed_target = False

        if parsed_dates:

            oldest_date = min(
                parsed_dates
            )

            if oldest_date < target_date:

                passed_target = True

        return {
            "found": False,
            "passed_target": passed_target,
            "best_score": best_score,
            "best_flight": best_flight,
            "best_date": best_date
        }

    # ---------------------------------------------------------
    # Find Trip
    # ---------------------------------------------------------

    def find_trip(
        self,
        flight_number,
        flight_date
    ):

        print()

        print("=" * 60)

        print(
            "Searching Trip"
        )

        print("=" * 60)

        print(
            f"Looking for: "
            f"{flight_number} | "
            f"{flight_date}"
        )

        target_date = self.parse_date(
            flight_date
        )

        if target_date is None:

            print(
                "\n❌ Invalid flight date."
            )

            print(
                f"Date: {flight_date}"
            )

            return False

        # -----------------------------------------------------
        # Always start a new trip from Page 1
        # -----------------------------------------------------

        self.reset()

        while True:

            print()

            print(
                f"Searching Page "
                f"{self.current_page}"
            )

            result = (
                self.search_current_page(
                    flight_number,
                    flight_date
                )
            )

            # -------------------------------------------------
            # Found
            # -------------------------------------------------

            if result["found"]:

                return True

            # -------------------------------------------------
            # Date boundary reached
            # -------------------------------------------------

            if result["passed_target"]:

                print(
                    "\n🛑 Date boundary reached."
                )

                print(
                    f"Target Date : "
                    f"{flight_date}"
                )

                print(
                    "Portal is now older "
                    "than the target date."
                )

                print(
                    "Stopping search."
                )

                return False

            # -------------------------------------------------
            # Last portal page
            # -------------------------------------------------

            if self.is_last_page():

                print(
                    "\n❌ Reached last portal page."
                )

                print(
                    f"Flight : "
                    f"{flight_number}"
                )

                print(
                    f"Date   : "
                    f"{flight_date}"
                )

                return False

            # -------------------------------------------------
            # Move forward
            # -------------------------------------------------

            moved = self.next_page()

            if not moved:

                print(
                    "\n❌ Unable to move "
                    "to next page."
                )

                return False