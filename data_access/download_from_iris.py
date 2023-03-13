# -*- coding: utf-8 -*-
"""
This script will download magnetic field data from IRIS in the mSEED format.

Can also be used to retrieve data from other datacentres.

"""

import argparse
import pathlib

from obspy import UTCDateTime
from obspy.clients.fdsn import Client
from obspy.clients.fdsn.header import FDSNNoDataException


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-a", "--archive_path", type=str, required=True)
    parser.add_argument("-n", "--network", type=str, required=True)
    parser.add_argument("-s", "--station", type=str, required=True)
    parser.add_argument("--starttime", type=str, required=True)
    parser.add_argument("--endtime", type=str, required=True)
    parser.add_argument("-d", "--data_center", type=str, default="IRIS")
    args = parser.parse_args()

    archive = pathlib.Path(args.archive_path)

    # --- Download waveform data ---
    read_from = UTCDateTime(args.starttime)
    while read_from < UTCDateTime(args.endtime):
        print(f"\t...retrieving waveform data on {read_from}...")
        try:
            client = Client(args.data_center)
            st = client.get_waveforms(
                network=args.network,
                station=args.station,
                location="*",
                channel="*F*",
                starttime=read_from,
                endtime=UTCDateTime(read_from.date) + 86400
            )
        except FDSNNoDataException:
            print(
                f"\t\t...no waveform data for OKBR on {read_from}..."
            )
            read_from = UTCDateTime(read_from.date) + 86400
            continue
        print("\tWaveforms retrieved, writing...")
        st.merge(method=-1)
        
        for comp in "ZNE":
            channel_code = st.select(component=comp)[0].stats.channel
            waveform_path = (
                archive
                / f"{read_from.year}/{args.network}/{args.station}/{channel_code}.D"
            )
            waveform_path.mkdir(parents=True, exist_ok=True)

            fname = (
                f"{args.network}.{args.station}..{channel_code}.D."
                f"{read_from.year}.{read_from.julday:03d}"
            )
            try:
                st_comp = st.select(component=comp)
                if not bool(st_comp):
                    continue
                st_comp.write(
                    str(waveform_path / fname),
                    format="MSEED"
                )
            except IndexError:
                pass

        read_from = UTCDateTime(read_from.date) + 86400


if __name__ == "__main__":
    main()
