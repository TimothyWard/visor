from marshmallow import post_load

from .track import Track, TrackSchema
from .track_type import TrackType


class Impression(Track):
    def __init__(self, ad_name, ip, ad_format):
        super(Impression, self).__init__(ad_name, ip, ad_format, TrackType.IMPRESSION)

    def __repr__(self):
        return '<Impression(' \
               'type={self.track_type!r},' \
               'ad_name={self.ad_name!r},' \
               'ip={self.ip!r},' \
               'ad_format={self.ad_format!r}' \
               'timestamp={self.timestamp!r}' \
               ')>'.format(self=self)


class ImpressionSchema(TrackSchema):
    @post_load
    def make_expense(self, data):
        return Impression(**data)
