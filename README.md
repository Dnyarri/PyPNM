
| [EN] | [RU](README.RU.md) |
| ---- | ---- |

# PyPNM - Pure Python PPM and PGM image files reading and writing module

## Overview and justification

PPM and PGM (particular cases of PNM format group) are simplest file formats for RGB and L images, correspondingly. Paradoxically, this simplicity lead to some adverse consequences:

- lack of strict official specification. Instead, you may find words like "usual" in format description. Surely, there is someone who implement this part of image format in unprohibited, yet a totally unusual way.

- unwillingness of many software developers to provide any good support to for simple and open format. It took years for almighty Adobe Photoshop developers to include PNM module in distribution rather than count on third-party developers, and surely (see above) they used this chance to implement a separator scheme nobody else uses. What as to PNM support in Python, say, Pillow... sorry, I promised not to mention Pillow anywhere ladies and children are allowed to read it.

As a result, novice Python user (like me) may find it difficult to get reliable input/output modules for PPM and PGM image formats; therefore current PyPNM module was developed, combining input/output functions for 8-bits and 16-bits per channel binary and ascii [Portable Gray Map](https://netpbm.sourceforge.net/doc/pgm.html) and [Portable Pixel Map](https://netpbm.sourceforge.net/doc/ppm.html) files, i.e. P2, P5, P3 and P6 PNM file types. Both greyscale and RGB with 16-bit per channel color depth (0...65535 range) are supported directly, without limitations and without dancing with tambourine and proclaiming it to be a novel method.

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
- **list2pnm**  - writing data created with list2bin to file.
- **list2pnmascii** - alternative function to write ASCII PPM (P3) or PGM (P2) files.
- **create_image** - creating empty nested 3D list for image representation. Not used within this particular module but often needed by programs this module is supposed to be used with.

Detailed functions arguments description is provided below as well as in docstrings.

### pnm2list

`X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(in_filename)`

read data from PPM/PGM file, where:

- `X, Y, Z`   - image sizes (int);
- `maxcolors` - number of colors per channel for current image (int);
- `image3D`   - image pixel data as list(list(list(int)));
- `in_filename` - PPM/PGM file name (str).

### list2bin

`image_bytes = pnmlpnm.list2bin(image3D, maxcolors)`

Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `image_bytes` - PNM-structured binary data.

### list2pnm

`pnmlpnm.list2pnm(out_filename, image3D, maxcolors)` where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `out_filename` - PNM file name.

### list2pnmascii

Similar to `list2pnm` above but creates ascii pnm file instead of binary.

`pnmlpnm.list2pnmascii(out_filename, image3D, maxcolors)` where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `out_filename` - PNM file name.

### create_image

Create empty 3D nested list of `X*Y*Z` sizes.

## viewer.py

Program **viewer.py** is a small illustrative utility: using *pnmlpnm* package, it reads different flavours of PGM and PPM files, and allows saving them as different types of PGM/PNM, i.e. it can read ascii PPM and write it as binary PPM or vs. Also this program shows images using *pnmlpnm* and Tkinter. No, there is no mistake: it does not feed PPM files to Tkinter directly. Instead, it uses nested 3D list data loaded using *pnmlpnm* to generate in-memory bytes object of PPM structure using `preview_data = pnmlpnm.list2bin(image3D, maxcolors)`, and then feeds this in-memory bytes object to Tkinter as `preview = PhotoImage(data=preview_data)` (note using *data=*, not *file=*). This way it shows, for example, ascii PPM which Tkinter itself cannot handle.

[![Example of ascii ppm opened in viewer.py and converted to binary ppm on the fly to be rendered with Tkinter](https://dnyarri.github.io/pypnm/viewer.png)](https://dnyarri.github.io/pypnm.html)

As a result, you may use *pnmlpnm* and Tkinter to visualize any data that can be represented as greyscale or RGB without huge external packages and writing files on disk; all you need is Tkinter, included into standard CPython distributions, and highly compatible pure Python *pnmlpnm.py* taking only 16 kbytes.

## References

1. [Netpbm file formats description](https://netpbm.sourceforge.net/doc/).

2. [PyPNM at PyPI](https://pypi.org/project/PyPNM/) - installing PyPN with `pip`. Does not contain viewer example etc., only core converter, but provides regular `pip`-driven automated updates.

3. [PyPNM at Github](https://github.com/Dnyarri/PyPNM/) containing example viewer application, illustrating using `list2bin` to produce data for Tkinter `PhotoImage(data=...)` to display, as well as opening/saving various portable map formats.

4. [PixelArtScaling](https://github.com/Dnyarri/PixelArtScaling/) - usage example, pure Python image rescaling applications using Scale2x and Scale3x, PNG I/O is based on [PyPNG](https://gitlab.com/drj11/pypng), and PPM/PGM I/O - on  [PyPNM](https://pypi.org/project/PyPNM/), thus making everything pure Python and therefore cross-platform.

5. [POVRay Thread: Linen and Stitch](https://dnyarri.github.io/povthread.html) - usage example, contains image filtering application «Averager», implementing non-standard adaptive image averaging. Filter before/after preview based on statically linked PyPNM list2bin code and Tkinter `PhotoImage(data=...)` class. As a result, fully operational pure Python interactive image filtering application ensued.
