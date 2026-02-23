#!/usr/bin/env python3

"""Test shell for `PyPNM for Python >= 3.11`_ module - a Tkinter-based viewer.

Viewer does not use PNM file directly to display it with
Tkinter ``PhotoImage(file=...)`` - instead, it loads image file,
then constructs PNM-like bytes data object in memory,
and then displays it using Tkinter ``PhotoImage(data=...)``.

For example, it's able to display ASCII PGM and PPM,
not supported by Tkinter, since it recodes them to binary on the fly.

.. _PyPNM for Python >= 3.11: https://github.com/Dnyarri/PyPNM

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025-2026 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2.26.23.23'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from pathlib import Path
from platform import python_version, python_version_tuple  # Used for info
from sys import argv
from time import ctime  # Used to show file info only
from tkinter import Button, Frame, Label, Menu, PhotoImage, Tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showinfo

import pypnm  # import whole module to display version info

""" ╔══════════════════════════════════╗
    ║ GUI events and functions thereof ║
    ╚══════════════════════════════════╝ """


def DisMiss(event=None) -> None:
    """Kill dialog and continue"""

    sortir.destroy()


def BindAll() -> None:
    """Binding events needed even with no image open"""

    sortir.bind_all('<Button-3>', ShowMenu)
    sortir.bind_all('<Alt-f>', ShowMenu)
    sortir.bind_all('<Control-o>', GetSource)
    sortir.bind_all('<Control-q>', DisMiss)


def UINormal() -> None:
    """Normal UI state"""

    zanyato['state'] = 'normal'
    sortir.update()


def UIBusy() -> None:
    """Busy UI state"""

    zanyato['state'] = 'disabled'
    sortir.update()


def ShowMenu(event) -> None:
    """Pop menu up (or sort of drop it down)"""

    menu01.post(event.x_root, event.y_root)


def ShowInfo(event=None) -> None:
    """Show program and module version, and image info"""

    file_size = Path(sourcefilename).stat().st_size
    file_size_str = f'{file_size / 1048576:.2f} Mb' if (file_size > 1048576) else f'{file_size / 1024:.2f} Kb' if (file_size > 1024) else f'{file_size} bytes'
    creation_str = f'{ctime(Path(sourcefilename).stat().st_ctime)}' if int(python_version_tuple()[1]) < 12 else f'{ctime(Path(sourcefilename).stat().st_birthtime)}'
    modification_str = ctime(Path(sourcefilename).stat().st_mtime)
    showinfo(
        title='General information',
        message=f'PNMViewer ver. {__version__}\nPython: {python_version()}\nModules:\n{pypnm.__name__} ver. {pypnm.__version__}',
        detail=f'File properties:\n{sourcefilename}\nSize: {file_size_str}\nCreated: {creation_str}\nModified: {modification_str}\n\nImage properties:\nWidth: {X} px\nHeight: {Y} px\nChannels: {Z} channel{"s" if Z > 1 else ""}\nColor depth: {maxcolors + 1} gradations/channel',
    )


def GetSource(event=None) -> None:
    """Open source image and redefine other controls state"""

    global zoom_factor, zoom_do, zoom_show, preview, preview_data
    global X, Y, Z, maxcolors, image3D, sourcefilename, filename_from_command
    zoom_factor = 0

    # ↓ Trying to receive file name from command line, if None, opening GUI
    if filename_from_command is None:
        sourcefilename = askopenfilename(title='Open PPM/PGM file to view', filetypes=[('Portable any map', '.ppm .pgm .pbm .pnm')])
        if sourcefilename == '':
            return
    else:
        sourcefilename = filename_from_command
        filename_from_command = None  # Removing file name after first open

    UIBusy()

    # ↓ Loading file, converting data to list.
    #   NOTE: maxcolors, image3D are GLOBALS!
    #   They are used during save!
    X, Y, Z, maxcolors, image3D = pypnm.pnm2list(sourcefilename)
    # ↓ Converting list to bytes of PPM-like structure "preview_data" in memory
    preview_data = pypnm.list2bin(image3D, maxcolors)
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
    #   GUI X extra = 16 px, GUI Y extra = 63 px
    screen_width = sortir.winfo_screenwidth()
    screen_height = sortir.winfo_screenheight()
    if X + 16 > screen_width or Y + 64 > screen_height:
        zoom_factor = -(max((X + 16) // screen_width, (Y + 64) // screen_height))

    preview = zoom_do[zoom_factor]
    zanyato.config(image=preview, compound='none', borderwidth=1, background=zanyato.master['background'])
    zanyato.pack_configure(pady=max(0, 16 - (preview.height() // 2)))
    # ↓ binding on preview click
    zanyato.bind('<Control-Button-1>', zoomIn)  # Ctrl + left click
    zanyato.bind('<Double-Control-Button-1>', zoomIn)  # Ctrl + left click too fast
    zanyato.bind('<Alt-Button-1>', zoomOut)  # Alt + left click
    zanyato.bind('<Double-Alt-Button-1>', zoomOut)  # Alt + left click too fast
    sortir.bind_all('<MouseWheel>', zoomWheel)  # Wheel
    sortir.bind_all('<Control-i>', ShowInfo)
    # ↓ enabling zoom buttons
    butt_plus.config(state='normal', cursor='hand2')
    butt_minus.config(state='normal', cursor='hand2')
    # ↓ updating zoom label display
    label_zoom.config(text=zoom_show[zoom_factor])
    # ↓ enabling "Save as..."
    menu01.entryconfig('Save binary PNM...', state='normal')  # Instead of name numbers from 0 may be used
    menu01.entryconfig('Save ASCII PNM...', state='normal')
    menu01.entryconfig('Export via Tkinter...', state='normal')
    menu01.entryconfig('Info', state='normal')
    UINormal()
    sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+{(sortir.winfo_screenheight() - sortir.winfo_height()) // 2 - 32}')


def SaveAsPNM(bin: bool) -> None:
    """Once pressed on any of Save PNM"""

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

    # ↓ Open "Save as..." file
    savefilename = asksaveasfilename(
        title=f'Save {filetype.upper()} file',
        filetypes=format,
        defaultextension=extension,
        initialdir=Path(sourcefilename).parent,
        initialfile=Path(sourcefilename).stem + f' copy.{filetype}',
    )
    if savefilename == '':
        return

    # ↓ Saving "savefilename" in PNM format depending on "bin" value
    UIBusy()
    pypnm.list2pnm(savefilename, image3D, maxcolors, bin)
    # ↓ Changing filename to new saved one
    sourcefilename = savefilename
    sortir.title(f'PNMViewer: {Path(sourcefilename).name}')
    UINormal()


def ExportPhotoImage() -> None:
    """Use Tkinter PhotoImage.write to export image.

    This function writes Tkinter PhotoImage object to file.
    It does not create editable 3D list as PyPNM does. It just dumps.
    All Tkinter limitations apply, like color depth ones.

    """

    if Z == 1:
        format_list = [('Portable network graphics', '.png'), ('Graphics interchange format', '.gif'), ('Portable any map', '.pnm')]
        proposed_name = Path(sourcefilename).stem + '.png'
    elif Z == 3:
        format_list = [('Portable network graphics', '.png'), ('Portable any map', '.pnm')]
        proposed_name = Path(sourcefilename).stem + '.png'
    else:
        format_list = [('Portable network graphics', '.png')]
        proposed_name = Path(sourcefilename).stem + '.png'

    # ↓ Open "Save as..." file
    savefilename = asksaveasfilename(
        title='Export via Tinter',
        filetypes=format_list,
        defaultextension='.png',
        initialdir=Path(sourcefilename).parent,
        initialfile=proposed_name,
    )
    if savefilename == '':
        return
    UIBusy()

    # ↓ Recreates preview_data from global image3D,
    #   does not show it but feeds to Tkinter to create and
    #   dump PhotoImage.
    preview_data = pypnm.list2bin(image3D, maxcolors)
    preview_dump = PhotoImage(data=preview_data)
    if Path(savefilename).suffix.lower() in ('.pgm', '.ppm', '.pnm'):
        preview_dump.write(savefilename, format='ppm')
    elif Path(savefilename).suffix.lower() == '.gif':
        preview_dump.write(savefilename, format='gif')
    else:
        preview_dump.write(savefilename, format='png')
    UINormal()


def zoomIn(event=None) -> None:
    """Zoom preview in"""

    global zoom_factor, preview
    zoom_factor = min(zoom_factor + 1, 4)  # max zoom 5
    preview = PhotoImage(data=preview_data)
    preview = zoom_do[zoom_factor]
    zanyato.config(image=preview, compound='none')
    zanyato.pack_configure(pady=max(0, 16 - (preview.height() // 2)))
    # ↓ updating zoom factor display
    label_zoom.config(text=zoom_show[zoom_factor])
    # ↓ reenabling +/- buttons
    butt_minus.config(state='normal', cursor='hand2')
    if zoom_factor == 4:  # max zoom 5
        butt_plus.config(state='disabled', cursor='arrow')
    else:
        butt_plus.config(state='normal', cursor='hand2')


def zoomOut(event=None) -> None:
    """Zoom preview out"""

    global zoom_factor, preview
    zoom_factor = max(zoom_factor - 1, -4)  # min zoom 1/5
    preview = PhotoImage(data=preview_data)
    preview = zoom_do[zoom_factor]
    zanyato.config(image=preview, compound='none')
    zanyato.pack_configure(pady=max(0, 16 - (preview.height() // 2)))
    # ↓ updating zoom factor display
    label_zoom.config(text=zoom_show[zoom_factor])
    # ↓ reenabling +/- buttons
    butt_plus.config(state='normal', cursor='hand2')
    if zoom_factor == -4:  # min zoom 1/5
        butt_minus.config(state='disabled', cursor='arrow')
    else:
        butt_minus.config(state='normal', cursor='hand2')


def zoomWheel(event) -> None:
    """zoomIn or zoomOut by mouse wheel"""

    if event.delta < 0:
        zoomOut()
    if event.delta > 0:
        zoomIn()


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """

