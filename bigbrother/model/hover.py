from marshmallow import post_load, Schema, fields
from .track import Track, TrackSchema
from .track_type import TrackType
from bigbrother.model.ad_format import AdFormat


class Hover(Track):
    def __init__(self, ad_name, ip, ad_format, x_pixel, y_pixel, track_type="HOVER", timestamp=None):
        if isinstance(ad_format, str):
            ad_format = AdFormat[ad_format]
        self.x_pixel = x_pixel
        self.y_pixel = y_pixel
        super(Hover, self).__init__(ad_name, ip, ad_format, TrackType[track_type], timestamp)

    def __repr__(self):
        return '<Hover(' \
               'track_type={self.track_type!r},' \
               'ad_name={self.ad_name!r},' \
               'ip={self.ip!r},' \
               'ad_format={self.ad_format!r}' \
               'x_pixel={self.x_pixel!r}' \
               'y_pixel={self.y_pixel!r}' \
               'timestamp={self.timestamp!r}' \
               ')>'.format(self=self)


class HoverSchema(TrackSchema):

    x_pixel = fields.Number()
    y_pixel = fields.Number()

    @post_load
    def make_track_event(self, data):
        return Hover(**data)
