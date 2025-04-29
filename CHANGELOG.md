# PyPNM

Pure Python module for PPM and PGM image files reading, displaying, and writing.

## Version

[Main version](https://github.com/Dnyarri/PyPNM/). Compatible with Python 3.10 and above.

## History

0.11.26.0   Initial working version 26 Nov 2024.
Version numbering: MAINVERSION.MMsinceJan2024.DD.BUILD.

1.12.14.1   [Public release at PyPI](https://pypi.org/project/PyPNM/).

1.13.09.0   Complete rewriting of `pnm2list` using `re` and `array`; PPM and PGM support rewritten.

1.13.10.5   Header pattern seem to comprise all problematic cases; PBM support rewritten.

1.14.08.12  File output rewritten to reduce memory usage; `list2pnm` per row, `list2pnmascii` per sample.

1.15.1.1    Rendering preview for LA and RGBA against chessboard added to `list2bin`,
controlled by optional `show_chessboard` bool added to arguments.
Default is `False` (i.e. simply ignoring alpha) for backward compatibility.
Improved robustness.

1.15.19.19  General branch shortening and more cleanup. Minor bogus stuff removed.
Yet another final version 😉

1.16.1.9    General cleanup, minor speedup.

1.16.29.19  Added `list2pnm` function, previous `list2pnm` renamed to `list2pnmbin`.
New `list2pnm` is a switch between `list2pnmbin` and `list2pnmascii`, controlled with `bin` bool; default is True that provides backward compatibility.
