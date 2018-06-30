from marshmallow import post_load

from .track import Track, TrackSchema
from .track_type import TrackType
from bigbrother.model.ad_format import AdFormat


class Close(Track):
    def __init__(self, ad_name, ip, ad_format, track_type="CLOSE", timestamp=None):
        if isinstance(ad_format, str):
            ad_format = AdFormat[ad_format]
        super(Close, self).__init__(ad_name, ip, ad_format, TrackType[track_type], timestamp)

    def __repr__(self):
        return '<Close(' \
               'track_type={self.track_type!r},' \
               'ad_name={self.ad_name!r},' \
               'ip={self.ip!r},' \
               'ad_format={self.ad_format!r}' \
               'timestamp={self.timestamp!r}' \
               ')>'.format(self=self)


class CloseSchema(TrackSchema):
    @post_load
    def make_track_event(self, data):
        return Close(**data)
