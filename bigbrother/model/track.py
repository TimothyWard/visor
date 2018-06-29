import datetime as dt

from marshmallow import Schema, fields


class Track(object):
    def __init__(self, ad_name, ip, ad_format, track_type):
        self.ad_name = ad_name
        self.ip = ip
        self.ad_format = ad_format
        self.track_type = track_type
        self.timestamp = dt.datetime.now()

    def __repr__(self):
        return '<Track(' \
               'type={self.track_type!r},' \
               'ad_name={self.ad_name!r},' \
               'ip={self.ip!r},' \
               'ad_format={self.ad_format!r}' \
               'timestamp={self.timestamp!r}' \
               ')>'.format(self=self)


class TrackSchema(Schema):
    track_type = fields.Str()
    ad_name = fields.Str()
    ip = fields.Str()
    timestamp = fields.Date()
    ad_format = fields.Str()
