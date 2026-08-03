from playwright.sync_api import sync_playwright

from config import (
    PORTAL_URL,
    PORTAL_USERNAME,
    PORTAL_PASSWORD,
)

from bot.selectors import (
    LOGIN_USERNAME,
    LOGIN_PASSWORD,
    LOGIN_BUTTON,
    SIDEBAR,
)


class Portal:

    def __init__(self):

        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=250
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

    # ---------------------------------------------------------
    # LOGIN
    # ---------------------------------------------------------

    def login(self):

        print("\n========================================")
        print("Opening Portal")
        print("========================================")

        self.page.goto(
            PORTAL_URL,
            wait_until="domcontentloaded"
        )

        print("Waiting for Login Page...")

        self.page.locator(
            LOGIN_USERNAME
        ).wait_for(
            state="visible",
            timeout=60000
        )

        print("Entering Username...")

        self.page.locator(
            LOGIN_USERNAME
        ).fill(PORTAL_USERNAME)

        print("Entering Password...")

        self.page.locator(
            LOGIN_PASSWORD
        ).fill(PORTAL_PASSWORD)

        print("Signing In...")

        self.page.locator(
            LOGIN_BUTTON
        ).click()

        print("Waiting for Dashboard...")

        self.page.locator(
            SIDEBAR
        ).wait_for(
            state="visible",
            timeout=60000
        )

        print("✅ Login Successful")

    # ---------------------------------------------------------
    # WAIT
    # ---------------------------------------------------------

    def wait(self, seconds=1):

        self.page.wait_for_timeout(
            seconds * 1000
        )

    # ---------------------------------------------------------
    # CLOSE
    # ---------------------------------------------------------

    def close(self):

        print("\nClosing Browser...")

        try:
            self.context.close()
        except:
            pass

        try:
            self.browser.close()
        except:
            pass

        try:
            self.playwright.stop()
        except:
            pass

        print("✅ Browser Closed")