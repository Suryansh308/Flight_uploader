from playwright.sync_api import sync_playwright


class Browser:

    def __init__(self):
        self.playwright = sync_playwright().start()

        self.browser = self.playwright.chromium.launch(
            headless=False,
            slow_mo=100
        )

        self.context = self.browser.new_context()

        self.page = self.context.new_page()

    def open(self, url: str):
        self.page.goto(url)

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()