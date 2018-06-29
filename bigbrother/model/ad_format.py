from enum import Enum


class AdFormat(Enum):

    def __str__(self):
        return str(self.value)

    MOBILE = "MOBILE"
    TABLET = "TABLET"
    DESKTOP = "DESKTOP"
    OTHER = "OTHER"
    APP_BROWSER = "APP_BROWSER"
