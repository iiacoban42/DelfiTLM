"""Scripts for saving the frames into the database"""
import re
import copy
import json
from django.utils.dateparse import parse_datetime
from skyfield.api import load, EarthSatellite
import pytz
from transmission.models import Uplink, Downlink, TLE, Satellite
from members.models import Member


def register_downlink_frames(frames_to_add) -> None:
    """Adds a list of json frames to the downlink table (dummy data)

    Args:
        input: a json containing a list of json object, each of them being a frame
        to be added to the downlink table.
    """
    for frame in frames_to_add["frames"]:
        frame_entry = Downlink()
        frame_entry = parse_frame(frame, frame_entry)
        frame_entry.save()


def add_frame(frame, identifier="downlink", username=None, application=None) -> None:
    """Adds one json frame to the downlink table"""

    frame_entry = None

    if username is not None:
        user = Member.objects.get(username=username)

        if identifier == "uplink":
            if not user.has_perm("transmission.add_uplink"):
                return
            frame_entry = Uplink()

        elif identifier == "downlink":
            if not user.has_perm("transmission.add_downlink"):
                return
            frame_entry = Downlink()
        else:
            return

        frame_entry.radio_amateur = user

    # if present, store the application name/version used to submit the data
    if application is not None:
        frame_entry.application = application

    # copy fields from frame to frame_entry
    frame_entry = parse_frame(frame, frame_entry)

    frame_entry.save()


def parse_frame(frame, frame_entry):
    """Extract frame info from frame and stores it into frame_entry (database frame)"""

    # check if the frame exists and it is a HEX string
    non_hex = re.match("[^0-9A-Fa-f]", frame["frame"])
    if non_hex:
        raise ValueError("Invalid frame, not an hexadecimal value.")

    # assign the frame HEX values
    frame_entry.frame = frame['frame']

    # check is a timestamp is attached
    if "timestamp" not in frame or frame["timestamp"] is None:
        raise ValueError("Invalid submission, no timestamp attached.")

    # assign the timestamp
    frame_entry.timestamp = parse_datetime(frame["timestamp"]).astimezone(pytz.utc)

    # assign frequency, if present
    if "frequency" in frame and frame["frequency"] is not None:
        frame_entry.frequency = frame["frequency"]

    # assign qos, if present
    if "qos" in frame and frame["qos"] is not None:
        frame_entry.qos = frame["qos"]

    # assign sat, if present
    if "sat" in frame and frame["sat"] is not None:
        frame_entry.sat = frame["sat"]

    # add metadata
    metadata = copy.deepcopy(frame)
    # remove previousely parsed fields
    for field in ["frequency", "qos", "sat", "timestamp"]:
        if field in metadata:
            del metadata[field]

    frame_entry.metadata = json.dumps(metadata)

    return frame_entry


def save_tle(tle):
    """Insert a TLE into the database.
        TLE format:
        ISS (ZARYA)
        1 25544U 98067A   08264.51782528 -.00002182  00000-0 -11606-4 0  2927
        2 25544  51.6416 247.4627 0006703 130.5360 325.0288 15.72125391563537
    """
    time_scale = load.timescale()
    tle_split_lines = tle.splitlines()
    sat = tle_split_lines[0]
    line1 = tle_split_lines[1]
    line2 = tle_split_lines[2]

    satellite = EarthSatellite(line1, line2, sat, time_scale)

    epoch = satellite.epoch.utc_datetime()
    # tz = pytz.timezone("Europe/Amsterdam")
    # epoch = satellite.epoch.astimezone(tz)
    tle_instance = TLE()
    tle_instance.valid_from = epoch
    tle_instance.sat = Satellite.objects.get(sat=sat)
    tle_instance.tle = tle

    tle_instance.save()

    return tle_instance
