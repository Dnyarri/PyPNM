# PyPNM - PPM and PGM image files reading, viewing and writing module in pure Python

## Overview

PyPNM is a pure Python module, providing functions for:

- **reading** PPM and PGM image files (both 8 and 16 bits per channel color depth, both binary and ASCII files) to image 3D nested lists for further editing;

  Reading support for 1 bpc PBM is provided as well. Writing PBM is not supported and not planned.

- **displaying** 3D list thus obtained by converting it to Tkinter-compatible data in memory;
- **writing** edited image 3D list to disk as PPM or PGM file, either binary or ASCII.

Functions are detailed in *"Functions description"*, and illustrated in *"Usage example"* sections below.

## Image representation

Image structure is `list(list(list(int)))`. Note that for L images it's still `list(list(list(int)))`, i.e. a pixel is a list of 1 int. Note that PBM files get promoted from 1-bit ink on/off color space to 8-bit L images when reading.

## Installation

In case of installing from PyPI via `pip`:

```console
python -m pip install --upgrade PyPNM
```

## Usage

Since version 2.21.3.4.post7 recommended import is:

```python
import pypnm
```

Note that legacy import schemes like

```python
from pypnm import pnmlpnm
```

are still working, so old programs do not need rewriting after PyPNM update.

## Usage example

Below is a minimal Python program, illustrating all PyPNM functions at once: reading PPM file (image files are not included into PyPI PyPNM distribution. You may use any of [compatibility testing samples](https://github.com/Dnyarri/PyPNM/tree/main/compatibility) from Git repository) to image nested list, writing image list to disk as binary PPM, writing image list as ASCII PPM, and displaying image list using Tkinter:

```python
#!/usr/bin/env python3

from tkinter import Button, PhotoImage, Tk

from pypnm import list2bin, list2pnm, pnm2list

X, Y, Z, maxcolors, image3D = pnm2list('example.ppm')  # Open "example.ppm"
list2pnm('binary.ppm', image3D, maxcolors, bin=True)  # Save as binary pnm
list2pnm('ascii.ppm', image3D, maxcolors, bin=False)  # Save as ascii pnm

main_window = Tk()
main_window.title('PyPNM demo')
preview_data = list2bin(image3D, maxcolors)  # Image list -> preview bytes
preview = PhotoImage(data=preview_data)  # Preview bytes -> PhotoImage object
preview_button = Button(main_window, text='Example\n(click to exit)', image=preview,
    compound='top', command=lambda: main_window.destroy())  # Showing PhotoImage
preview_button.pack()
main_window.mainloop()

```

## Functions description

PyPNM module contains 100% pure Python implementation of everything one may need to read and write a variety of PGM and PPM files, as well as to display corresponding image data. No non-standard dependencies used, no extra downloads needed, no dependency version conflicts expected. All the functionality is provided as functions/procedures, as simple as possible; main functions are listed below:

- **pnm2list**  - reading binary or ASCII RGB PPM or L PGM file and returning image data as nested list of int.
- **list2bin**  - getting image data as nested list of int and creating binary PPM (P6) or PGM (P5) data structure in memory. Suitable for generating data to display with Tkinter.
- **list2pnm** - getting image data as nested list of int and writing either binary or ASCII file depending on `bin` argument.

Detailed functions arguments description is provided below, as well as in module docstrings and [PyPNM documentation bedside book (PDF)](https://dnyarri.github.io/pypnm/pypnm.pdf).

### pnm2list

```python
X, Y, Z, maxcolors, image3D = pypnm.pnm2list(in_filename, tuplevel)
```

Read data from PPM/PGM file to nested image data list, where:

- `X, Y, Z`    - image sizes (int);
- `maxcolors`  - maximal color value per channel for current image (int), either 255, or 65535;
- `image3D`    - image pixel data as list(list(list(int)));
- `in_filename` - PPM/PGM file name (str);
- `tuplevel`   - `image3D` structure switch:
  - `tuplevel='image'`: `image3D` is tuple(tuple(tuple(int)));
  - `tuplevel='pixel'`: `image3D` is list(list(tuple(int)));
  - `tuplevel=` other: `image3D` is list(list(list(int))).

  Default `tuplevel=None`, meaning no tuples are used, and `image3D` structure is list(list(list(int))).

### list2bin

```python
image_bytes = pypnm.list2bin(image3D, maxcolors, show_chessboard)
```

Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory, where:

- `image3D`   - list (image) of lists (rows) of lists (pixels) of ints (channel values), having `Y * X * Z` size;
- `maxcolors` - maximal color value per channel for current image (int), either 255, or 65535;
- `show_chessboard` - optional bool, set `True` to show LA and RGBA images against chessboard pattern; `False` or missing show existing L or RGB data for transparent areas as opaque (see the Note below).

   Default is `False` for backward compatibility;

- `image_bytes` - returned PNM-structured binary data.

  `image_bytes` object thus obtained is well compatible with Tkinter `PhotoImage(data=...)` method and therefore may be used to (and actually was developed for) visualize any data represented as image-like 3D list.

> **Note:**
>
> When encountering image list with 2 or 4 channels, current version of `list2bin` may treat it as LA or RGBA image correspondingly, and generate image preview for Tkinter as transparent over chessboard background (like Photoshop or GIMP). Since PNM images do not have transparency, this preview is actually either L or RGB, with image mixed with chessboard background, generated by `list2bin` on the fly.
>
> This behaviour is controlled by `show_chessboard` option. Default setting is `False` (meaning simply ignoring alpha channel) for backward compatibility.

### list2pnm

```python
pypnm.list2pnm(out_filename, image3D, maxcolors, bin)
```

Write either binary or ASCII file from nested image data list, where:

- `out_filename` - name of PNM file to be written.
- `image3D`   - `Y * X * Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - maximal color value per channel for current image (int), either 255, or 65535;
- `bin` - switch (bool) defining whether to write binary PNM file or ASCII one.

   Default is `True`, meaning binary output, to provide backward compatibility.

Note that `list2pnm` is a switch between internal `list2pnmbin` and `list2pnmascii` functions, whose direct usage is considered legacy. Using `list2pnm` instead of legacy calls simplifies writing "Save as..." functions for main programs - now you can use one function for all PNM flavours. Default is `bin = True` since binary PNM seem to be more convenient for big programs like Photoshop.

## References

1. [Netpbm file formats specifications](https://netpbm.sourceforge.net/doc/) strictly followed in the course of PyPNM development.

2. [PyPNM at Github](https://github.com/Dnyarri/PyPNM) contains both PyPNM module and viewer application example, illustrating using `list2bin` to produce data for Tkinter `PhotoImage(data=...)` to display, and other PyPNM functions for opening/saving various portable map formats (so viewer may be used as converter between binary and ASCII variants of PPM and PGM files).

   Issues and discussions are open for possible bug reports and suggestions, correspondingly.

3. [PyPNM for Python 3.4 at Github](https://github.com/Dnyarri/PyPNM/tree/py34/) - same as above, but compatible with Python down to 3.4. Besides PPM and PGM support, image viewer in this branch also have PNG support, based on [PyPNG](https://gitlab.com/drj11/pypng), and therefore may be used as pure Python PNM <=> PNG converter.

4. [PyPNM bedside book (PyPNM documentation in PDF format)](https://dnyarri.github.io/pypnm/pypnm.pdf).

5. [PyPNM home page with explanations and versions description](https://dnyarri.github.io/pypnm.html).
