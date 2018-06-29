from enum import Enum


class TrackType(Enum):

    def __str__(self):
        return str(self.value)

    CLOSE = "CLOSE"
    CLICK = "CLICK"
    HOVER = "HOVER"
    SCROLL = "SCROLL"
    IMPRESSION = "IMPRESSION"
