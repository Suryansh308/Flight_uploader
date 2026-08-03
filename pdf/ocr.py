import fitz
import easyocr
import numpy as np
from PIL import Image
from pdf.regions import (
    FLIGHT_BOX,
    DATE_BOX,
)

class OCRExtractor:

    def __init__(self):

        #
        # Initialize EasyOCR once
        #

        self.reader = easyocr.Reader(
            ["en"],
            gpu=True
        )

    # ---------------------------------------------------------
    # Extract Words From Page
    # ---------------------------------------------------------

    def extract(self, page):

    #
    # Render full page
    #

        pix = page.get_pixmap(dpi=300)

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        #
        # Page dimensions
        #

        width, height = image.size

        #
        # Header region
        # (percentage based)
        #

        left = int(width * 0.210)
        top = int(height * 0.178)
        right = int(width * 0.600)
        bottom = int(height * 0.268)

        #
        # Crop only header
        #

        image = image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )

        #
        # Convert to grayscale
        #

        image = image.convert("L")

        #
        # Increase contrast
        #

        from PIL import ImageOps

        image = ImageOps.autocontrast(image)

        #
        # Convert to numpy
        #

        image = np.array(image)

        #
        # OCR
        #

        results = self.reader.readtext(
            image,
            detail=1
        )

        words = []

        for item in results:

            bbox, text, confidence = item

            tokens = text.split()

            x0 = bbox[0][0]
            y0 = bbox[0][1]
            x1 = bbox[2][0]
            y1 = bbox[2][1]

            current_x = x0

            width = (x1 - x0) / max(
                len(tokens),
                1
            )

            for token in tokens:

                words.append(
                    (
                        current_x,
                        y0,
                        current_x + width,
                        y1,
                        token,
                        0,
                        0,
                        0
                    )
                )

                current_x += width

        return words

    def extract_region(
    self,
    page,
    region
):

        pix = page.get_pixmap(dpi=400)

        image = Image.frombytes(
            "RGB",
            [pix.width, pix.height],
            pix.samples
        )

        width, height = image.size

        left = int(width * region[0])
        top = int(height * region[1])
        right = int(width * region[2])
        bottom = int(height * region[3])

        image = image.crop(
            (
                left,
                top,
                right,
                bottom
            )
        )

        #
        # enlarge before OCR
        #

        image = image.resize(

            (
                image.width * 4,
                image.height * 4
            )

        )

        from PIL import ImageOps

        image = image.convert("L")

        image = ImageOps.autocontrast(image)

        image = np.array(image)

        results = self.reader.readtext(
            image,
            detail=0
        )

        return results

#
# Singleton
#

ocr = OCRExtractor()