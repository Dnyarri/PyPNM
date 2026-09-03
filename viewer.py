#!/usr/bin/env python3

"""Test shell for `PyPNM for Python >= 3.11`_ module - a Tkinter-based viewer.

Viewer does not use PNM file directly to display it with Tkinter
``PhotoImage(file=...)`` - instead, it loads image file, then constructs
PNM-like bytes data object in memory, and then displays it using Tkinter
``PhotoImage(data=...)``.
For example, it's able to display ASCII PGM and PPM, not supported by Tkinter,
since it recodes them to binary on the fly.

NOTE:

This is special developer edition, including PNG support with `PyPNG`_.,
and equipped with debug window, added deliberately to check data structures.

.. _PyPNM for Python >= 3.11: https://github.com/Dnyarri/PyPNM

.. _PyPNG: https://gitlab.com/drj11/pypng

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2.33.3.8.dev1'  # 3 Sep 2026
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from pathlib import Path
from platform import python_version, python_version_tuple
from sys import argv
from time import localtime, strftime  # Used to show file info only
from tkinter import BooleanVar, Button, Canvas, Frame, Label, Menu, PhotoImage, Tk, Toplevel
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo
from tkinter.scrolledtext import ScrolledText

import pypng
import pypnm

""" ╔══════════════════════════════════╗
    ║ GUI events and functions thereof ║
    ╚══════════════════════════════════╝ """


def DisMiss(event=None) -> None:
    """Kill dialog and continue."""

    sortir.destroy()


def ShallPass() -> None:

    pass


def PopUnpopDebug() -> None:
    """Pop or hide debug window depending on `pop_debug` value."""

    if pop_debug.get():
        insecticide.deiconify()
        insecticide.lower(sortir)
    else:
        insecticide.iconify()


def UINormal() -> None:
    """Normal UI state."""

    zanyato.config(state='normal', cursor='')
    sortir.update()


def UIBusy() -> None:
    """Busy UI state."""

    zanyato.config(state='disabled', cursor='watch')
    sortir.update()


def ShowMenu(event) -> None:
    """Pop menu up (or sort of drop it down)."""

    menu01.post(event.x_root, event.y_root)


def ShowInfo(event=None) -> None:
    """Show program and module version, and image info."""

    file_size = Path(sourcefilename).stat().st_size
    file_size_str = f'{file_size / 1048576:.2f} Mb' if (file_size > 1048576) else f'{file_size / 1024:.2f} Kb' if (file_size > 1024) else f'{file_size} bytes'
    creation_str = strftime('%d %B %Y %H:%M:%S', localtime(Path(sourcefilename).stat().st_ctime)) if int(python_version_tuple()[1]) < 12 else strftime('%d %B %Y %H:%M:%S', localtime(Path(sourcefilename).stat().st_birthtime))
    modification_str = strftime('%d %B %Y %H:%M:%S', localtime(Path(sourcefilename).stat().st_mtime))
    showinfo(
        title='General information',
        message=f'PNMViewer ver. {__version__}\nPython: {python_version()}\nModules:\n{pypnm.__name__} ver. {pypnm.__version__}',
        detail=f'File properties:\n{sourcefilename}\nSize: {file_size_str}\nCreated:  {creation_str}\nModified: {modification_str}\n\nImage properties:\nWidth: {X} px\nHeight: {Y} px\nChannels: {Z} channel{"s" if Z > 1 else ""}\nColor depth: {maxcolors + 1} gradations/channel',
    )


def GetSource(event=None) -> None:
    """Open source image and redefine other controls state."""

    global zoom_factor, zoom_do, zoom_show, preview, preview_data
    global X, Y, Z, maxcolors, image3D, info, sourcefilename, filename_from_command

    zoom_factor = 0

    # ↓ Trying to receive file name from command line, if None, opening GUI
    if filename_from_command is None:
        sourcefilename = askopenfilename(
            title='Open image file',
            filetypes=[
                ('Supported formats', '.png .ppm .pgm .pbm .pnm'),
                ('Portable network graphics', '.png'),
                ('Portable any map', '.ppm .pgm .pbm .pnm'),
            ],
        )
        if sourcefilename == '':
            return
    else:
        sourcefilename = filename_from_command
        filename_from_command = None  # Removing file name after first open

    UIBusy()

    # ↓ Loading file, converting data to list.
    #   NOTE: maxcolors, image3D, info are GLOBALS!
    #   They are used during save!
    tuplevel = 'image'
    if Path(sourcefilename).suffix.lower() == '.png':
        X, Y, Z, maxcolors, image3D, info = pypng.png2list(sourcefilename, tuplevel)

    elif Path(sourcefilename).suffix.lower() in ('.ppm', '.pgm', '.pbm', '.pnm'):
        X, Y, Z, maxcolors, image3D = pypnm.pnm2list(sourcefilename, tuplevel)
        # ↓ Creating dummy info, containing bpc value required to Save As PNG properly
        info = {'bitdepth': 16} if maxcolors > 255 else {'bitdepth': 8}
    else:
        raise ValueError('Extension not recognized')

    # ↓ Updating debug text
    pogovorit.insert('end', f'\n{sourcefilename=}\n{X=} {Y=} {Z=} {maxcolors=} {tuplevel=}\n')
    if X * Y < 16 * 16 + 1:
        pogovorit.insert('end', f'{image3D}\n')
    else:
        if tuplevel in ('image', 'pixel'):
            divider = ' ('
        else:
            divider = ' ['
        example = (str(image3D)[0 : ((16 * 16) * Z)]).rpartition(divider)[0]
        pogovorit.insert('end', f'\nImage too big, printing just a beginning:\n{example} ...\n')
    pogovorit.see('end')
    # ↓ Showing debug window if option set in menu
    PopUnpopDebug()

    # ↓ Converting list to bytes of PPM-like structure "preview_data" in memory
    preview_data = pypnm.list2bin(image3D, maxcolors, show_chessboard=True)
    pogovorit.insert('end', f'\nPreview bytes beginning:\n{str(preview_data)[0:256]} ...\n')
    pogovorit.see('end')
    # ↓ Now showing "preview_data" bytes using Tkinter
    preview = PhotoImage(data=preview_data)
    # ↓ Adding filename to window title a-la Photoshop
    sortir.title(f'PNMViewer: {Path(sourcefilename).name}')
    # ↓ Dictionary of zoom label texts
    zoom_show = {
        -4: 'Zoom 1:5',
        -3: 'Zoom 1:4',
        -2: 'Zoom 1:3',
        -1: 'Zoom 1:2',
        0: 'Zoom 1:1',
        1: 'Zoom 2:1',
        2: 'Zoom 3:1',
        3: 'Zoom 4:1',
        4: 'Zoom 5:1',
    }
    # ↓ Dictionary of zoom functions, corresponding to "zoom_show" above
    zoom_do = {
        -4: preview.subsample(5, 5),
        -3: preview.subsample(4, 4),
        -2: preview.subsample(3, 3),
        -1: preview.subsample(2, 2),
        0: preview,  # 1:1
        1: preview.zoom(2, 2),
        2: preview.zoom(3, 3),
        3: preview.zoom(4, 4),
        4: preview.zoom(5, 5),
    }

    # ↓ attempt to calculate zoom to fit
    #   GUI extra = 16 px
    screen_width, screen_height = sortir.winfo_screenwidth(), sortir.winfo_screenheight()
    if (preview.width() + 16) > screen_width or (preview.height() + frame_zoom.winfo_reqheight() + 16) > screen_height:
        zoom_factor = max(-(max((preview.width() + 16) // screen_width, (preview.height() + frame_zoom.winfo_reqheight() + 16) // screen_height)), minizoom)

    preview = zoom_do[zoom_factor]
    # ↓ Sizes of preview to fit the screen
    preview_width, preview_height = min(preview.width(), 8 * sortir.winfo_screenwidth() // 10), min(preview.height(), (8 * sortir.winfo_screenheight() // 10) - frame_zoom.winfo_height())

    zanyato.config(
        image=preview,
        compound='none',
        borderwidth=1,
        background=zanyato.master['background'],
    )
    canvas.config(
        width=preview_width,
        height=preview_height,  # Note that 'scrollregion' may be bigger than canvas!
        scrollregion=(0, 0, preview.width(), preview.height()),
        cursor='arrow',
    )
    canvas.itemconfig(  # configuring 'zanyato' size in a normal way doesn't work on canvas
        zanyato_,
        width=preview.width(),
        height=preview.height(),
    )

    # ↓ Binding preview
    zanyato.bind('<Motion>', canvasCoord)  # tracking cursor coords for possible drag
    zanyato.bind('<B1-Motion>', canvasDrag)  # mouse drag
    zanyato.bind('<ButtonRelease-1>', lambda event: canvas.config(cursor='arrow'))  # cursor back after drag
    zanyato.bind('<Control-Button-1>', zoomIn)  # Ctrl + left click
    zanyato.bind('<Double-Control-Button-1>', zoomIn)  # Ctrl + left click too fast
    zanyato.bind('<Control-+>', zoomIn)
    zanyato.bind('<Control-=>', zoomIn)
    zanyato.bind('<Alt-Button-1>', zoomOut)  # Alt + left click
    zanyato.bind('<Double-Alt-Button-1>', zoomOut)  # Alt + left click too fast
    zanyato.bind('<Control-minus>', zoomOut)
    sortir.bind_all('<MouseWheel>', zoomWheel)  # Wheel
    zanyato.bind('<Control-Key-1>', zoomOne)
    zanyato.bind('<Control-Alt-Key-0>', zoomOne)
    sortir.bind_all('<Control-i>', ShowInfo)
    # ↓ enabling zoom buttons
    butt_plus.config(state='normal', cursor='hand2')
    butt_minus.config(state='normal', cursor='hand2')
    # ↓ updating zoom label display
    label_zoom.config(text=zoom_show[zoom_factor])
    # ↓ enabling "Save as..."
    menu01.entryconfig('Save binary PNM...', state='normal')  # Instead of name numbers from 0 may be used
    menu01.entryconfig('Save ASCII PNM...', state='normal')
    menu01.entryconfig('Save PNG...', state='normal')
    menu01.entryconfig('Info', state='normal')
    UINormal()
    fit_width, fit_height = min(sortir.winfo_reqwidth(), 9 * sortir.winfo_screenwidth() // 10), min(sortir.winfo_reqheight(), 9 * sortir.winfo_screenheight() // 10)
    sortir.minsize(fit_width, fit_height)
    sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_reqwidth()) // 2}+64')
    zanyato.focus_set()  # Required for some binding to work


def SaveAsPNM(bin: bool) -> None:
    """Once pressed on any of Save PNM."""

    global sourcefilename

    # ↓ Adjusting "Save to" formats to be displayed according to channel number
    if Z < 3:
        format = [('Portable grey map', '.pgm')]
        extension = '.pgm'
        filetype = 'pgm'
    else:
        format = [('Portable pixel map', '.ppm')]
        extension = '.ppm'
        filetype = 'ppm'

    # ↓ Figuring out suggested file name based on saving in source/different format
    if Path(sourcefilename).suffix.lower() in ('.ppm', '.pgm', '.pnm'):
        proposed_name = Path(sourcefilename).stem + f' copy.{filetype}'
    else:
        proposed_name = Path(sourcefilename).stem + f'.{filetype}'

    # ↓ Open "Save as..." file
    savefilename = asksaveasfilename(
        title=f'Save {"binary" if bin else "ASCII"} {filetype.upper()} file',
        filetypes=format,
        defaultextension=extension,
        initialdir=Path(sourcefilename).parent,
        initialfile=proposed_name,
    )
    if savefilename == '':
        return

    # ↓ Saving "savefilename" in PNM format depending on "bin"
    UIBusy()
    pypnm.list2pnm(savefilename, image3D, maxcolors, bin)
    # ↓ Saved file becomes source file
    sourcefilename = savefilename
    sortir.title(f'PNMViewer: {Path(sourcefilename).name}')
    UINormal()


def SaveAsPNG() -> None:
    """Once pressed on Save PNG."""

    global sourcefilename

    # ↓ Figuring out suggested file name based on saving in source/different format
    if Path(sourcefilename).suffix.lower() == '.png':
        proposed_name = Path(sourcefilename).stem + ' copy.png'
    else:
        proposed_name = Path(sourcefilename).stem + '.png'

    # ↓ Open "Save as..." file
    savefilename = asksaveasfilename(
        title='Save PNG file',
        filetypes=[('Portable network graphics', '.png')],
        defaultextension='.png',
        initialdir=Path(sourcefilename).parent,
        initialfile=proposed_name,
    )
    if savefilename == '':
        return

    # ↓ Feeding list to PyPNG via pnglpng
    UIBusy()
    pypng.list2png(savefilename, image3D, info)
    # ↓ Saved file becomes source file
    sourcefilename = savefilename
    sortir.title(f'PNMViewer: {Path(sourcefilename).name}')
    UINormal()


def zoomIn(event=None) -> None:
    """Zoom preview in."""

    global zoom_factor, preview

    zoom_factor = min(zoom_factor + 1, maxizoom)
    preview = zoom_do[zoom_factor]
    zanyato.config(
        image=preview,
        compound='none',
    )
    # ↓ Sizes of preview to fit the screen
    preview_width, preview_height = min(preview.width(), 8 * sortir.winfo_screenwidth() // 10), min(preview.height(), (8 * sortir.winfo_screenheight() // 10) - frame_zoom.winfo_height())
    canvas.config(
        width=preview_width,
        height=preview_height,  # Note that 'scrollregion' may be bigger than canvas!
        scrollregion=(0, 0, preview.width(), preview.height()),
        cursor='arrow',
    )
    canvas.itemconfig(  # configuring 'zanyato' size in a normal way doesn't work on canvas
        zanyato_,
        width=preview.width(),
        height=preview.height(),
    )
    sortir.update()
    fit_width, fit_height = min(sortir.winfo_reqwidth(), 9 * sortir.winfo_screenwidth() // 10), min(sortir.winfo_reqheight(), 9 * sortir.winfo_screenheight() // 10)
    sortir.minsize(fit_width, fit_height)
    # ↓ updating zoom factor display
    label_zoom.config(text=zoom_show[zoom_factor])
    # ↓ reenabling +/- buttons
    butt_minus.config(state='normal', cursor='hand2')
    if zoom_factor == maxizoom:
        butt_plus.config(state='disabled', cursor='arrow')
    else:
        butt_plus.config(state='normal', cursor='hand2')


def zoomOut(event=None) -> None:
    """Zoom preview out."""

    global zoom_factor, preview

    zoom_factor = max(zoom_factor - 1, minizoom)
    preview = zoom_do[zoom_factor]
    zanyato.config(
        image=preview,
        compound='none',
    )
    # ↓ Sizes of preview to fit the screen
    preview_width, preview_height = min(preview.width(), 8 * sortir.winfo_screenwidth() // 10), min(preview.height(), (8 * sortir.winfo_screenheight() // 10) - frame_zoom.winfo_height())
    canvas.config(
        width=preview_width,
        height=preview_height,  # Note that 'scrollregion' may be bigger than canvas!
        scrollregion=(0, 0, preview.width(), preview.height()),
        cursor='arrow',
    )
    canvas.itemconfig(  # configuring 'zanyato' size in a normal way doesn't work on canvas
        zanyato_,
        width=preview.width(),
        height=preview.height(),
    )
    sortir.update()
    fit_width, fit_height = min(sortir.winfo_reqwidth(), 9 * sortir.winfo_screenwidth() // 10), min(sortir.winfo_reqheight(), 9 * sortir.winfo_screenheight() // 10)
    sortir.minsize(fit_width, fit_height)
    # ↓ updating zoom factor display
    label_zoom.config(text=zoom_show[zoom_factor])
    # ↓ reenabling +/- buttons
    butt_plus.config(state='normal', cursor='hand2')
    if zoom_factor == minizoom:  # min zoom 1/5
        butt_minus.config(state='disabled', cursor='arrow')
    else:
        butt_minus.config(state='normal', cursor='hand2')


def zoomWheel(event) -> None:
    """zoomIn or zoomOut by mouse wheel."""

    if event.widget not in (insecticide, pogovorit):
        if event.delta < 0:
            zoomOut()
        if event.delta > 0:
            zoomIn()


def zoomOne(event=None) -> None:
    """Zoom 1:1."""

    global zoom_factor, preview

    zoom_factor = 0
    preview = zoom_do[zoom_factor]
    zanyato.config(
        image=preview,
        compound='none',
    )
    # ↓ Sizes of preview to fit the screen
    preview_width, preview_height = min(preview.width(), 8 * sortir.winfo_screenwidth() // 10), min(preview.height(), (8 * sortir.winfo_screenheight() // 10) - frame_zoom.winfo_height())
    canvas.config(
        width=preview_width,
        height=preview_height,  # Note that 'scrollregion' may be bigger than canvas!
        scrollregion=(0, 0, preview.width(), preview.height()),
        cursor='arrow',
    )
    canvas.itemconfig(  # configuring 'zanyato' size in a normal way doesn't work on canvas
        zanyato_,
        width=preview.width(),
        height=preview.height(),
    )
    sortir.update()
    fit_width, fit_height = min(sortir.winfo_reqwidth(), 9 * sortir.winfo_screenwidth() // 10), min(sortir.winfo_reqheight(), 9 * sortir.winfo_screenheight() // 10)
    sortir.minsize(fit_width, fit_height)
    # ↓ updating zoom factor display
    label_zoom.config(text=zoom_show[zoom_factor])

    # ↓ Reenabling +/- buttons
    butt_plus.config(state='normal', cursor='hand2')
    butt_minus.config(state='normal', cursor='hand2')


def canvasCoord(event) -> None:
    """Marking 'canvas' click point for further dragging."""

    canvas.scan_mark(event.x, event.y)


def canvasDrag(event) -> None:
    """Dragging 'canvas' Canvas."""

    canvas.scan_dragto(
        event.x,
        event.y,
        gain=1,
    )
    canvas['cursor'] = 'fleur'


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """

