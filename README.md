
| 【EN】 | [〖RU〗](README.RU.md) |
| ---- | ---- |

# PyPNM - Pure Python PPM and PGM image files reading and writing module

> [!NOTE]
> This branch contains a special extended compatibility version of PyPNM, deliberately made to be compatible with old versions of Python 3.
>
> It was successfully tested with Python 3.4 under Windows XP 32 bit, and may probably work even with something more antique.

If you use Python 3.11 or above, it is highly recommended to switch to [**main** PyPNM branch](https://github.com/Dnyarri/PyPNM/tree/main/), where the newest main version is hanging.

> [!WARNING]
> THIS BRANCH IS NOT MEANT TO BE MERGED WITH ANY OTHERS!

## Overview and justification

PPM ([Portable Pixel Map](https://netpbm.sourceforge.net/doc/ppm.html)) and PGM ([Portable Gray Map](https://netpbm.sourceforge.net/doc/pgm.html)) (particular cases of PNM format group) are simplest file formats for RGB and L images, correspondingly. Paradoxically, this simplicity lead to some adverse consequences:

- lack of strict official specification. Instead, you may find words like "usual" in format description. Surely, there is someone who implement this part of image format in unprohibited, yet a totally unusual way.

- unwillingness of many software developers to provide any good support for simple and open format. It took years for almighty Adobe Photoshop developers to include PNM module in distribution rather than count on third-party developers, and surely (see above) they took their chance to implement a header scheme nobody else uses.

  What as to PNM support in Python, say, Pillow, it normally is rather incomplete or completely missing when it comes to 16 bits per channel modes, and requires special measures when some limited support exist.

As a result, novice Python user (like me) may find it difficult to get reliable input/output modules for PPM and PGM image formats.

## Objectives

1. Obtain suitable facility for visualization of image-like data (images first and foremost), existing in form of 3D nested lists, via Tkinter `PhotoImage(data=...)` method.

2. Obtain simple and compact cross-platform module for reading PPM and PGM files as 3D nested lists for further processing with Python, and subsequent writing of processed 3D nested lists data to PPM or PGM files.

To accomplish this, current PyPNM module was developed, combining input/output functions for 8-bits and 16-bits per channel binary and ASCII [Portable Gray Map](https://netpbm.sourceforge.net/doc/pgm.html) and [Portable Pixel Map](https://netpbm.sourceforge.net/doc/ppm.html) files, i.e. P2, P5, P3 and P6 PNM file types. All color depth ranges supported directly, without limitations and without dancing with tambourine and proclaiming it to be a novel method.

## Python compatibility

Current PyPNM version is maximal backward compatibility build. While most of the development was performed using Python 3.12, extensive testing with other versions was carried out, and PyPNM proven to work with antique **Python 3.4** ([reached end of life 18 Mar 2019](https://devguide.python.org/versions/)) under **Windows XP 32-bit** ([reached end of support 8 Apr 2014](https://learn.microsoft.com/en-us/lifecycle/products/windows-xp)).

> [!NOTE]
> Tkinter, bundled with standard CPython distributions 3.10 and below have problems with 16 bpc images. Although it's not PyPNM but Tkinter problem, it's still ungood and severely discombobulating. As a workaround, `list2bin` function in PyPNM extended compatibility version (.34) includes a routine for color depth reduction from 16 bpc to 8 bpc when generating a preview. Surely `list2bin` tries to avoid such a remapping unless it is absolutely necessary since remapping requires extra calculation and therefore slows the function down; decision on remapping, however, is based on correlation between Python version and bundled Tkinter version, and therefore may fail if you have custom builds of Tkinter, or Python, or both. Failure is most likely to manifest as unnecessary slowdowns, and least likely as Tkinter crash. Remember that this module is provided under Unlicense, I don't care much of my copyright, so you may edit the source, including Python version detection criteria, at will. Hint: Python versions is determined as `python_version_tuple()[1]`.
>
> On the other hand, if you have only new versions of Python and Tkinter, you may prefer downloading [Main version of PyPNM](https://github.com/Dnyarri/PyPNM), which doesn't have any backward compatibility fixes, and therefore doesn't waste CPU time on it.

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

Note that since main PyPNM purpose is facilitating image editing, when reading 1-bit PBM files into image this module promotes data to 8-bit L, inverting values and multiplying by 255, so that source 1 (ink on) is changed to 0 (black), and source 0 (ink off) is changed to 255 (white) - since any palette-based images, 1-bit included, are next to useless for general image processing (try to imagine 1-bit Gaussian blur, for example), and have to be converted to smooth color for that, conversion is performed by PyPNM automatically.

## Installation

In case of installing from PyPI via `pip`:

```console
python -m pip install --upgrade PyPNM
```

## Usage

Since version 2.26.22.34 recommended import is:

```python
import pypnm
```

then use functions as described in section [*"Functions description"*](#functions-description), or just take a look at [*"Usage example"*](#usage-example) section below.

Note that legacy import schemes like

```python
from pypnm import pnmlpnm
```

are still working.

## Usage example

Below is a minimal Python program, illustrating all PyPNM functions at once: reading PPM file (small collection of compatibility testing samples is included into current Git repository) to image nested list, writing image list to disk as binary PPM, writing image list as ASCII PPM, and displaying image list using Tkinter:

```python
#!/usr/bin/env python3

from tkinter import Button, PhotoImage, Tk

from pypnm import list2bin, list2pnm, pnm2list

X, Y, Z, maxcolors, image3D = pnm2list('example.ppm')  # Open "example.ppm"
list2pnm('binary.ppm', image3D, maxcolors, bin=True)  # Save as binary pnm
list2pnm('ASCII.ppm', image3D, maxcolors, bin=False)  # Save as ASCII pnm

main_window = Tk()
main_window.title('PyPNM demo')
preview_data = list2bin(image3D, maxcolors)  # Image list 🡢 preview bytes
preview = PhotoImage(data=preview_data)  # Preview bytes 🡢 PhotoImage object
preview_button = Button(main_window, text='Example\n(click to exit)', image=preview,
    compound='top', command=lambda: main_window.destroy())  # Showing PhotoImage
preview_button.pack()
main_window.mainloop()

```

With a fistful of code for widgets and events this simplistic program may be easily turned into a rather functional application (see [Viewer.py](#viewerpy) below).

## Functions description

PyPNM module contains 100% pure Python implementation of everything one may need to read and write a variety of PGM and PPM files, as well as to display corresponding image data. No non-standard dependencies used, no extra downloads needed, no dependency version conflicts expected. All the functionality is provided as functions/procedures, as simple as possible; main functions are listed below:

- **pnm2list**  - reading binary or ASCII RGB PPM or L PGM file and returning image data as nested list of int.
- **list2bin**  - getting image data as nested list of int and creating binary PPM (P6) or PGM (P5) data structure in memory. Suitable for generating data to display with Tkinter.
- **list2pnm** - getting image data as nested list of int and writing either binary or ASCII file depending on `bin` argument.

Detailed functions arguments description is provided below, as well as in module docstrings and [PyPNM documentation bedside book (PDF)](https://dnyarri.github.io/pypnm/pypnm.pdf).

### pnm2list

```python
X, Y, Z, maxcolors, image3D = pypnm.pnm2list(in_filename)
```

Read data from PPM/PGM file to nested image data list, where:

- `X, Y, Z`   - image sizes (int);
- `maxcolors` - number of colors per channel for current image (int);
- `image3D`   - image pixel data as list(list(list(int)));
- `in_filename` - PPM/PGM file name (str).

### list2bin

```python
image_bytes = pypnm.list2bin(image3D, maxcolors, show_chessboard)
```

Convert nested image data list to PGM P5 or PPM P6 (binary) data structure in memory, where:

- `image3D`   - `Y * X * Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `show_chessboard` - optional bool, set `True` to show LA and RGBA images against chessboard pattern; `False` or missing show existing L or RGB data for transparent areas as opaque.

   Default is `False` for backward compatibility;

- `image_bytes` - PNM-structured binary data.

`image_bytes` object thus obtained is well compatible with Tkinter `PhotoImage(data=...)` method and therefore may be used to (and actually was developed for) visualize any data represented as image-like 3D list.

> [!NOTE]
> When encountering image list with 2 or 4 channels, current version of `list2bin` may treat it as LA or RGBA image correspondingly, and generate image preview for Tkinter as transparent over chessboard background (like Photoshop or GIMP). Since PNM images do not have transparency, this preview is actually either L or RGB, with image mixed with chessboard background, generated by `list2bin` (pattern settings match Photoshop "Light Medium" defaults). This behaviour is controlled by `show_chessboard` option. Default setting is `False` (meaning simply skipping alpha channel) for backward compatibility.

### list2pnm

`pnmlpnm.list2pnm(out_filename, image3D, maxcolors, bin)`

Write either binary or ASCII file from nested image data list, where:

- `image3D`   - `Y*X*Z` list (image) of lists (rows) of lists (pixels) of ints (channels);
- `maxcolors` - number of colors per channel for current image (int);
- `bin` - switch defining whether to write binary file or ASCII (bool). Default is True, meaning binary output, to provide backward compatibility.
- `out_filename` - Name of PNM file to be written.

Note that `list2pnm`, is merely a switch between internal `list2pnmbin` and `list2pnmascii`, introduced for simplifying writing "Save as..." GUI dialog functions - now you can use one function for all PNM flavours, passing `bin` via lambda, is necessary.

## viewer.py

Program **viewer.py** is a small illustrative utility: using *pnmlpnm* package, it reads different flavours of PGM and PPM files, and allows saving them as different types of PGM/PNM, i.e. it can read ASCII PPM and write it as binary PPM or vs. Also this program shows images using *pnmlpnm* and Tkinter. No, there is no mistake: it does not feed PPM files to Tkinter directly. Instead, it uses nested 3D list data loaded using *pnmlpnm* to generate in-memory bytes object of PPM structure using `preview_data = pnmlpnm.list2bin(image3D, maxcolors)`, and then feeds this in-memory bytes object to Tkinter as `preview = PhotoImage(data=preview_data)` (note using *data=*, not *file=*). This way it displays, for example, ASCII PPM and PGM which Tkinter itself cannot handle.

| Fig. 1. *Example of ASCII PPM opened in viewer.py* |
| :---: |
| [![Example of ASCII ppm opened in viewer.py and converted to binary ppm on the fly to be rendered with Tkinter](https://dnyarri.github.io/pypnm/viewer34.png "Example of ASCII ppm opened in viewer.py and converted to binary ppm on the fly to be rendered with Tkinter")](https://dnyarri.github.io/pypnm.htm "PyPNM page with explanations") |

Beside having simple yet fully functional GUI with mouse events handling a-la Photoshop, *viewer.py* is also capable to process command line arguments like

```python
py -3.4 viewer.py filename.ppm
```

for opening files. In theory, you may even register it as system viewer for PPM, PGM and PBM files.

## Conclusion

Using *PyPNM* and Tkinter you may easily visualize any data that can be represented as greyscale or RGB images (images first and foremost), without large external packages and writing files on disk. Nested list data structures used by PyPNM are well suited for nested loop/map image processing.

## References

1. [Netpbm file formats specifications](https://netpbm.sourceforge.net/doc/ "Original specifications for PPM, PGM and PBM files formats") strictly followed in the course of PyPNM development.

2. [PyPNM at PyPI](https://pypi.org/project/PyPNM/ "Pure Python PNM reading, displaying and writing module for Python >= 3.4") - installing PyPN with `pip`. Does not contain viewer example etc., only core converter module, but provides regular `pip`-driven automated updates.

3. [PyPNM at Github](https://github.com/Dnyarri/PyPNM/ "Pure Python PNM reading, displaying and writing module for Python >= 3.11") containing both PyPNM module and example viewer application, illustrating using `list2bin` to produce data for Tkinter `PhotoImage(data=...)` to display, as well as opening/saving various portable map formats.

4. [PyPNM ver *.34 at Github](https://github.com/Dnyarri/PyPNM/tree/py34 "Pure Python PNM reading, displaying and writing module for Python >= 3.4") - same as [3] above, but compatible with Python 3.4.

5. [PyPNM docs (PDF)](https://dnyarri.github.io/pypnm/pypnm.pdf "PyPNM docs (PDF)"). While current documentation was written for 9 May 2025 "Victory" version, it remains valid for 2 Sep 2025 "Victory II" release since the latter involves total inner optimization without changing input/output format.

## Examples

[**PixelArtScaling**](https://dnyarri.github.io/scalenx.html "Scale2x, Scale3x, Scale2xSFX and Scale3xSFX in pure Python") - usage example, pure Python implementation of Scale2x, Scale3x, Scale2xSFX and Scale3xSFX image rescaling methods. Since ScaleNx methods are based on whole pixel comparison, image representation as nested list, provided by PyPNM, perfectly fits ScaleNx module algorithm. In main programs PNG I/O is based on [PyPNG](https://gitlab.com/drj11/pypng "Pure Python PNG reading and writing module"), on-screen preview and PPM/PGM I/O - on [PyPNM](https://pypi.org/project/PyPNM/ "Pure Python PNM reading, displaying and writing module"), thus making entire project pure Python and therefore cross-platform.

[**Averager**](https://dnyarri.github.io/povthread.html#averager "Pure Python image filtering application, largely based on PyPNM"), non-standard adaptive image average filtering application, written entirely in Python.

| Fig. 2. *Pure Python image filtering application, largely based on PyPNM* |
| :---: |
| [![Pure Python image adaptive averaging application, largely based on PyPNM](https://dnyarri.github.io/thread/ave.png "Pure Python image filtering application, largely based on PyPNM")](https://dnyarri.github.io/povthread.html#averager "Pure Python image filtering application, largely based on PyPNM") |

Filter before/after preview based on PyPNM `list2bin` code and Tkinter `PhotoImage(data=...)` class. Filtering itself largely utilize the fact that nested lists, produced by PyPNM, may be easily processed with one-loop-fits-all algorithms regardless of color mode. As a result, fully operational pure Python interactive image filtering application ensued.

[**imin** Bilinear and barycentric image interpolation module](https://dnyarri.github.io/imin.html "Bilinear and barycentric image interpolation, main applications are largely based on PyPNM"), written entirely in Python. Sample applications are largely based on PyPNM.

| Fig. 3. *Pure Python image displacing/distorting application, largely based on PyPNM* |
| :---: |
| [![Pure Python image displacing and deformation application, largely based on PyPNM](https://dnyarri.github.io/imin/anigui.png "Pure Python image filtering application, largely based on PyPNM")](https://dnyarri.github.io/imin.html "Pure Python image filtering application, largely based on PyPNM") |

As with "Averager" above, the module itself utilizes the fact that pixels represented as nested lists, produced by PyPNM, are easy to process using the same `map()` for any color mode.

---

[Dnyarri website - more Python freeware for image processing, 3D, and batch automation](https://dnyarri.github.io "The Toad's Slimy Mudhole - Python freeware for POV-Ray and other 3D, Scale2x, Scale3x, Scale2xSFX, Scale3xSFX, PPM and PGM image support, bilinear and barycentric image interpolation, and batch processing") by the same author.
