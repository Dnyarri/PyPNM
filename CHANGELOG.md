# PyPNM

Pure Python module for PPM and PGM image files reading, displaying, and writing.

## Version

[PyPNM Maximum compatibility version](https://github.com/Dnyarri/PyPNM/tree/py34/ "PyPNM for Python 3.4 and above").
Successfully tested with Python 3.4 under Windows XP.

Note that this branch ([`.34`](https://github.com/Dnyarri/PyPNM/tree/py34/ "PyPNM for Python 3.4 and above")) is functionally identical to, yet internally different from [`main`](https://github.com/Dnyarri/PyPNM/ "PyPNM for Python 3.11 and above") branch.

## History

Current versioning for this branch is MAINVERSION.MMsinceJan2024.DD.34.

### Version 2

| Version | Date | Major changes |
| :---- | :---- | :---- |
| 2.29.19.34 | 18 May 2026 | Changed preview bitdepth reduction code for old Tkinter (18 May 2026). |
| 2.26.26.34 | 27 Feb 2026 | Minor changes to chessboard rendering. |
| 2.26.22.34 | 23 Feb 2026 | Introduced more suitable import pattern, like `from pypnm import list2bin, list2pnm, pnm2list` |
| 2.21.3.4.post5 | 31 Dec 2025 | Compatibility list extended. |
| 2.21.3.4.post4 | 23 Nov 2025 | Even more developer-friendly docstrings. |
| 2.21.3.4.post3 | 12 Nov 2025 | More ReST-compliant docstrings. |
| 2.21.3.4 | 3 Sep 2025 | "Victory II" update mostly consist of more friendly help. |
| 2.21.2.34 | **2 Sep 2025** | "**Victory II**": substantial changes aimed to save resources:<br>- `mmap` introduced for reading to remove intermediates of `re`.<br>- generators are widely used for writing.<br>Module input/output remains the same as for 1.17.9.34 "Victory". |

### Version 1

- 1.12.14.1     [Public release at PyPI](https://pypi.org/project/PyPNM/).
- 1.13.09.0     Complete rewriting of `pnm2list` using `re` and `array`; PPM and PGM support rewritten.
- 1.13.10.5     Header pattern seem to comprise all problematic cases; PBM support rewritten.
- 1.14.08.12    File output rewritten to reduce memory usage; `list2pnm` per row, `list2pnmascii` per sample.
- 1.15.1.1      Rendering preview for LA and RGBA against chessboard added to `list2bin`,
controlled by optional `show_chessboard` bool added to arguments.
Default is `False` (i.e. simply ignoring alpha) for backward compatibility.
Improved robustness.
- 1.15.1.34     Special build of 1.15.1.1 version, downgraded to Python 3.4
(f-strings replaced with concatenation, type hints removed, *etc.*); `.34` branch split from `main`
(versioning for this compatibility branch is MAINVERSION.MMsinceJan2024.DD.34)
- 1.16.1.34     General cleanup, concatenations replaced with join, minor speedup.
- 1.16.12.34    Conditional branches shortened, some more RAM cleanup attempts.
- 1.17.1.34     1 May 2025 "Mayday": Added `list2pnm` function, previous `list2pnm` renamed to `list2pnmbin`.
New `list2pnm` is a switch between `list2pnmbin` and `list2pnmascii`, controlled with `bin` bool; default is True that provides backward compatibility.
- 1.17.9.34     **9 May** 2025 "**Victory**": Forced 8-bit output for `list2bin` under old Python. Some optimizations.
[PyPNM 1.17.9.34.post2 "Victory"](https://pypi.org/project/PyPNM/1.17.9.34.post2/) will be the last one in ver. 1 series.

## Prehistory

0.11.26.0   Initial working version 26 Nov 2024.

Version numbering: MAINVERSION.MMsinceJan2024.DD.BUILD.
