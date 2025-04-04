
| 【EN】 | [〖RU〗](README.RU.md) |
| ---- | ---- |

# PyPNM - Pure Python PPM and PGM image files reading and writing module

![PyPI - Downloads](https://img.shields.io/pypi/dm/pypnm)

## Overview and justification

PPM ([Portable Pixel Map](https://netpbm.sourceforge.net/doc/ppm.html)) and PGM ([Portable Gray Map](https://netpbm.sourceforge.net/doc/pgm.html)) (particular cases of PNM format group) are simplest file formats for RGB and L images, correspondingly. Paradoxically, this simplicity lead to some adverse consequences:

- lack of strict official specification. Instead, you may find words like "usual" in format description. Surely, there is someone who implement this part of image format in unprohibited, yet a totally unusual way.

- unwillingness of many software developers to provide any good support for simple and open format. It took years for almighty Adobe Photoshop developers to include PNM module in distribution rather than count on third-party developers, and surely (see above) they took their chance to implement a separator scheme nobody else uses. What as to PNM support in Python, say, Pillow... sorry, I promised not to mention Pillow anywhere ladies and children are allowed to read it.

As a result, novice Python user (like me) may find it difficult to get reliable input/output modules for PPM and PGM image formats.

## Objectives

1. Obtain suitable facility for visualization of image-like data (images first and foremost), existing in form of 3D nested lists, via Tkinter `PhotoImage(data=...)` method.

2. Obtain simple and compact cross-platform module for reading PPM and PGM files as 3D nested lists for further processing with Python, and subsequent writing of processed 3D nested lists data to PPM or PGM files.

To accomplish this, current PyPNM module was developed, combining input/output functions for 8-bits and 16-bits per channel binary and ascii [Portable Gray Map](https://netpbm.sourceforge.net/doc/pgm.html) and [Portable Pixel Map](https://netpbm.sourceforge.net/doc/ppm.html) files, i.e. P2, P5, P3 and P6 PNM file types. All color depth ranges supported directly, without limitations and without dancing with tambourine and proclaiming it to be a novel method.

## Format compatibility

Current PyPNM module read and write capabilities are briefly summarized below.

| Image format | File format | Read | Write |
| ------ | ------ | ------ | ------ |
| 16 bits per channel RGB | P6 Binary PPM | ✅ | ✅ |
| 16 bits per channel RGB | P3 ASCII PPM | ✅ | ✅ |
| 8 bits per channel RGB | P6 Binary PPM | ✅ | ✅ |
| 8 bits per channel RGB | P3 ASCII PPM | ✅ | ✅ |
| 16 bits per channel L | P5 Binary PGM | ✅ | ✅ |
| 16 bits per channel L | P2 ASCII PGM | ✅ | ✅ |
| 8 bits per channel L | P5 Binary PGM | ✅ | ✅ |
| 8 bits per channel L | P2 ASCII PGM | ✅ | ✅ |
| 1 bit ink on/off | P4 Binary PBM | ✅ | ❌ |
| 1 bit ink on/off | P1 ASCII PBM | ✅ | ❌ |

## Python compatibility

Current version of PyPNM was successfully tested with Python 3.10 and above. However, there is also a [Python 3.4 compatible PyPNM version](https://github.com/Dnyarri/PyPNM/tree/py34/), proven to work with Python 3.4 under Windows XP.

## Target image representation

Main goal of module under discussion is not just bytes reading and writing but representing image as some logically organized structure for further image editing.

Is seems logical to represent an RGB image as nested 3D structure - (X, Y)-sized matrix of three-component RGB vectors. Since in Python list seem to be about the only variant for mutable structures like that, it is suitable to represent image as `list(list(list(int)))` structure. Therefore, it would be convenient to have module read/write image data to/from such a structure.

Note that for L images memory structure is still `list(list(list(int)))`, with innermost list having only one component, thus enabling further image editing with the same nested Y, X, Z loop regardless of color mode.

Note that for the same reason when reading 1 bit PBM files into image this module promotes data to 8 bit L, inverting values and multiplying by 255, so that source 1 (ink on) is changed to 0 (black), and source 0 (ink off) is changed to 255 (white).

## Installation

In case of installing using pip:

`pip install PyPNM`

then in your program import section:

`from pypnm import pnmlpnm`

then use functions as described in section *"pnmlpnm.py functions"* below.

In case you downloaded file **pnmlpnm.py** from Github or somewhere else as plain .py file and not a package, simply put this file into your program folder, then use `import pnmlpnm`.

## pnmlpnm.py

Module file **pnmlpnm.py** contains 100% pure Python implementation of everything one may need to read/write a variety of PGM and PPM files. I/O functions are written as functions/procedures, as simple as possible, and listed below:

- **pnm2list**  - reading binary or ascii RGB PPM or L PGM file and returning image data as nested list of int.
- **list2bin**  - getting image data as nested list of int and creating binary PPM (P6) or PGM (P5) data structure in memory. Suitable for generating data to display with Tkinter.
- **list2pnm**  - getting image data as nested list of int and writing binary PPM (P6) or PGM (P5) file.
- **list2pnmascii** - alternative function to write ASCII PPM (P3) or PGM (P2) files.
- **create_image** - creating empty nested 3D list for image representation. Not used within this particular module but often needed by programs this module is supposed to be used with.

Detailed functions arguments description is provided below as well as in docstrings.

### pnm2list

`X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(in_filename)`

read data from PPM/PGM file to nested image data list, where:

- `X, Y, Z`   - image sizes (int);
- `maxcolors` - number of colors per channel for current image (int);
- `image3D`   - image pixel data as list(list(list(int)));
- `in_filename` - PPM/PGM file name (str).

### list2bin

`image_bytes = pnmlpnm.list2bin(image3D, maxcolors, show_chessboard)`

Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `show_chessboard` - optional bool, set `True` to show LA and RGBA images against chessboard pattern; `False` or missing show existing L or RGB data for transparent areas as opaque. Default is `False` for backward compatibility;
- `image_bytes` - PNM-structured binary data.

`image_bytes` object thus obtained is well compatible with Tkinter `PhotoImage(data=...)` method and therefore may be used to (and actually was developed for) visualize any data represented as image-like 3D list.

> [!NOTE]
> When encountering image list with 2 or 4 channels, current version of `list2bin` may treat it as LA or RGBA image correspondingly, and generate image preview for Tkinter as transparent over chessboard background (like Photoshop or GIMP). Since PNM images do not have transparency, this preview is actually either L or RGB, with image mixed with chessboard background, generated by `list2bin` (pattern settings match Photoshop "Light Medium" defaults). This behaviour is controlled by `show_chessboard` option. Default setting is `False` (meaning simply skipping alpha channel) for backward compatibility.
Note that Tkinter used for Python 3.10 displays some hight-color images incorrectly; this was entirely a Tkinter problem, fixed with Python 3.11 release.

### list2pnm

`pnmlpnm.list2pnm(out_filename, image3D, maxcolors)`

Write PGM P5 or PPM P6 (binary) file from nested image data list, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `out_filename` - PNM file name.

### list2pnmascii

`pnmlpnm.list2pnmascii(out_filename, image3D, maxcolors)` where:

Write PGM P2 or PPM P3 (ASCII text) file from nested image data list, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `out_filename` - PNM file name.

### create_image

`image3D = create_image(X, Y, Z)`

Create empty 3D nested list of `X*Y*Z` sizes.

## viewer.py

Program **viewer.py** is a small illustrative utility: using *pnmlpnm* package, it reads different flavours of PGM and PPM files, and allows saving them as different types of PGM/PNM, i.e. it can read ascii PPM and write it as binary PPM or vs. Also this program shows images using *pnmlpnm* and Tkinter. No, there is no mistake: it does not feed PPM files to Tkinter directly. Instead, it uses nested 3D list data loaded using *pnmlpnm* to generate in-memory bytes object of PPM structure using `preview_data = pnmlpnm.list2bin(image3D, maxcolors)`, and then feeds this in-memory bytes object to Tkinter as `preview = PhotoImage(data=preview_data)` (note using *data=*, not *file=*). This way it shows, for example, ascii PPM which Tkinter itself cannot handle.

[![Example of ascii ppm opened in viewer.py and converted to binary ppm on the fly to be rendered with Tkinter](https://dnyarri.github.io/pypnm/viewer.png)](https://dnyarri.github.io/pypnm.html)

As a result, you may use *pnmlpnm* and Tkinter to visualize any data that can be represented as greyscale or RGB without huge external packages and writing files on disk; all you need is Tkinter, included into standard CPython distributions, and highly compatible pure Python *pnmlpnm.py* taking only 16 kbytes.

## References

1. [Netpbm file formats description](https://netpbm.sourceforge.net/doc/).

2. [PyPNM at PyPI](https://pypi.org/project/PyPNM/) - installing PyPN with `pip`. Does not contain viewer example etc., only core converter, but provides regular `pip`-driven automated updates.

3. [PyPNM at Github](https://github.com/Dnyarri/PyPNM/) containing example viewer application, illustrating using `list2bin` to produce data for Tkinter `PhotoImage(data=...)` to display, as well as opening/saving various portable map formats.

4. [PyPNM for Python 3.4 at Github](https://github.com/Dnyarri/PyPNM/tree/py34/) containing example viewer application, illustrating using `list2bin` to produce data for Tkinter `PhotoImage(data=...)` to display, as well as opening/saving various portable map formats. This particular version was tested and shown to work under Python 3.4, Windows XP. This particular distribution also contain [PyPNG](https://gitlab.com/drj11/pypng), providing universal pure Python viewer and converter for PNG and all flavour of PGM and PPM.

## Examples

1. [PixelArtScaling](https://github.com/Dnyarri/PixelArtScaling/) - usage example, pure Python image rescaling applications using Scale2x and Scale3x, PNG I/O is based on [PyPNG](https://gitlab.com/drj11/pypng), and PPM/PGM I/O - on  [PyPNM](https://pypi.org/project/PyPNM/), thus making everything pure Python and therefore cross-platform.

2. [POVRay Thread: Linen and Stitch](https://dnyarri.github.io/povthread.html) - usage example, contains image filtering application «Averager», implementing non-standard adaptive image averaging. Filter before/after preview based on statically linked PyPNM list2bin code and Tkinter `PhotoImage(data=...)` class. As a result, fully operational pure Python interactive image filtering application ensued.

## Home

[The Toad's Slimy Mudhole](https://dnyarri.github.io) - other Python freeware by the the same author, illustrated.
