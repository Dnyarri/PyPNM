# PyPNM

Pure Python module for PPM and PGM image files reading, displaying, and writing.

## Version

[Maximum compatibility version](https://github.com/Dnyarri/PyPNM/tree/py34/).
Successfully tested with Python 3.4 under Windows XP.

Note that this branch (`.34`) is functionally identical to, yet internally different from `main` branch.

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

1.15.1.34   Special build of 1.15.1.1 version, downgraded to Python 3.4
(f-strings replaced with concatenation, type hints removed, *etc.*); `.34` branch split from `main`
(versioning for this compatibility branch is MAINVERSION.MMsinceJan2024.DD.34)

1.16.1.34   General cleanup, concatenations replaced with join, minor speedup.

1.16.4.34   Bugfix.

1.16.12.34  Conditional branches shortened, some more RAM cleanup attempts.
