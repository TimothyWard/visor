from flask import Flask, jsonify, request

from bigbrother.model.click import Click, ClickSchema
from bigbrother.model.impression import Impression, ImpressionSchema
from bigbrother.model.close import Close, CloseSchema
from bigbrother.model.hover import Hover, HoverSchema
from bigbrother.model.scroll import Scroll, ScrollSchema
from bigbrother.model.track import TrackSchema
from bigbrother.model.track_type import TrackType
from bigbrother.model.ad_format import AdFormat
from datetime import datetime

app = Flask(__name__)

tracks = [
    Click('Cialis', '1.1.1.1', AdFormat['MOBILE']),
    Impression('Viagra', '2.2.2.2', AdFormat['TABLET']),
    Close('Levitra', '3.3.3.3', AdFormat['DESKTOP'], "CLOSE"),
    Hover('Stendra', '4.4.4.4', AdFormat['OTHER'], 100, 30),
    Scroll('Staxyn', '5.5.5.5', AdFormat['APP_BROWSER'])
]


@app.route('/status')
def get_status():
    print(tracks)
    return "HOORAY", 200


@app.route('/track')
def get_tracks():

    track_type = request.args.get('track_type')
    ad_name = request.args.get('ad_name')
    start_ip = request.args.get('start_ip')
    end_ip = request.args.get('end_ip')
    start_timestamp = request.args.get('start_timestamp')
    end_timestamp = request.args.get('end_timestamp')
    ad_format = request.args.get('ad_format')

    # track type must be ALL, a single type, or some comma separated list of types
    if not track_type:
        return "Track Type Is Required", 400
    elif track_type == "ALL":
        allowed_types = [TrackType[t.value] for t in TrackType]
    else:
        allowed_types = [TrackType[x.strip()] for x in track_type.split(',')]

    # ad name must be a single name or some comma separated list of names
    if not ad_name:
        return "Ad Name Is Required", 400
    else:
        allowed_names = [n.strip() for n in ad_name.split(',')]

    # ad format must be ALL, a single format, or some comma separated list of formats
    if not ad_format:
        return "Ad Format Is Required", 400
    elif ad_format == "ALL":
        allowed_formats = [AdFormat[f.value] for f in AdFormat]
    else:
        allowed_formats = [AdFormat[f.strip()] for f in ad_format.split(',')]

    if not start_ip:
        start_ip = '0.0.0.0'
    if not end_ip:
        end_ip = '255.255.255.255'
    if not start_timestamp:
        start_timestamp = datetime.min
    if not end_timestamp:
        end_timestamp = datetime.max

    filtered_tracks = TrackSchema(many=True).dump(
        filter(lambda t:
               t.track_type in allowed_types
               and t.ad_name in allowed_names
               and t.ad_format in allowed_formats
               , [t for t in tracks if t.track_type != TrackType.HOVER])
    )

    # treat HOVER tracking events differently because they have more fields
    filtered_hovers = HoverSchema(many=True).dump(
        filter(lambda t:
               t.track_type in allowed_types
               and t.ad_name in allowed_names
               and t.ad_format in allowed_formats
               , [t for t in tracks if t.track_type == TrackType.HOVER])
    )
    return jsonify(filtered_tracks.data + filtered_hovers.data), 200


@app.route('/track', methods=['POST'])
def add_track():

    track_schema = TrackSchema().load(request.get_json())
    track_type = TrackType[track_schema.data['track_type']]
    if track_type not in [TrackType[t.value] for t in TrackType]:
        return "Track Type Is Required", 400

    if track_type == TrackType.HOVER:
        track_schema = HoverSchema().load(request.get_json())
        track = Hover(**track_schema.data)

    elif track_type == TrackType.CLICK:
        track_schema = ClickSchema().load(request.get_json())
        track = Click(**track_schema.data)

    elif track_type == TrackType.SCROLL:
        track_schema = ScrollSchema().load(request.get_json())
        track = Scroll(**track_schema.data)

    elif track_type == TrackType.IMPRESSION:
        track_schema = ImpressionSchema().load(request.get_json())
        track = Impression(**track_schema.data)

    elif track_type == TrackType.CLOSE:
        track_schema = CloseSchema().load(request.get_json())
        track = Close(**track_schema.data)

    tracks.append(track.data)
    return "", 204


if __name__ == "__main__":
    app.run()
