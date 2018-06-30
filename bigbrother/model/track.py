from marshmallow import Schema, fields
from datetime import datetime as dt


class Track(object):
    def __init__(self, ad_name, ip, ad_format, track_type, timestamp=None):
        self.ad_name = ad_name
        self.ip = ip
        self.ad_format = ad_format
        self.track_type = track_type
        if not timestamp:
            self.timestamp = dt.utcnow()
        else:
            self.timestamp = dt.strptime(timestamp, "%Y-%m-%dT%H:%M:%S.%f+00:00")

    def __repr__(self):
        return '<Track(' \
               'track_type={self.track_type!r},' \
               'ad_name={self.ad_name!r},' \
               'ip={self.ip!r},' \
               'ad_format={self.ad_format!r}' \
               'timestamp={self.timestamp!r}' \
               ')>'.format(self=self)


class TrackSchema(Schema):
    track_type = fields.Str()
    ad_name = fields.Str()
    ip = fields.Str()
    timestamp = fields.DateTime()
    ad_format = fields.Str()
