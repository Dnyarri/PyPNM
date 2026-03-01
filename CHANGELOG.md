# PyPNM

Pure Python module for PPM and PGM image files reading, displaying, and writing.

## Version

[PyPNM Main version](https://github.com/Dnyarri/PyPNM/), compatible with Python 3.11 and above.

## History

### Version 2

| Version | Major changes |
| :--- | :--- |
| 2.26.27.312 | Minor changes to chessboard rendering. |
| 2.26.23.23 | More suitable import scheme like `from pypnm import list2bin, list2pnm, pnm2list` |
| 2.23.23.23 | Even more developer-friendly docstrings. |
| 2.23.13.13 | ReST-compliant docstrings. |
| 2.21.3.12 | **3 Sep 2025** "**Victory II**" update mostly consist of more friendly help. |
| 2.21.2.2 | **2 Sep 2025** "**Victory II**" release: substantial changes aimed to save resources:<br>- for reading, `mmap` introduced to remove intermediates of `re`.<br>- for writing, generators are widely used.<br>Module input/output structure remains the same as for 1.17.9.34 "Victory". |

### Version 1

| Version | Major changes |
| :--- | :--- |
| 1.17.9.1 | **9 May 2025 "Victory"** release: Optimizations. |
| 1.17.1.1 | 1 May 2025 "Mayday": Added `list2pnm` function, previous `list2pnm` renamed to `list2pnmbin`. New `list2pnm` is a switch between `list2pnmbin` and `list2pnmascii`, controlled with `bin` bool; default is True that provides backward compatibility. |
| 1.16.1.9 | General cleanup, minor speedup. |
| 1.15.19.19 | General branch shortening and more cleanup. Minor bogus stuff removed. Yet another final version 😉 |
| 1.15.1.1 | Rendering preview for LA and RGBA against chessboard added to `list2bin`, controlled by optional `show_chessboard` bool added to arguments. Default is `False` (i.e. simply ignoring alpha) for backward compatibility. Improved robustness. |
| 1.14.08.12 | File output rewritten to reduce memory usage; `list2pnm` per row, `list2pnmascii` per sample. |
| 1.13.10.5 | Header pattern seem to comprise all problematic cases; PBM support rewritten. |
| 1.13.09.0 | Complete rewriting of `pnm2list` using `re` and `array`; PPM and PGM support rewritten. |
| 1.12.14.1 | [Public release at PyPI](https://pypi.org/project/PyPNM/). |

## Prehistory

0.11.26.0   Initial working version 26 Nov 2024. Version numbering: MAINVERSION.MMsinceJan2024.DD.BUILD (*i.e.*, \*.13 is Jan 2025, \*.25 is Jan 2026 *etc.*)
