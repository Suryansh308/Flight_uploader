from playwright.sync_api import TimeoutError
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

            except:

                continue

        return visible_rows

    # ---------------------------------------------------------
    # Read Flight Number
    # ---------------------------------------------------------

    def get_flight(self, row):

        cells = row.locator("td")

        text = cells.nth(8).text_content()

        if text:

            return text.strip()

        return ""

    # ---------------------------------------------------------
    # Read Flight Date
    # ---------------------------------------------------------

    def get_date(self, row):

        cells = row.locator("td")

        text = cells.nth(9).text_content()

        if text:

            return text.strip()

        return ""

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

        self.page.wait_for_timeout(500)

    # ---------------------------------------------------------
    # Print Rows (Debug)
    # ---------------------------------------------------------

    def print_rows(self):

        rows = self.get_rows()

        print()

        print("=" * 60)

        print(
            f"Visible Rows : {len(rows)}"
        )

        print("=" * 60)

        for index, row in enumerate(rows, start=1):

            try:

                print(

                    f"{index}.",

                    self.get_flight(row),

                    "|",

                    self.get_date(row)

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

        except:

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

        except:

            return True

    # ---------------------------------------------------------
    # Previous Page
    # ---------------------------------------------------------

    def previous_page(self):

        if self.is_first_page():

            return False

        print("← Previous Page")

        button = self.page.locator(
            PREVIOUS_PAGE
        )

        button.click()

        #
        # Wait for table to stabilize
        #

        self.wait_for_table()

        self.page.wait_for_timeout(1000)

        return True

    # ---------------------------------------------------------
    # Next Page
    # ---------------------------------------------------------

    def next_page(self):

        if self.is_last_page():

            return False

        print("→ Next Page")

        button = self.page.locator(
            NEXT_PAGE
        )

        button.click()

        #
        # Wait for table refresh
        #

        self.wait_for_table()

        self.page.wait_for_timeout(1000)

        return True

    # ---------------------------------------------------------
    # Reset Search
    # ---------------------------------------------------------

        # ---------------------------------------------------------
    # Reset Search
    # ---------------------------------------------------------

    def reset(self):

        print("\nResetting to first page...")

        safety = 20

        while safety > 0:

            try:

                previous = self.page.locator(
                    PREVIOUS_PAGE
                )

                if previous.is_disabled():

                    break

                previous.click()

                #
                # Wait for table refresh
                #

                self.wait_for_table()

                self.page.wait_for_timeout(800)

                safety -= 1

            except Exception:

                break

        print("✅ Reset Complete")
        # ---------------------------------------------------------
    # Search Current Page
    # ---------------------------------------------------------

    def search_current_page(
        self,
        flight_number,
        flight_date
    ):

        rows = self.get_rows()

        print(f"\nVisible Rows : {len(rows)}")

        for index, row in enumerate(rows, start=1):

            try:

                portal_flight = self.get_flight(row)
                portal_date = self.get_date(row)

                print(
                    f"Row {index} | "
                    f"{portal_flight} | "
                    f"{portal_date}"
                )

                #
                # Exact Match
                #
                if (matcher.match(

                        portal_flight,

                        flight_number

                    )

                    and

                    portal_date.strip()

                    ==

                    flight_date.strip()

                ):

                    print("\n✅ Matching Trip Found")

                    self.click_checkbox(row)

                    return True

                #
                # Future OCR Matching Hook
                #
                # elif similarity(
                #     portal_flight,
                #     flight_number
                # ) > 0.90:
                #
                #     self.click_checkbox(row)
                #     return True
                #

            except Exception as e:

                print(
                    f"Row {index} skipped."
                )

                print(e)

        return False

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
        print("Searching Trip")
        print("=" * 60)

        #
        # Always start from Page 1
        #

        self.reset()

        page_number = 1

        #
        # Safety limit
        #

        max_pages = 100

        while page_number <= max_pages:

            print()
            print(
                f"Searching Page {page_number}"
            )

            found = self.search_current_page(
                flight_number,
                flight_date
            )

            if found:

                return True

            #
            # Last Page?
            #

            if self.is_last_page():

                print(
                    "\nReached Last Page."
                )

                return False

            #
            # Next Page
            #

            moved = self.next_page()

            if not moved:

                return False

            page_number += 1

        #
        # Infinite-loop protection
        #

        print(
            "\nPagination safety limit reached."
        )

        return False    