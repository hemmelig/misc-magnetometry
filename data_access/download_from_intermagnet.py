# -*- coding: utf-8 -*-
"""
Download geomagnetic data from Edinburgh GIN in the IMF v1.22 data format.

This script has been adapted from the automatic script produced by INTERMAGNET.

"""

import argparse
import pathlib

import requests
from obspy import UTCDateTime


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--archive_path", type=str, required=True)
    parser.add_argument("-s", "--station", type=str, required=True)
    parser.add_argument("--spd", type=int, default=1440)
    parser.add_argument("--startdate", type=str, required=True)
    parser.add_argument("-d", "--days", type=int, default=1)
    args = parser.parse_args()

    archive = pathlib.Path(args.archive_path)

    remote_api = (
        "https://imag-data.bgs.ac.uk/GIN_V1/GINServices?Request=GetData"
        f"&format=IMFV122&testObsys=0&observatoryIagaCode={args.station}"
        f"&samplesPerDay={args.spd}&publicationState=adj-or-rep"
        "&recordTermination=UNIX&dataStartDate={startdate}&dataDuration=1"
    )

    # Loop over days
    request_startdate = UTCDateTime(args.startdate)
    for day_count in range(args.days):
        startdate = "-".join([
            f"{request_startdate.year}",
            f"{request_startdate.month:02d}",
            f"{request_startdate.day:02d}",
        ])
        print(f"Downloading data for {startdate}...")
        outfile = (
            archive
            / f"{request_startdate.year}"
            / f"{args.station.upper()}"
            / f"{startdate}.{args.station.lower()}"
        )
        outfile.parent.mkdir(parents=True, exist_ok=True)

        r = requests.get(remote_api.format(startdate=startdate, duration=1))
        with outfile.open("wb") as f:
            f.write(r.content)
        request_startdate += 86400


if __name__ == "__main__":
    main()
