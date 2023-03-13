# -*- coding: utf-8 -*-
"""
Utilities for converting a data file from the IMF v1.22 data file format to an mSEED
file.

"""

from datetime import datetime
from itertools import chain
from typing import Generator

import numpy as np
from obspy import Stream, Trace, UTCDateTime


def is_marker_line(line: str) -> bool:
    """Check if a line is a marker line."""
    return line[29] == " "


def lines_before_next_marker(
    lines: Generator[str, None, None]
) -> Generator[str, None, None]:
    """Yields all lines up to but not including the next marker line."""

    valid_lines = []
    for line in lines:
        if is_marker_line(line):
            break
        valid_lines.append(line)
    yield from valid_lines


def advance_past_next_marker(lines: Generator[str, None, None]) -> None:
    """Advance a given iterator through the first encountered marker line, if any."""

    for line in lines:
        if is_marker_line(line):
            break


def lines_between_markers(
    lines: Generator[str, None, None]
) -> Generator[str, None, None]:
    """Yields the lines between the first two marker lines."""

    iterator = iter(lines)
    advance_past_next_marker(iterator)
    yield from lines_before_next_marker(iterator)


def derive_metadata(line: str) -> dict:
    """
    Derive the metadata from the first line of an IMF data file.

    Parameters
    ----------
    line: Top line containing basic metadata for the data file.

    Returns
    -------
    meta: A dictionary containing the basic metadata.

    """

    block = line.split()

    starttime = UTCDateTime(
        datetime.strptime(f"{block[1]}_{block[3]}:00", "%b%d%y_%H:%M")
    )

    meta = {
        "station": block[0],
        "network": "",
        "delta": 60,
        "starttime": starttime,
    }

    return meta


def read_imf(filename: str) -> Stream:
    """
    Utility function to convert from the IMF v1.22 data file format to an ObsPy
    Stream object.

    Parameters
    ----------
    filename: Path to the IMF file to be converted.

    Returns
    -------
    st: Stream object containing the N, E, Z, and total field (T) data.

    """

    st = Stream()

    with open(filename, "r") as f:
        lines = iter(f)
        meta = derive_metadata(next(lines))
        data = []
        final_block = False
        i = 1
        while not final_block:
            block = lines_before_next_marker(lines)
            try:
                first_element = next(block)
                block = chain([first_element], block)

                # Extract datapoints to arrays
                for line in block:
                    data.append(line.split()[:4])
                    data.append(line.split()[4:])
                i += 1
            except StopIteration:
                final_block = True

        data = np.asarray(data, dtype=int).T

        # Build traces
        for comp_data, comp in zip(data, "NEZT"):
            st += Trace(
                data=comp_data,
                header={"channel": f"UF{comp}", "npts": len(comp_data), **meta},
            )

        st._cleanup()

        return st
