from pathlib import Path

from playwright.sync_api import TimeoutError

from bot.selectors import (
    UPLOAD_BUTTON,
    FILE_INPUT,
    SUBMIT_BUTTON,
    OK_BUTTON,
)


class UploadManager:

    def __init__(self, page):

        self.page = page

    # ---------------------------------------------------------
    # Open Upload Dialog
    # ---------------------------------------------------------

    def open_dialog(self):

        print("\nOpening Upload Dialog...")

        button = self.page.locator(
            UPLOAD_BUTTON
        )

        button.wait_for(
            state="visible",
            timeout=30000
        )

        button.click()

        self.page.wait_for_timeout(1000)

        print("✅ Upload Dialog Opened")

    # ---------------------------------------------------------
    # Select PDF
    # ---------------------------------------------------------

    def choose_file(self, pdf_path):

        pdf_path = Path(pdf_path)

        if not pdf_path.exists():

            raise FileNotFoundError(pdf_path)

        print(
            f"Selecting File : {pdf_path.name}"
        )

        self.page.locator(
            FILE_INPUT
        ).set_input_files(
            str(pdf_path)
        )

        self.page.wait_for_timeout(1500)

        print("✅ File Selected")

    # ---------------------------------------------------------
    # Submit Upload
    # ---------------------------------------------------------

    def submit(self):

        print("Submitting...")

        button = self.page.locator(
            SUBMIT_BUTTON
        )

        button.wait_for(
            state="visible",
            timeout=30000
        )

        button.click()

    # ---------------------------------------------------------
    # Wait Until Upload Finishes
    # ---------------------------------------------------------

    def wait_until_uploaded(self):

        print("Waiting for upload...")

        try:

            ok = self.page.locator(
                OK_BUTTON
            )

            ok.wait_for(
                state="visible",
                timeout=120000
            )

            print("✅ Upload Finished")

        except TimeoutError:

            raise Exception(
                "Upload did not finish."
            )

    # ---------------------------------------------------------
    # Confirm
    # ---------------------------------------------------------

    def confirm(self):

        print("Closing Success Dialog...")

        self.page.locator(
            OK_BUTTON
        ).click()

        self.page.wait_for_timeout(1000)

        print("✅ Success Dialog Closed")

    # ---------------------------------------------------------
    # Complete Upload
    # ---------------------------------------------------------

    def upload_document(self, pdf_path):

        self.open_dialog()

        self.choose_file(
            pdf_path
        )

        self.submit()

        self.wait_until_uploaded()

        self.confirm()

        return True