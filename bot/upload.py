from pathlib import Path

from playwright.sync_api import TimeoutError

from bot.selectors import (
    UPLOAD_BUTTON,
    FILE_INPUT,
    SUBMIT_BUTTON,
    OK_BUTTON,
    TABLE,
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

            raise FileNotFoundError(
                pdf_path
            )

        print(
            f"Selecting File : "
            f"{pdf_path.name}"
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
    # Confirm Success
    # ---------------------------------------------------------

    def confirm(self):

        print(
            "Closing Success Dialog..."
        )

        ok = self.page.locator(
            OK_BUTTON
        )

        ok.wait_for(
            state="visible",
            timeout=10000
        )

        ok.click()

        self.page.wait_for_timeout(
            1000
        )

        print(
            "✅ Success Dialog Closed"
        )

    # ---------------------------------------------------------
    # Wait For Upload Modal To Close
    # ---------------------------------------------------------

    def wait_for_upload_modal_closed(self):

        print(
            "Checking upload modal..."
        )

        modal = self.page.locator(
            "#upload_view_file"
        )

        try:

            modal.wait_for(
                state="hidden",
                timeout=15000
            )

        except TimeoutError:

            raise Exception(
                "Upload view modal is still open."
            )

        print(
            "✅ Upload view modal closed."
        )

    # ---------------------------------------------------------
    # Wait For Main Table
    # ---------------------------------------------------------

    def wait_for_table(self):

        print(
            "Waiting for trip table..."
        )

        try:

            table = self.page.locator(
                TABLE
            )

            table.wait_for(
                state="visible",
                timeout=30000
            )

        except TimeoutError:

            raise Exception(
                "Trip table did not become "
                "available after upload."
            )

        self.page.wait_for_timeout(
            1000
        )

        print(
            "✅ Trip table ready."
        )

    # ---------------------------------------------------------
    # Verify Page Is Ready For Navigation
    # ---------------------------------------------------------

    def verify_ready_for_navigation(self):

        modal = self.page.locator(
            "#upload_view_file"
        )

        try:

            if modal.is_visible():

                raise Exception(
                    "Upload view modal is still "
                    "visible; pagination is unsafe."
                )

        except Exception as e:

            if (
                "pagination is unsafe"
                in str(e)
            ):

                raise

        print(
            "✅ Portal ready for navigation."
        )

    # ---------------------------------------------------------
    # Complete Upload
    # ---------------------------------------------------------

    def upload_document(
        self,
        pdf_path
    ):

        self.open_dialog()

        self.choose_file(
            pdf_path
        )

        self.submit()

        self.wait_until_uploaded()

        self.confirm()

        #
        # Critical:
        # Do not return until the upload modal
        # is genuinely gone.
        #

        self.wait_for_upload_modal_closed()

        self.wait_for_table()

        self.verify_ready_for_navigation()

        print(
            "✅ Upload process completely finished."
        )

        return True