from marshmallow import post_load

from .track import Track, TrackSchema
from .track_type import TrackType


class Close(Track):
    def __init__(self, ad_name, ip, ad_format, track_type):
        super(Close, self).__init__(ad_name, ip, ad_format, TrackType[track_type])

    def __repr__(self):
        return '<Close(' \
               'type={self.track_type!r},' \
               'ad_name={self.ad_name!r},' \
               'ip={self.ip!r},' \
               'ad_format={self.ad_format!r}' \
               'timestamp={self.timestamp!r}' \
               ')>'.format(self=self)


class CloseSchema(TrackSchema):
    @post_load
    def make_expense(self, data):
        return Close(**data)
