from bot.selectors import (
    SIDEBAR,
    TRIPS,
    MY_TRIPS,
)


class Navigation:

    def __init__(self, page):

        self.page = page

    # -----------------------------------------------------
    # Sidebar
    # -----------------------------------------------------

    def open_sidebar(self):

        print("\nOpening Sidebar...")

        self.page.locator(
            SIDEBAR
        ).click()

        self.page.wait_for_timeout(500)

        print("✅ Sidebar Opened")

    # -----------------------------------------------------
    # Trips
    # -----------------------------------------------------

    def open_trips(self):

        print("Opening Trips...")

        self.page.locator(
            TRIPS
        ).click()

        self.page.wait_for_timeout(500)

        print("✅ Trips Opened")

    # -----------------------------------------------------
    # My Trips
    # -----------------------------------------------------

    def open_my_trips(self):

        print("Opening My Trips...")

        self.page.locator(
            MY_TRIPS
        ).click()

        self.page.wait_for_load_state(
            "networkidle"
        )

        print("✅ My Trips Opened")

    # -----------------------------------------------------
    # Complete Navigation
    # -----------------------------------------------------

    def go_to_my_trips(self):

        self.open_sidebar()

        self.open_trips()

        self.open_my_trips()