from pathlib import Path

from config import UPLOADS_DIR


def get_latest_pdf() -> Path:
    """
    Returns the most recently modified PDF
    inside the uploads folder.
    """

    pdf_files = list(UPLOADS_DIR.glob("*.pdf"))

    if not pdf_files:
        raise FileNotFoundError(
            "No PDF files found inside the uploads folder."
        )

    latest_pdf = max(
        pdf_files,
        key=lambda file: file.stat().st_mtime
    )

    return latest_pdf