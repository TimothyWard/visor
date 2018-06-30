from flask import Flask, jsonify, request

from bigbrother.model.click import Click, ClickSchema
from bigbrother.model.impression import Impression, ImpressionSchema
from bigbrother.model.close import Close, CloseSchema
from bigbrother.model.hover import Hover, HoverSchema
from bigbrother.model.scroll import Scroll, ScrollSchema
from bigbrother.model.track import TrackSchema
from bigbrother.model.track_type import TrackType
from bigbrother.model.ad_format import AdFormat
from datetime import datetime as dt
from ipaddress import IPv4Address
import re


app = Flask(__name__)

tracks = [
    # Click('Cialis', '1.1.1.1', AdFormat['MOBILE']),
    # Impression('Viagra', '2.2.2.2', AdFormat['TABLET']),
    # Close('Levitra', '3.3.3.3', AdFormat['DESKTOP'], "CLOSE"),
    # Hover('Stendra', '4.4.4.4', AdFormat['OTHER'], 100, 30),
    # Scroll('Staxyn', '5.5.5.5', AdFormat['APP_BROWSER'])
]


@app.route('/')
def get_root():
    return "Welcome to Big Brother, you're ad-tracking solution!", 200


@app.route('/track/statistics')
def get_statistics():

    tracking_events = [_get_schema_instance(te["track_type"]).make_track_event(te) for te in _get_tracking_events()]

    track_event_lists = {}
    track_event_counts = {}
    for tt in [t.value for t in TrackType]:
        track_event_lists[tt] = [te for te in tracking_events if te.track_type == TrackType[tt]]
        track_event_counts[tt] = track_event_lists[tt].__len__()

    if track_event_counts[TrackType.IMPRESSION.value] == 0:
        conversion_rate = 0
    else:
        conversion_rate = track_event_counts[TrackType.CLICK.value] / track_event_counts[TrackType.IMPRESSION.value]
    statistics = {
        "tracking_counts": track_event_counts,
        "conversion_rate": conversion_rate,
        "heatmap_data": [(h.x_pixel, h.y_pixel) for h in track_event_lists[TrackType.HOVER.value]]
    }
    return jsonify(statistics), 200


@app.route('/track', methods=['GET'])
def get_tracking_events():

    # return the serialized tracking events with a 200 success response
    return jsonify(_get_tracking_events()), 200


def _get_tracking_events():

    filter_vars = _parse_track_query()
    track_events = []

    # for each type of track event in the requested track events
    for track_type in filter_vars["allowed_types"]:
        # keep the results in one global list of track events
        track_events.append(
            # dynamically get the correct schema type for this type of track event
            _get_schema_instance(track_type).dump(
                # filter the data to that schema type only, then to a subset of what is allowed in my data
                _get_filtered_data(
                    _get_track_events_by_type(track_type),
                    filter_vars
                )
            )
        )
    # return the combined and flattened set of tracking records found
    return [item for sublist in [x.data for x in track_events] for item in sublist]


@app.route('/track', methods=['POST'])
def add_tracking_event():
    track = TrackSchema().load(request.get_json())
    track_type = TrackType[track.data['track_type']]
    if track_type not in [TrackType[t.value] for t in TrackType]:
        return "Track Type Is Invalid or Not Specified", 400
    track = _get_schema_instance(track_type).make_track_event(request.get_json())
    _persist_track_event(track)
    return "New Tracking Event Successfully Added", 200


# a better way might be to include a reference to the Schema class on the Object class (not sure how in Python)
def _get_schema_instance(track_type):

    if isinstance(track_type, str):
        track_type = TrackType[track_type]

    if track_type == TrackType.HOVER:
        return HoverSchema(many=True)
    elif track_type == TrackType.CLICK:
        return ClickSchema(many=True)
    elif track_type == TrackType.SCROLL:
        return ScrollSchema(many=True)
    elif track_type == TrackType.IMPRESSION:
        return ImpressionSchema(many=True)
    elif track_type == TrackType.CLOSE:
        return CloseSchema(many=True)


def _persist_track_event(track):
    tracks.append(track)


def _get_track_events_by_type(track_type):
    return [t for t in tracks if t.track_type == track_type]


def _get_filtered_data(data, filter_vars):
    return filter(
        lambda t:
        t.track_type in filter_vars["allowed_types"]
        and (t.ad_name in filter_vars["allowed_names"] or re.match(filter_vars["ad_name_pattern"], t.ad_name))
        and t.ad_format in filter_vars["allowed_formats"]
        and IPv4Address(filter_vars["start_ip"]) <= IPv4Address(t.ip) <= IPv4Address(filter_vars["end_ip"])
        and filter_vars["start_timestamp"] <= dt.strptime(t.timestamp.__str__(), "%Y-%m-%d %H:%M:%S.%f")
            <= filter_vars["end_timestamp"]
        , data
    )


def _parse_track_query():

    # pull request variables from URL params
    track_type = request.args.get('track_type')
    ad_name = request.args.get('ad_name')
    start_ip = request.args.get('start_ip')
    end_ip = request.args.get('end_ip')
    start_timestamp = request.args.get('start_timestamp')
    end_timestamp = request.args.get('end_timestamp')
    ad_format = request.args.get('ad_format')

    # track type must be ALL, a single type, or some comma separated list of types
    if not track_type or track_type == "ALL":
        allowed_types = [TrackType[t.value] for t in TrackType]
    else:
        allowed_types = [TrackType[x.strip()] for x in track_type.split(',')]

    # ad name must be a single name or some comma separated list of names
    ad_name_pattern = ""
    allowed_names = []
    if not ad_name:
        ad_name_pattern = '.*'
    elif ',' in ad_name:
        allowed_names = [n.strip() for n in ad_name.split(',')]
    else:
        ad_name_pattern = ad_name

    # ad format must be ALL, a single format, or some comma separated list of formats
    if not ad_format or ad_format == "ALL":
        allowed_formats = [AdFormat[f.value] for f in AdFormat]
    else:
        allowed_formats = [AdFormat[f.strip()] for f in ad_format.split(',')]

    # default IP address range is ALL IPs
    if not start_ip:
        start_ip = '0.0.0.0'
    if not end_ip:
        end_ip = '255.255.255.255'

    # default datetime range is ALL dates/times
    if not start_timestamp:
        start_timestamp = dt.min
    else:
        start_timestamp = dt.strptime(start_timestamp.__str__(), "%Y-%m-%d %H:%M:%S.%f")
    if not end_timestamp:
        end_timestamp = dt.max
    else:
        end_timestamp = dt.strptime(end_timestamp.__str__(), "%Y-%m-%d %H:%M:%S.%f")

    return {
        "allowed_types": allowed_types,
        "allowed_names": allowed_names,
        "ad_name_pattern": ad_name_pattern,
        "allowed_formats": allowed_formats,
        "start_ip": start_ip,
        "end_ip": end_ip,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp
    }


if __name__ == "__main__":
    app.run()