zoom_factor = 0
sourcefilename = X = Y = Z = maxcolors = None
minizoom, maxizoom = (-4, 4)  # Zoom from 1:5 to 5:1. Mnemonic: "mini" means "image look small".

sortir = Tk()
sortir.title('PNMViewer')
sortir.iconphoto(True, PhotoImage(data=b'P6\n2 2\n255\n\xff\x00\x00\xff\xff\x00\x00\x00\xff\x00\xff\x00'))

# ↓ Main menu, currently one "File" entry
menu01 = Menu(sortir, tearoff=False)
menu01.add_command(label='Open...', state='normal', accelerator='Ctrl+O', command=GetSource)
menu01.add_separator()
menu01.add_command(label='Save binary PNM...', state='disabled', command=lambda: SaveAsPNM(bin=True))
menu01.add_command(label='Save ASCII PNM...', state='disabled', command=lambda: SaveAsPNM(bin=False))
menu01.add_command(label='Save PNG...', state='disabled', command=SaveAsPNG)
menu01.add_separator()
menu01.add_command(label='Info', state='disabled', accelerator='Ctrl+I', command=ShowInfo)
menu01.add_separator()
pop_debug = BooleanVar(value=False)
menu01.add_checkbutton(label='Pop debug window', variable=pop_debug, state='normal', command=PopUnpopDebug)
menu01.add_separator()
menu01.add_command(label='Exit', state='normal', accelerator='Ctrl+Q', command=DisMiss)

