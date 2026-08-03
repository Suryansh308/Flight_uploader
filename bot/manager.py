from bot.portal import Portal
from bot.navigation import Navigation
from bot.search import TripFinder
from bot.upload import UploadManager

from pdf.extractor import PDFExtractor
from pdf.parser import PDFParser

from utils.files import get_latest_pdf


class Manager:

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

    # ---------------------------------------------------------
    # Load PDF
    # ---------------------------------------------------------

    def load_pdf(self):

        pdf_path = get_latest_pdf()

        print("\n==========================================")
        print("PDF Selected")
        print("==========================================")
        print(pdf_path.name)

        extractor = PDFExtractor(pdf_path)

        parser = PDFParser()

        return extractor, parser

    # ---------------------------------------------------------
    # Process One Trip
    # ---------------------------------------------------------

    def process_trip(

        self,

        page_index,

        total_pages,

        extractor,

        parser

    ):

        print()

        print("=" * 60)

        print(

            f"[{page_index + 1}/{total_pages}]"

        )

        print("=" * 60)

        #
        # Read PDF Page
        #

        trip = extractor.get_trip(

            page_index,

            parser

        )

        print()

        print(

            f"Flight : {trip.flight_number}"

        )

        print(

            f"Date   : {trip.flight_date}"

        )

        print(

            f"PDF    : {trip.pdf_file.name}"

        )

        #
        # IMPORTANT
        #
        # Every search starts from Page 1
        #

        self.search.reset()

        #
        # Search Trip
        #

        found = self.search.find_trip(

            trip.flight_number,

            trip.flight_date

        )

        if not found:

            print()

            print("❌ Trip Not Found")

            return False

        #
        # Upload
        #

        print()

        print("Uploading...")

        self.upload.upload_document(

            trip.pdf_file

        )
        #
# Give portal time to rebuild the table
#

        self.portal.page.wait_for_timeout(2000)
        print("✅ Upload Completed")

        return True

    # ---------------------------------------------------------
    # Run
    # ---------------------------------------------------------

    def run(self):

        success = 0

        failed = 0

        extractor = None

        try:

            #
            # Login
            #

            self.portal.login()

            #
            # Open My Trips
            #

            self.navigation.go_to_my_trips()

            #
            # PDF
            #

            extractor, parser = self.load_pdf()

            total_pages = extractor.page_count

            print()

            print(

                f"Total Pages : {total_pages}"

            )

            #
            # Process Every PDF Page
            #

            for page in range(total_pages):

                try:

                    completed = self.process_trip(

                        page,

                        total_pages,

                        extractor,

                        parser

                    )

                    if completed:

                        success += 1

                    else:

                        failed += 1

                except Exception as e:

                    failed += 1

                    print()

                    print("❌ ERROR")

                    print(e)

                    #
                    # Continue with next PDF page
                    #

                    continue

            #
            # Summary
            #

            print()

            print("=" * 60)

            print("UPLOAD SUMMARY")

            print("=" * 60)

            print(

                f"Successful : {success}"

            )

            print(

                f"Failed     : {failed}"

            )

            print("=" * 60)

            input(

                "\nPress ENTER to close..."

            )

        finally:

            if extractor:

                extractor.close()

            self.portal.close()