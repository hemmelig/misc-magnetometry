# -*- coding: utf-8 -*-
"""
Convert magnetic field data files from the IMF v1.22 file format to mSEED.

"""

import argparse
import pathlib

from utilities import read_imf


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input_path", type=str, required=True)
    parser.add_argument("-a", "--archive_path", type=str)
    parser.add_argument("-s", "--station", type=str, default="*")
    args = parser.parse_args()

    input_path = pathlib.Path(args.input_path)
    if args.archive_path is None:
        archive_path = input_path.parent / "miniseed"
    else:
        archive_path = pathlib.Path(args.archive_path)

    archive_format = "{year}/IM/{station}/{channel}.D"
    filename_format = "IM.{station}..{channel}.D.{year}.{julday:03d}"

    for file in input_path.glob("*/{args.station}/*.*"):
        print(f"Working on:\n{file}")
        st = read_imf(str(file))
        for tr in st:
            archive_dir = archive_path / archive_format.format(
                year=tr.stats.starttime.year,
                station=tr.stats.station,
                channel=tr.stats.channel
            )
            archive_dir.mkdir(parents=True, exist_ok=True)
            fname = archive_dir / filename_format.format(
                year=tr.stats.starttime.year,
                julday=tr.stats.starttime.julday,
                station=tr.stats.station,
                channel=tr.stats.channel
            )
            tr.write(str(fname), format="MSEED")


if __name__ == "__main__":
    main()
