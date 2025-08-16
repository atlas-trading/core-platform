from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class StatusDTO:
    status: str  # 'ok' | 'shutdown' | 'error' | 'maintenance'
    updated: int | None  # 1723738473621
    eta: int | None  # Estimated time of service restoration
    url: str | None  # URL for more information, if available
    # info (original data from exchange)
