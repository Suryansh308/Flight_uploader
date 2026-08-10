import numpy as np
from PIL import Image, ImageOps
from paddleocr import PaddleOCR


class OCRExtractor:

    def __init__(self):

        print("\nInitializing PaddleOCR...")

        self.reader = PaddleOCR(
            lang="en",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

        print("✅ PaddleOCR Ready")

    # ---------------------------------------------------------
    # Render + Crop Region
    # ---------------------------------------------------------

    def _prepare_region(
        self,
        page,
        region,
        dpi=600
    ):

        pix = page.get_pixmap(
            dpi=dpi,
            alpha=False
        )

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

        image = ImageOps.autocontrast(
            image
        )

        return np.array(image)

    # ---------------------------------------------------------
    # OCR Region
    # ---------------------------------------------------------

    def extract_region(
        self,
        page,
        region
    ):

        image = self._prepare_region(
            page,
            region,
            dpi=600
        )

        result = self.reader.predict(
            image
        )

        texts = []

        for page_result in result:

            try:

                data = page_result

                if "rec_texts" in data:

                    detected = data["rec_texts"]

                elif "res" in data:

                    detected = data["res"]["rec_texts"]

                else:

                    detected = []

            except Exception:

                detected = []

            for text in detected:

                if text:

                    texts.append(
                        text.strip()
                    )

        return texts

    # ---------------------------------------------------------
    # Extract Full Header
    # ---------------------------------------------------------

    def extract(self, page):

        #
        # Same tuned header region
        #

        region = (
            0.210,
            0.166,
            0.600,
            0.256,
        )

        texts = self.extract_region(
            page,
            region
        )

        words = []

        for text in texts:

            words.append(
                (
                    0,
                    0,
                    0,
                    0,
                    text,
                    0,
                    0,
                    0
                )
            )

        print(
            f"✅ PaddleOCR extracted "
            f"{len(words)} words."
        )

        return words


# ---------------------------------------------------------
# Singleton
# ---------------------------------------------------------

ocr = OCRExtractor()