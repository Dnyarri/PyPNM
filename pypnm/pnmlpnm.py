#!/usr/bin/env python3

"""Functions to read PPM and PGM files to nested 3D list of int and/or write back.

Overview
---------

pnmlpnm (pnm-list-pnm) module is a pack of functions for dealing with PPM and PGM image files.
Functions included are:

- pnm2list: reading binary or ascii RGB PPM or L PGM file and returning image data as nested list of int.
- list2bin: getting image data as nested list of int
and creating binary PPM (P6) or PGM (P5) data structure in memory.
Suitable for generating data to display with Tkinter `PhotoImage(data=...)` class.
- list2pnm: getting image data as nested list of int and writing binary PPM (P6) or PGM (P5) image file.
Note that bytes generations procedure is optimized to save memory
while working with large files and therefore is different from that used in 'list2bin'.
- list2pnmascii: alternative function to write ASCII PPM (P3) or PGM (P2) files.
- create_image: creating empty nested 3D list for image representation.
Not used within this particular module but often needed by programs this module is supposed to be used with.

Installation
-------------

Via PyPI:

    `pip install PyPNM`

then in your program import section:

    `from pypnm import pnmlpnm`

If you acquired module in some other, non-PyPI way, you may simply put module into your main program folder.

Usage
------
After `import pnmlpnm`, use something like:

    `X, Y, Z, maxcolors, list_3d = pnmlpnm.pnm2list(in_filename)`

for reading data from PPM/PGM, where:

- `X`, `Y`, `Z`: image dimensions (int);
- `maxcolors`: number of colors per channel for current image (int);
- `list_3d`: image pixel data as list(list(list(int)));

and:

    `pnm_bytes = pnmlpnm.list2bin(list_3d, maxcolors)`

for writing data from `list_3d` nested list to `pnm_bytes` bytes object in memory,

or:

    `pnmlpnm.list2pnm(out_filename, list_3d, maxcolors)`

for writing data from `list_3d` nested list to binary PPM/PGM file `out_filename`, or:

    `pnmlpnm.list2pnmascii(out_filename, list_3d, maxcolors)`

for writing data from `list_3d` nested list to ASCII PPM/PGM file `out_filename`.


Copyright and redistribution
-----------------------------
Written by `Ilya Razmanov <https://dnyarri.github.io/>`_ to provide working with PPM/PGM files
and converting image-like data to PPM/PGM bytes to be displayed with Tkinter `PhotoImage` class.

May be freely used, redistributed and modified.
In case of introducing useful modifications, please report to the developer.

References
-----------

`Netpbm specifications <https://netpbm.sourceforge.net/doc/>`_

`PyPNM at GitHub <https://github.com/Dnyarri/PyPNM/>`_

`PyPNM at PyPI <https://pypi.org/project/PyPNM/>`_

Version history
----------------

0.11.26.0   Initial working version 26 Nov 2024.

1.12.14.1   Public release at `PyPI <https://pypi.org/project/PyPNM/>`_.

1.13.09.0   Complete rewriting of `pnm2list` using `re` and `array`; PPM and PGM support rewritten.

1.13.10.5   Header pattern seem to comprise all problematic cases; PBM support rewritten.

1.14.08.12  File output rewritten to reduce memory usage; `list2pnm` per row, `list2pnmascii` per sample.

1.15.1.1    Rendering preview for LA and RGBA against chessboard added to `list2bin`,
controlled by optional `show_chessboard` bool added to arguments.
Default is `False` (i.e. simply ignoring alpha) for backward compatibility.
Improved robustness.

1.15.19.19  General branch shortening and more cleanup. Minor bogus stuff removed.
Yet another final version ;-)

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2024-2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '1.15.19.19'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

import array
import re

""" ╔══════════╗
    ║ pnm2list ║
    ╚══════════╝ """


def pnm2list(in_filename: str) -> tuple[int, int, int, int, list[list[list[int]]]]:
    """Read PGM or PPM file to nested image data list.

    Usage
    -

        `X, Y, Z, maxcolors, list_3d = pnmlpnm.pnm2list(in_filename)`

    for reading data from PPM/PGM, where:

    - `X`, `Y`, `Z`: image dimensions (int);
    - `maxcolors`: number of colors per channel for current image (int);
    - `list_3d`: image pixel data as list(list(list(int)));
    - `in_filename`: PPM/PGM file name (str).

    """

    with open(in_filename, 'rb') as file:  # Open file in binary mode
        full_bytes = file.read()

    if full_bytes.startswith((b'P6', b'P5', b'P3', b'P2')):
        """ ┌────────────────────┐
            │ IF Continuous tone │
            └────────────────────┘ """
        # Getting header by pattern
        header: list[bytes] = re.search(
            rb'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
            rb'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
            rb'\s*(\d+)\s(?:\s*#.*\s)*'
            rb'\s*(\d+)\s)',
            full_bytes,
        ).groups()

        magic, X, Y, maxcolors = header

        magic = (magic.split()[0]).decode()
        X = int(X)
        Y = int(Y)
        maxcolors = int(maxcolors)

        # Removing header by the same pattern, leaving only image data
        filtered_bytes = re.sub(
            rb'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
            rb'\s*(\d+)\s(?:\s*#.*\s)*'
            rb'\s*(\d+)\s(?:\s*#.*\s)*'
            rb'\s*(\d+)\s)',
            b'',  # empty space to replace with
            full_bytes,
        )

        del full_bytes  # Cleanup

        if (magic == 'P6') or (magic == 'P3'):
            Z = 3
        elif (magic == 'P5') or (magic == 'P2'):
            Z = 1

        if (magic == 'P6') or (magic == 'P5'):
            """ ┌───────────────────────────┐
                │ IF Binary continuous tone │
                └───────────────────────────┘ """
            if maxcolors < 256:
                datatype = 'B'
            else:
                datatype = 'H'

            array_1d = array.array(datatype, filtered_bytes)

            array_1d.byteswap()  # Critical for 16 bits per channel

            list_1d = array_1d.tolist()

            del array_1d  # Cleanup

            list_3d = [[[list_1d[z + x * Z + y * X * Z] for z in range(Z)] for x in range(X)] for y in range(Y)]

            del list_1d  # Cleanup

            return (X, Y, Z, maxcolors, list_3d)  # Output mimic that of pnglpng

        if (magic == 'P3') or (magic == 'P2'):
            """ ┌──────────────────────────┐
                │ IF ASCII continuous tone │
                └──────────────────────────┘ """
            list_1d = filtered_bytes.split()

            list_3d = [[[int(list_1d[z + x * Z + y * X * Z]) for z in range(Z)] for x in range(X)] for y in range(Y)]

            del list_1d  # Cleanup

            return (X, Y, Z, maxcolors, list_3d)  # Output mimic that of pnglpng

    elif full_bytes.startswith((b'P4', b'P1')):
        """ ┌────────────────┐
            │ IF 1 Bit/pixel │
            └────────────────┘ """
        # Getting header by pattern. Note that for 1 bit pattern does not include maxcolors
        header: list[bytes] = re.search(
            rb'(^P\d\s(?:\s*#.*\s)*'  # last \s gives better compatibility than [\r\n]
            rb'\s*(\d+)\s(?:\s*#.*\s)*'  # first \s further improves compatibility
            rb'\s*(\d+)\s)',
            full_bytes,
        ).groups()

        magic, X, Y = header

        magic = (magic.split()[0]).decode()
        X = int(X)
        Y = int(Y)
        Z = 1
        maxcolors = 255  # Forcing conversion to L

        # Removing header by the same pattern, leaving only image data
        filtered_bytes = re.sub(
            rb'(^P\d\s(?:\s*#.*\s)*'  # pattern to replace to
            rb'\s*(\d+)\s(?:\s*#.*\s)*'
            rb'\s*(\d+)\s)',
            b'',  # empty space to replace with
            full_bytes,
        )

        del full_bytes  # Cleanup

        if magic == 'P4':
            """ ┌───────────────────────┐
                │ IF Binary 1 Bit/pixel │
                └───────────────────────┘ """

            row_width = (X + 7) // 8  # Rounded up version of width, to get whole bytes including junk at EOLNs

            list_3d = []
            for y in range(Y):
                row = []
                for x in range(row_width):
                    single_byte = filtered_bytes[(y * row_width) + x]
                    single_byte_bits = [int(bit) for bit in bin(single_byte)[2:].zfill(8)]
                    single_byte_bits_normalized = [[255 * (1 - c)] for c in single_byte_bits]  # renormalizing colors from ink on/off to L model, replacing int with [int]
                    row.extend(single_byte_bits_normalized)  # assembling row, junk included

                list_3d.append(row[0:X])  # apparently cutting junk off

            return (X, Y, Z, maxcolors, list_3d)  # Output mimic that of pnglpng

        if magic == 'P1':
            """ ┌──────────────────────┐
                │ IF ASCII 1 Bit/pixel │
                └──────────────────────┘ """

            """ Removing any formatting by consecutive split/join, then changing types to turn bit char into int while reshaping to 3D nested list probably is not the fastest solution but I will think about it tomorrow. """
            list_1d = list(str(b''.join(filtered_bytes.split())))[2:-1]  # Slicing off junk chars like 'b', "'"

            list_3d = [[[(255 * (1 - int(list_1d[z + x * Z + y * X * Z]))) for z in range(Z)] for x in range(X)] for y in range(Y)]

            del list_1d  # Cleanup

            return (X, Y, Z, maxcolors, list_3d)  # Output mimic that of pnglpng

    else:
        raise ValueError(f'Unsupported format {in_filename}: {full_bytes[:32]}')


""" ╔══════════╗
    ║ list2bin ║
    ╚══════════╝ """


def list2bin(list_3d: list[list[list[int]]], maxcolors: int, show_chessboard: bool = False) -> bytes:
    """Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory to be used with Tkinter PhotoImage(data=...).

    Based on `Netpbm specifications<https://netpbm.sourceforge.net/doc/>`_.

    Usage
    -

        `image_bytes = pnmlpnm.list2bin(list_3d, maxcolors, show_chessboard)` where:

    Input:

    - `list_3d`: Y * X * Z list (image) of lists (rows) of lists (pixels) of ints (channel values);
    - `maxcolors`: number of colors per channel for current image (int);
    - `show_chessboard`: optional bool, set `True` to show LA and RGBA images against chessboard pattern; `False` or missing show existing L or RGB data for transparent areas as opaque. Default is `False` for backward compatibility.

    Output:

    - `image_bytes`: PNM-structured binary data.

    """

    def _chess(x: int, y: int) -> int:
        """Chessboard pattern, size and color match Photoshop 7.0.

        Photoshop chess pattern preset parameters:
        Small: 4 px; Medium: 8 px, Large: 16 px
        Light: 0.8, 1; Medium: 0.4, 0.6; Dark: 0.2, 0.4 of maxcolors

        """
        return int(maxcolors * 0.8) if ((y // 8) % 2) == ((x // 8) % 2) else maxcolors

    # Determining list dimensions
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    if Z < 3:
        magic = 'P5'
    else:
        magic = 'P6'

    if Z == 3 or Z == 1:  # Source has no alpha
        Z_READ = Z
        # Flattening 3D list to 1D list
        list_1d = [list_3d[y][x][z] for y in range(Y) for x in range(X) for z in range(Z_READ)]

    else:  # Source has alpha
        Z_READ = min(Z, 4) - 1  # To fiddle with alpha; clipping anything above RGBA off

        if show_chessboard:
            # Flattening 3D list to 1D list, mixing with chessboard
            list_1d = [(((list_3d[y][x][z] * list_3d[y][x][Z_READ]) + (_chess(x, y) * (maxcolors - list_3d[y][x][Z_READ]))) // maxcolors) for y in range(Y) for x in range(X) for z in range(Z_READ)]
        else:
            # Flattening 3D list to 1D list, skipping alpha
            list_1d = [list_3d[y][x][z] for y in range(Y) for x in range(X) for z in range(Z_READ)]

    del list_3d  # Cleanup

    if maxcolors < 256:
        datatype = 'B'
    else:
        datatype = 'H'

    content = array.array(datatype, list_1d)

    del list_1d  # Cleanup

    content.byteswap()  # Critical for 16 bits per channel

    return f'{magic}\n{X} {Y}\n{maxcolors}\n'.encode('ascii') + content.tobytes()
# End of 'list2bin' list to in-memory PNM conversion function


""" ╔══════════╗
    ║ list2pnm ║
    ╚══════════╝ """


def list2pnm(out_filename: str, list_3d: list[list[list[int]]], maxcolors: int) -> None:
    """Write binary PNM `out_filename` file; writing performed per row to reduce RAM usage.

    Usage
    -

        `pnmlpnm.list2pnm(out_filename, list_3d, maxcolors)` where:

    - `list_3d`: X * Y * Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - `maxcolors`: number of colors per channel for current image (int);
    - `out_filename`: PNM file name.

    """

    # Determining list dimensions
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    if Z < 3:
        magic = 'P5'
    else:
        magic = 'P6'

    if Z == 3 or Z == 1:
        Z_READ = Z
    else:
        Z_READ = min(Z, 4) - 1  # To skip alpha later

    if maxcolors < 256:
        datatype = 'B'
    else:
        datatype = 'H'

    with open(out_filename, 'wb') as file_pnm:
        file_pnm.write(array.array('B', f'{magic}\n{X} {Y}\n{maxcolors}\n'.encode('ascii')))  # Writing PNM header to file
        for y in range(Y):
            row_1d = [list_3d[y][x][z] for x in range(X) for z in range(Z_READ)]  # Flattening row
            row_array = array.array(datatype, row_1d)  # list[int] to array
            row_array.byteswap()  # Critical for 16 bits per channel
            file_pnm.write(row_array)  # Adding row bytes array to file

    return None
# End of 'list2pnm' function writing binary PPM/PGM file


""" ╔═══════════════╗
    ║ list2pnmascii ║
    ╚═══════════════╝ """


def list2pnmascii(out_filename: str, list_3d: list[list[list[int]]], maxcolors: int) -> None:
    """Write ASCII PNM `out_filename` file; writing performed per sample to reduce RAM usage.

    Usage
    -

        `pnmlpnm.list2pnmascii(out_filename, list_3d, maxcolors)` where:

    - `list_3d`: Y * X * Z list (image) of lists (rows) of lists (pixels) of ints (channels);
    - `maxcolors`: number of colors per channel for current image (int);
    - `out_filename`: PNM file name.

    """

    # Determining list dimensions
    Y = len(list_3d)
    X = len(list_3d[0])
    Z = len(list_3d[0][0])

    if Z == 1:  # L image
        magic = 'P2'
        Z_READ = 1

    if Z == 2:  # LA image
        magic = 'P2'
        Z_READ = 1  # To skip alpha later

    if Z == 3:  # RGB image
        magic = 'P3'
        Z_READ = 3

    if Z > 3:  # RGBA image
        magic = 'P3'
        Z_READ = 3  # To skip alpha later

    with open(out_filename, 'w') as file_pnm:
        file_pnm.write(f'{magic}\n{X} {Y}\n{maxcolors}\n')  # Writing file header
        sample_count = 0  # Start counting samples to break line <= 60 char
        for y in range(Y):
            for x in range(X):
                for z in range(Z_READ):
                    sample_count += 1
                    if (sample_count % 3) == 0:  # 3 must fit any specs for line length
                        file_pnm.write('\n')  # Writing break to fulfill specs line <= 60 char
                    file_pnm.write(f'{list_3d[y][x][z]} ')  # Writing channel value to file

    return None
# End of 'list2pnmascii' function writing ASCII PPM/PGM file


""" ╔════════════════════╗
    ║ Create empty image ║
    ╚════════════════════╝ """


def create_image(X: int, Y: int, Z: int) -> list[list[list[int]]]:
    """Create empty 3D nested list of X * Y * Z size."""

    new_image = [
                    [
                        [0 for z in range(Z)] for x in range(X)
                    ] for y in range(Y)
                ]

    return new_image
# End of 'create_image' empty nested 3D list creation


# --------------------------------------------------------------

if __name__ == '__main__':
    print('Module to be imported, not run as standalone')
