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

    # ----------------------------------------------------------
    # Load PDF
    # ----------------------------------------------------------

    def load_pdf(self):

        pdf_path = get_latest_pdf()

        print("\n==========================================")
        print("PDF Selected")
        print("==========================================")
        print(pdf_path.name)

        extractor = PDFExtractor(pdf_path)

        parser = PDFParser()

        return extractor, parser

    # ----------------------------------------------------------
    # Extract All Trips
    # ----------------------------------------------------------

    def extract_all_trips(
        self,
        extractor,
        parser
    ):

        trips = []

        print("\n==========================================")
        print("Reading PDF")
        print("==========================================")

        for page in range(extractor.page_count):

            print(f"\nReading Page {page + 1}...")

            try:

                trip = extractor.get_trip(
                    page,
                    parser
                )

                print(
                    f"✅ {trip.flight_number} | {trip.flight_date}"
                )

                trips.append(trip)

            except Exception as e:

                print(
                    f"❌ Failed to parse Page {page + 1}"
                )

                print(e)

                raise

        #
        # Portal is newest → oldest
        # PDF is oldest → newest
        #

        trips.reverse()

        print(f"\nTrips Found : {len(trips)}")

        print("\nDetected Trips")

        print("------------------------------------------")

        for i, trip in enumerate(trips, start=1):

            print(
                f"{i}. "
                f"{trip.flight_number} | "
                f"{trip.flight_date}"
            )

        print("------------------------------------------")

        return trips

    # ----------------------------------------------------------
    # Upload One Trip
    # ----------------------------------------------------------

    def process_trip(
        self,
        index,
        total,
        trip
    ):

        print()

        print("=" * 60)

        print(f"[{index}/{total}]")

        print("=" * 60)

        print()

        print(f"Flight : {trip.flight_number}")

        print(f"Date   : {trip.flight_date}")

        print(f"PDF    : {trip.pdf_file.name}")

        found = self.search.find_trip(

            flight_number=trip.flight_number,

            flight_date=trip.flight_date

        )

        if not found:

            print("\n❌ Trip Not Found")

            return False

        print("\nUploading...")

        self.upload.upload_document(
            trip.pdf_file
        )

        #
        # Allow portal to refresh
        #

        self.portal.page.wait_for_timeout(
            2000
        )

        print("✅ Upload Completed")

        return True

    # ----------------------------------------------------------
    # Run
    # ----------------------------------------------------------

    def run(self):

        try:

            self.portal.login()

            self.navigation.go_to_my_trips()

            extractor, parser = self.load_pdf()

            trips = self.extract_all_trips(
                extractor,
                parser
            )

            success = 0

            failed = 0

            for index, trip in enumerate(

                trips,

                start=1

            ):

                try:

                    completed = self.process_trip(

                        index,

                        len(trips),

                        trip

                    )

                    if completed:

                        success += 1

                    else:

                        failed += 1

                except Exception as e:

                    failed += 1

                    print("\n❌ ERROR")

                    print(e)

            print("\n==========================================")

            print("UPLOAD SUMMARY")

            print("==========================================")

            print(f"Successful : {success}")

            print(f"Failed     : {failed}")

            print("==========================================")

            input("\nPress ENTER to close...")

        finally:

            self.portal.close()