frame_img = Frame(sortir, borderwidth=2, relief='groove')
frame_img.pack(side='top', anchor='center', expand=True)

canvas = Canvas(
    frame_img,
    borderwidth=1,
    highlightthickness=1,
    # ↓ Canvas have two borders, combination of both may give contrast with any image
    # background='red',  # internal border
    # highlightbackground='green',  # external border
    # highlightcolor='yellow',  # external border with opened image
)
canvas.pack()

zanyato = Label(
    canvas,
    text='Preview area.\n  Double click to open image,\n  Right click or Alt+F for a menu.\nWith image opened,\n  Zoom in: Ctrl+Click or Ctrl+"+",\n  Zoom out: Alt+Click or Ctrl+"-",\n  Zoom 1:1: Ctrl+1;\n  Wheel: zoom +/-;\n  Click and drag: pan',
    font=('helvetica', 12),
    justify='left',
    borderwidth=2,
    padx=24,
    pady=24,
    relief='groove',
    foreground='dark blue',
    background='light blue',
    cursor='arrow',
)
zanyato.pack(side='top', padx=0, pady=(0, 2))

zanyato_ = canvas.create_window(
    0,
    0,
    window=zanyato,
    width=zanyato.winfo_reqwidth(),
    height=zanyato.winfo_reqheight(),
    anchor='nw',
)
canvas.config(
    width=zanyato.winfo_reqwidth(),
    height=zanyato.winfo_reqheight(),
    scrollregion=(0, 0, zanyato.winfo_reqwidth(), zanyato.winfo_reqheight()),
)

