from difflib import SequenceMatcher


class FlightMatcher:

    def __init__(self):

        #
        # Minimum similarity required
        #
        self.threshold = 0.90

    # ---------------------------------------------------------
    # Normalize Flight Number
    # ---------------------------------------------------------

    def normalize(self, text):

        if not text:
            return ""

        return (
            text.upper()
                .replace(" ", "")
                .replace("-", "")
                .replace("_", "")
                .strip()
        )

    # ---------------------------------------------------------
    # Similarity Score
    # ---------------------------------------------------------

    def similarity(

        self,

        portal,

        pdf

    ):

        portal = self.normalize(portal)

        pdf = self.normalize(pdf)

        return SequenceMatcher(

            None,

            portal,

            pdf

        ).ratio()

    # ---------------------------------------------------------
    # Match
    # ---------------------------------------------------------

    def match(

        self,

        portal,

        pdf

    ):

        portal = self.normalize(portal)

        pdf = self.normalize(pdf)

        #
        # Exact Match
        #

        if portal == pdf:

            return True

        #
        # Similar Match
        #

        score = self.similarity(

            portal,

            pdf

        )

        print(

            f"Similarity : "

            f"{portal}"

            f" <-> "

            f"{pdf}"

            f" = "

            f"{score:.2f}"

        )

        return score >= self.threshold


matcher = FlightMatcher()