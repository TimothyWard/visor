from marshmallow import post_load

from .track import Track, TrackSchema
from .track_type import TrackType


class Scroll(Track):
    def __init__(self, ad_name, ip, ad_format):
        super(Scroll, self).__init__(ad_name, ip, ad_format, TrackType.SCROLL)

    def __repr__(self):
        return '<Scroll(' \
               'type={self.track_type!r},' \
               'ad_name={self.ad_name!r},' \
               'ip={self.ip!r},' \
               'ad_format={self.ad_format!r}' \
               'timestamp={self.timestamp!r}' \
               ')>'.format(self=self)


class ScrollSchema(TrackSchema):
    @post_load
    def make_expense(self, data):
        return Scroll(**data)
