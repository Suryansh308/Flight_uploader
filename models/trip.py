from dataclasses import dataclass


@dataclass
class TripDocument:
    flight_number: str
    flight_date: str
    page_number: int