zanyato.bind('<Double-Button-1>', GetSource)
frame_img.bind('<Double-Button-1>', GetSource)

frame_zoom = Frame(
    frame_img,
    width=300,
    borderwidth=2,
    relief='groove',
)
frame_zoom.pack(side='bottom')

butt_plus = Button(
    frame_zoom,
    text='+',
    font=('courier', 8),
    width=2,
    cursor='arrow',
    justify='center',
    state='disabled',
    borderwidth=1,
    command=zoomIn,
)
butt_plus.pack(side='left', padx=0, pady=0, fill='both')

butt_minus = Button(
    frame_zoom,
    text='-',
    font=('courier', 8),
    width=2,
    cursor='arrow',
    justify='center',
    state='disabled',
    borderwidth=1,
    command=zoomOut,
)
butt_minus.pack(side='right', padx=0, pady=0, fill='both')

label_zoom = Label(
    frame_zoom,
    text='Zoom 1:1',
    font=('courier', 8),
    state='disabled',
)
label_zoom.pack(side='left', anchor='n', padx=2, pady=0, fill='both')

sortir.bind_all('<Button-3>', ShowMenu)
sortir.bind_all('<Alt-f>', ShowMenu)
sortir.bind_all('<Alt-F>', ShowMenu)
sortir.bind_all('<Control-o>', GetSource)
sortir.bind_all('<Control-O>', GetSource)
sortir.bind_all('<Control-q>', DisMiss)
sortir.bind_all('<Control-Q>', DisMiss)
sortir.bind_all('<Control-w>', DisMiss)
sortir.bind_all('<Control-W>', DisMiss)

