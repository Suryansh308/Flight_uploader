import easyocr


class OCRReader:
    def __init__(self):
        """
        Initialize the EasyOCR reader once.
        """
        self.reader = easyocr.Reader(
            ["en"],
            gpu=False
        )

    def read(self, image):
        """
        Reads text from an OpenCV image.

        Parameters
        ----------
        image : numpy.ndarray

        Returns
        -------
        str
            Extracted text.
        """

        results = self.reader.readtext(
            image,
            detail=0
        )

        if not results:
            return ""

        return " ".join(results).strip()