zoom_factor = 0
sourcefilename = X = Y = Z = maxcolors = None

sortir = Tk()
sortir.title('PNMViewer')
sortir.minsize(128, 128)
sortir.iconphoto(True, PhotoImage(data=b'P6\n2 2\n255\n\xff\x00\x00\xff\xff\x00\x00\x00\xff\x00\xff\x00'))

# ↓ Main menu, currently one "File" entry
menu01 = Menu(sortir, tearoff=False)
menu01.add_command(label='Open...', state='normal', accelerator='Ctrl+O', command=GetSource)
menu01.add_separator()
menu01.add_command(label='Save binary PNM...', state='disabled', command=lambda: SaveAsPNM(bin=True))
menu01.add_command(label='Save ASCII PNM...', state='disabled', command=lambda: SaveAsPNM(bin=False))
menu01.add_command(label='Export via Tkinter...', state='disabled', command=ExportPhotoImage)
menu01.add_separator()
menu01.add_command(label='Info', accelerator='Ctrl+I', state='disabled', command=ShowInfo)
menu01.add_separator()
menu01.add_command(label='Exit', state='normal', accelerator='Ctrl+Q', command=DisMiss)

frame_img = Frame(sortir, borderwidth=2, relief='groove')
frame_img.pack(side='top', anchor='center', expand=True)