sortir.update()

# ↓ Setting minsize
fit_width, fit_height = min(sortir.winfo_reqwidth(), 9 * sortir.winfo_screenwidth() // 10), min(sortir.winfo_reqheight(), 9 * sortir.winfo_screenheight() // 10)
sortir.minsize(fit_width, fit_height)

# ↓ Setting maxsize to fit 90% of screen
sortir.maxsize(9 * sortir.winfo_screenwidth() // 10, 9 * sortir.winfo_screenheight() // 10)

# ↓ Center window, +64 vertically
sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_reqwidth()) // 2}+64')

# ↓ Debug window
insecticide = Toplevel(sortir)
"""Debug output window."""
insecticide.title('<DEBUG>')
insecticide.geometry('+32+32')
insecticide.protocol('WM_DELETE_WINDOW', ShallPass)
pogovorit = ScrolledText(
    insecticide,
    height=26,
    wrap='word',
    state='normal',
)
"""Scrollable text in Debug output window."""
pogovorit.pack(fill='both', side='top', expand=True)
pogovorit.insert('1.0', f'This is PNMViewer {__version__} debug window.\nSome image and image list info will be shown here.\n')
pogovorit.see('end')
# ↓ Hiding debug window; will be unhidden by GetSource.
insecticide.iconify()
# ↓ Placing debug window right below main one.
insecticide.lower(sortir)

# ↓ Command line part
if len(argv) == 2:
    sortir.focus_force()  # Otherwise loses focus when run from command line
    try_to_open = argv[1]
    if Path(try_to_open).exists() and Path(try_to_open).is_file() and (Path(try_to_open).suffix.lower() in ('.ppm', '.pgm', '.pbm', '.pnm', '.png')):
        filename_from_command = str(Path(try_to_open).resolve())
        GetSource()
    else:
        filename_from_command = None
else:
    sortir.focus_force()  # Otherwise loses focus when run from command line
    filename_from_command = None

sortir.mainloop()
