import json
from pathlib import Path

from bot.portal import Portal
from bot.navigation import Navigation
from bot.search import TripFinder
from bot.upload import UploadManager


class Manager:

    # ==========================================================
    # CURRENT PDF RUN
    # ==========================================================

    PDF_NAME = "Adobe Scan 09 Aug 2026.pdf"

    BASE_DIR = Path(__file__).resolve().parent.parent

    RUN_DIR = (
        BASE_DIR
        / "results"
        / "runs"
        / Path(PDF_NAME).stem
    )

    EXTRACTION_FILE = (
        RUN_DIR
        / "extraction_results.json"
    )

    UPLOAD_RESULTS_FILE = (
        RUN_DIR
        / "upload_results.json"
    )

    # ==========================================================
    # INIT
    # ==========================================================

    def __init__(self):

        self.portal = Portal()

        self.navigation = Navigation(
            self.portal.page
        )

        self.search = TripFinder(
            self.portal.page
        )

        self.upload = UploadManager(
            self.portal.page
        )

    # ==========================================================
    # LOAD EXISTING OCR JSON
    # ==========================================================

    def load_extraction_results(self):

        print()
        print("=" * 60)
        print("LOADING EXISTING OCR RESULTS")
        print("=" * 60)

        print(
            f"File : {self.EXTRACTION_FILE}"
        )

        if not self.EXTRACTION_FILE.exists():

            raise FileNotFoundError(
                "\nExtraction JSON not found:\n"
                f"{self.EXTRACTION_FILE.resolve()}\n\n"
                "OCR has NOT been run by Manager."
            )

        with open(
            self.EXTRACTION_FILE,
            "r",
            encoding="utf-8"
        ) as file:

            data = json.load(file)

        successful = data.get(
            "successful",
            {}
        )

        failed = data.get(
            "failed",
            {}
        )

        print(
            f"\nSuccessful OCR : "
            f"{len(successful)}"
        )

        print(
            f"Failed OCR     : "
            f"{len(failed)}"
        )

        print(
            "✅ Existing OCR JSON loaded."
        )

        return data

    # ==========================================================
    # LOAD EXISTING UPLOAD RESULTS
    # ==========================================================

    def load_upload_results(self):

        if not self.UPLOAD_RESULTS_FILE.exists():

            print(
                "\nNo previous upload report "
                "for this run."
            )

            return {
                "uploaded": {},
                "not_found": {},
                "upload_failed": {},
                "manual_review": {}
            }

        try:

            with open(
                self.UPLOAD_RESULTS_FILE,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

        except Exception as e:

            print(
                "\n⚠️ Could not read existing "
                "upload report."
            )

            print(e)

            return {
                "uploaded": {},
                "not_found": {},
                "upload_failed": {},
                "manual_review": {}
            }

        data.setdefault(
            "uploaded",
            {}
        )

        data.setdefault(
            "not_found",
            {}
        )

        data.setdefault(
            "upload_failed",
            {}
        )

        data.setdefault(
            "manual_review",
            {}
        )

        return data

    # ==========================================================
    # SAVE UPLOAD RESULTS
    # ==========================================================

    def save_upload_results(
        self,
        results
    ):

        self.UPLOAD_RESULTS_FILE.parent.mkdir(
            parents=True,
            exist_ok=True
        )

        temp_file = (
            self.UPLOAD_RESULTS_FILE.parent
            / "upload_results.tmp"
        )

        with open(
            temp_file,
            "w",
            encoding="utf-8"
        ) as file:

            json.dump(
                results,
                file,
                indent=4,
                ensure_ascii=False
            )

        temp_file.replace(
            self.UPLOAD_RESULTS_FILE
        )

    # ==========================================================
    # REMOVE OLD FAILURE STATUS
    # ==========================================================

    def clear_failure_status(
        self,
        results,
        page_number
    ):

        page = str(page_number)

        results[
            "not_found"
        ].pop(
            page,
            None
        )

        results[
            "upload_failed"
        ].pop(
            page,
            None
        )

        results[
            "manual_review"
        ].pop(
            page,
            None
        )

    # ==========================================================
    # MARK UPLOADED
    # ==========================================================

    def mark_uploaded(
        self,
        results,
        page_number,
        trip,
        pdf_path
    ):

        page = str(page_number)

        self.clear_failure_status(
            results,
            page_number
        )

        results[
            "uploaded"
        ][page] = {

            "page":
                page_number,

            "flight_number":
                trip.get(
                    "flight_number",
                    ""
                ),

            "flight_date":
                trip.get(
                    "flight_date",
                    ""
                ),

            "pdf":
                str(pdf_path),

            "status":
                "uploaded"
        }

        self.save_upload_results(
            results
        )

    # ==========================================================
    # RESET PORTAL TO PAGE 1
    # ==========================================================

    def reset_portal(self):

        print()
        print("=" * 60)
        print("RESETTING PORTAL TO PAGE 1")
        print("=" * 60)

        self.search.reset()

        print(
            "✅ Portal is at Page 1."
        )

    # ==========================================================
    # VALIDATE OCR TRIP
    # ==========================================================

    def validate_trip(
        self,
        page_number,
        trip,
        results
    ):

        flight_number = str(
            trip.get(
                "flight_number",
                ""
            )
        ).strip()

        flight_date = str(
            trip.get(
                "flight_date",
                ""
            )
        ).strip()

        # ------------------------------------------------------
        # Missing flight
        # ------------------------------------------------------

        if not flight_number:

            results[
                "manual_review"
            ][str(page_number)] = {

                "page":
                    page_number,

                "flight_number":
                    "",

                "flight_date":
                    flight_date,

                "status":
                    "manual_review",

                "reason":
                    "Flight number missing from OCR."
            }

            self.save_upload_results(
                results
            )

            print(
                "\n⚠️ Flight number missing."
            )

            return False

        # ------------------------------------------------------
        # Missing date
        # ------------------------------------------------------

        if not flight_date:

            results[
                "manual_review"
            ][str(page_number)] = {

                "page":
                    page_number,

                "flight_number":
                    flight_number,

                "flight_date":
                    "",

                "status":
                    "manual_review",

                "reason":
                    "Flight date missing from OCR."
            }

            self.save_upload_results(
                results
            )

            print(
                "\n⚠️ Flight date missing."
            )

            return False

        return True

    # ==========================================================
    # PROCESS ONE TRIP
    # ==========================================================

    def process_trip(
        self,
        page_number,
        trip,
        results
    ):

        flight_number = str(
            trip.get(
                "flight_number",
                ""
            )
        ).strip()

        flight_date = str(
            trip.get(
                "flight_date",
                ""
            )
        ).strip()

        print()
        print("=" * 60)

        print(
            f"PDF PAGE {page_number}"
        )

        print("=" * 60)

        print(
            f"Flight : {flight_number}"
        )

        print(
            f"Date   : {flight_date}"
        )

        # ------------------------------------------------------
        # Validate
        # ------------------------------------------------------

        if not self.validate_trip(
            page_number,
            trip,
            results
        ):

            return False

        # ------------------------------------------------------
        # PDF PATH FROM JSON
        # ------------------------------------------------------

        pdf_value = trip.get(
            "pdf"
        )

        if not pdf_value:

            results[
                "manual_review"
            ][str(page_number)] = {

                "page":
                    page_number,

                "flight_number":
                    flight_number,

                "flight_date":
                    flight_date,

                "status":
                    "manual_review",

                "reason":
                    "PDF path missing from extraction JSON."
            }

            self.save_upload_results(
                results
            )

            print(
                "\n❌ PDF path missing from JSON."
            )

            return False

        pdf_path = Path(
            pdf_value
        )

        if not pdf_path.exists():

            results[
                "manual_review"
            ][str(page_number)] = {

                "page":
                    page_number,

                "flight_number":
                    flight_number,

                "flight_date":
                    flight_date,

                "pdf":
                    str(pdf_path),

                "status":
                    "manual_review",

                "reason":
                    "PDF file does not exist."
            }

            self.save_upload_results(
                results
            )

            print(
                "\n❌ PDF file not found:"
            )

            print(
                pdf_path
            )

            return False

        print(
            f"PDF    : {pdf_path.name}"
        )

        # ------------------------------------------------------
        # SEARCH PORTAL
        # ------------------------------------------------------

        print(
            "\nSearching portal..."
        )

        try:

            found = self.search.find_trip(
                flight_number=flight_number,
                flight_date=flight_date
            )

        except Exception as e:

            results[
                "manual_review"
            ][str(page_number)] = {

                "page":
                    page_number,

                "flight_number":
                    flight_number,

                "flight_date":
                    flight_date,

                "pdf":
                    str(pdf_path),

                "status":
                    "manual_review",

                "reason":
                    str(e)
            }

            self.save_upload_results(
                results
            )

            print(
                "\n❌ Portal search error."
            )

            print(e)

            return False

        # ------------------------------------------------------
        # NOT FOUND
        # ------------------------------------------------------

        if not found:

            results[
                "not_found"
            ][str(page_number)] = {

                "page":
                    page_number,

                "flight_number":
                    flight_number,

                "flight_date":
                    flight_date,

                "pdf":
                    str(pdf_path),

                "status":
                    "not_found"
            }

            self.save_upload_results(
                results
            )

            print(
                "\n❌ Portal trip not found."
            )

            return False

        print(
            "\n✅ Portal trip matched."
        )

        # ------------------------------------------------------
        # UPLOAD
        # ------------------------------------------------------

        print(
            "\nUploading PDF..."
        )

        try:

            self.upload.upload_document(
                pdf_path
            )

        except Exception as e:

            results[
                "upload_failed"
            ][str(page_number)] = {

                "page":
                    page_number,

                "flight_number":
                    flight_number,

                "flight_date":
                    flight_date,

                "pdf":
                    str(pdf_path),

                "status":
                    "upload_failed",

                "reason":
                    str(e)
            }

            self.save_upload_results(
                results
            )

            print(
                "\n❌ Upload failed."
            )

            print(e)

            return False

        # ------------------------------------------------------
        # SUCCESS
        # ------------------------------------------------------

        self.mark_uploaded(
            results,
            page_number,
            trip,
            pdf_path
        )

        print(
            "\n✅ Upload completed."
        )

        return True

    # ==========================================================
    # UPLOAD FROM SAVED JSON
    # ==========================================================

    def upload_from_json(self):

        # ------------------------------------------------------
        # IMPORTANT:
        # This function NEVER creates PDFExtractor.
        # This function NEVER calls PaddleOCR.
        # ------------------------------------------------------

        extraction = (
            self.load_extraction_results()
        )

        successful = extraction.get(
            "successful",
            {}
        )

        failed = extraction.get(
            "failed",
            {}
        )

        results = (
            self.load_upload_results()
        )

        # ------------------------------------------------------
        # OCR SUMMARY
        # ------------------------------------------------------

        print()
        print("=" * 60)
        print("SAVED OCR SUMMARY")
        print("=" * 60)

        print(
            f"Successful : "
            f"{len(successful)}"
        )

        print(
            f"Failed     : "
            f"{len(failed)}"
        )

        print("=" * 60)

        # ------------------------------------------------------
        # OCR failures are NOT uploaded
        # ------------------------------------------------------

        if failed:

            print(
                "\n⚠️ OCR Failed Pages"
            )

            for page, data in sorted(
                failed.items(),
                key=lambda item: int(item[0])
            ):

                print(
                    f"Page {page} | "
                    f"{data.get('reason', '')}"
                )

        # ------------------------------------------------------
        # START PORTAL FROM PAGE 1
        # ------------------------------------------------------

        self.reset_portal()

        # ------------------------------------------------------
        # NEWEST PDF PAGE → OLDEST PDF PAGE
        #
        # PDF was extracted oldest → newest.
        # Portal is newest → oldest.
        # ------------------------------------------------------

        ordered = sorted(
            successful.items(),
            key=lambda item: int(item[0]),
            reverse=True
        )

        total = len(
            ordered
        )

        print()
        print(
            f"Trips to process : {total}"
        )

        # ------------------------------------------------------
        # PROCESS
        # ------------------------------------------------------

        for index, (
            page,
            trip
        ) in enumerate(
            ordered,
            start=1
        ):

            page_number = int(
                page
            )

            # --------------------------------------------------
            # ALREADY UPLOADED
            # --------------------------------------------------

            if (
                str(page_number)
                in results["uploaded"]
            ):

                print()
                print(
                    f"⏭️ Page {page_number} "
                    f"already uploaded."
                )

                continue

            print()
            print("=" * 60)

            print(
                f"[{index}/{total}]"
            )

            print(
                f"PDF PAGE {page_number}"
            )

            print("=" * 60)

            self.process_trip(
                page_number,
                trip,
                results
            )

        # ------------------------------------------------------
        # FINAL REPORT
        # ------------------------------------------------------

        print()
        print("=" * 60)
        print("UPLOAD RUN COMPLETE")
        print("=" * 60)

        print(
            f"Uploaded      : "
            f"{len(results['uploaded'])}"
        )

        print(
            f"Not Found     : "
            f"{len(results['not_found'])}"
        )

        print(
            f"Upload Failed : "
            f"{len(results['upload_failed'])}"
        )

        print(
            f"Manual Review : "
            f"{len(results['manual_review'])}"
        )

        print("=" * 60)

        print(
            "\n💾 Upload results:"
        )

        print(
            self.UPLOAD_RESULTS_FILE.resolve()
        )

    # ==========================================================
    # RUN
    # ==========================================================

    def run(self):

        try:

            print()
            print("=" * 60)
            print("STARTING UPLOAD RUN")
            print("=" * 60)

            print(
                "\nOCR: DISABLED FOR THIS RUN"
            )

            print(
                "Using existing extraction JSON."
            )

            print(
                f"JSON: "
                f"{self.EXTRACTION_FILE.resolve()}"
            )

            # --------------------------------------------------
            # LOGIN
            # --------------------------------------------------

            self.portal.login()

            print(
                "\n✅ Login complete."
            )

            # --------------------------------------------------
            # NAVIGATE
            # --------------------------------------------------

            self.navigation.go_to_my_trips()

            print(
                "\n✅ My Trips opened."
            )

            # --------------------------------------------------
            # UPLOAD FROM SAVED JSON
            # --------------------------------------------------

            self.upload_from_json()

            print()
            print("=" * 60)
            print("ALL DONE")
            print("=" * 60)

            input(
                "\nPress ENTER to close..."
            )

        finally:

            self.portal.close()