zanyato = Label(
    frame_img,
    text='Preview area.\n  Double click to open image,\n  Right click or Alt+F for a menu.\nWith image opened,\n  Ctrl+Click to zoom in,\n  Alt+Click to zoom out.',
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
zanyato.bind('<Double-Button-1>', GetSource)
frame_img.bind('<Double-Button-1>', GetSource)
zanyato.pack(side='top', padx=0, pady=(0, 2))

frame_zoom = Frame(frame_img, width=300, borderwidth=2, relief='groove')
frame_zoom.pack(side='bottom')

butt_plus = Button(frame_zoom, text='+', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', borderwidth=1, command=zoomIn)
butt_plus.pack(side='left', padx=0, pady=0, fill='both')

butt_minus = Button(frame_zoom, text='-', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', borderwidth=1, command=zoomOut)
butt_minus.pack(side='right', padx=0, pady=0, fill='both')

label_zoom = Label(frame_zoom, text='Zoom 1:1', font=('courier', 8), state='disabled')
label_zoom.pack(side='left', anchor='n', padx=2, pady=0, fill='both')

BindAll()

# ↓ Center window, +32 vertically
sortir.update()
sortir.geometry(f'+{(sortir.winfo_screenwidth() - sortir.winfo_width()) // 2}+{(sortir.winfo_screenheight() - sortir.winfo_height()) // 2 - 32}')

# ↓ Command line part
if len(argv) == 2:
    try_to_open = argv[1]
    if Path(try_to_open).exists() and Path(try_to_open).is_file() and (Path(try_to_open).suffix.lower() in ('.ppm', '.pgm', '.pbm', '.pnm')):
        filename_from_command = str(Path(try_to_open).resolve())
        GetSource()
    else:
        filename_from_command = None
    sortir.focus_force()  # Otherwise loses focus when run from command line
else:
    filename_from_command = None
    sortir.focus_force()  # Otherwise loses focus when run from command line

sortir.mainloop()
