from enum import Enum


class TimeInForce(str, Enum):
    GTC = "GTC"  # Good Till Cancelled (Maker/Taker)
    IOC = "IOC"  # Immediate Or Cancel (Maker/Taker)
    FOK = "FOK"  # Fill Or Kill (Taker)
