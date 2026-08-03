from datetime import datetime


class Logger:

    def __init__(self):

        self.show_time = True

    # ---------------------------------------------

    def _time(self):

        if not self.show_time:
            return ""

        return datetime.now().strftime(
            "%H:%M:%S"
        )

    # ---------------------------------------------

    def _print(
        self,
        level,
        message
    ):

        if self.show_time:

            print(
                f"[{self._time()}] "
                f"{level} {message}"
            )

        else:

            print(
                f"{level} {message}"
            )

    # ---------------------------------------------

    def info(
        self,
        message
    ):

        self._print(
            "ℹ️",
            message
        )

    # ---------------------------------------------

    def success(
        self,
        message
    ):

        self._print(
            "✅",
            message
        )

    # ---------------------------------------------

    def warning(
        self,
        message
    ):

        self._print(
            "⚠️",
            message
        )

    # ---------------------------------------------

    def error(
        self,
        message
    ):

        self._print(
            "❌",
            message
        )

    # ---------------------------------------------

    def header(
        self,
        title
    ):

        print()

        print("=" * 60)

        print(title)

        print("=" * 60)


log = Logger()