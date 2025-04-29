#!/usr/bin/env python3

"""Test shell for `PyPNM<https://github.com/Dnyarri/PyPNM/>`_ module - Tkinter-based viewer.

Viewer does not use PPM file directly to display it with Tkinter PhotoImage(file=...) -
instead, it loads image file, then constructs PPM-like bytes data object in memory,
and then displays it using Tkinter PhotoImage(data=...).
For example, it's able to display ascii PGM and PPM, not directly supported by Tkinter,
since it recodes them to binary on the fly.

NOTE:

This is special extended compatibility edition, tested with Python 3.4 under Windows XP,
including `PNG support<https://gitlab.com/drj11/pypng>`_.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2.16.28.34'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from pathlib import Path
from tkinter import Button, Frame, Label, Menu, PhotoImage, Tk, filedialog
from tkinter.messagebox import showinfo

from pypng import pnglpng
from pypnm import pnmlpnm


def DisMiss(event=None):
    """Kill dialog and continue"""
    sortir.destroy()


def UINormal():
    """Normal UI state"""
    zanyato.config(state='normal')
    sortir.update()


def UIBusy():
    """Busy UI state"""
    zanyato.config(state='disabled')
    sortir.update()


def ShowMenu(event):
    """Pop menu up (or sort of drop it down)"""
    menu01.post(event.x_root, event.y_root)


def ShowInfo():
    """Show program and module version"""
    message = ''.join(
        (
            'PNMViewer ver. ',
            str(__version__),
            '\nModules:\n',
            str(pnmlpnm.__name__),
            ' ver. ',
            str(pnmlpnm.__version__),
            '\n',
            str(pnglpng.__name__),
            ' ver. ',
            str(pnglpng.__version__),
            '\n',
            str(pnglpng.png.__name__),
            ' ver. ',
            str(pnglpng.png.__version__),
        )
    )
    detail = ''.join(('Image: ', sourcefilename, '\nX=', str(X), ' Y=', str(Y), ' Z=', str(Z), ' maxcolors=', str(maxcolors)))
    showinfo(
        title='General information',
        message=message,
        detail=detail,
    )


def GetSource(event=None):
    """Opening source image and redefining other controls state"""

    global zoom_factor, zoom_do, zoom_show, preview, preview_data
    global X, Y, Z, maxcolors, image3D, sourcefilename
    zoom_factor = 0

    sourcefilename = filedialog.askopenfilename(title='Open image file', filetypes=[('Supported formats', '.png .ppm .pgm .pbm'), ('PNG', '.png'), ('PNM', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        return

    UIBusy()

    """ ┌────────────────────────────────────────┐
        │ Loading file, converting data to list. │
        │  NOTE: maxcolors, image3D are GLOBALS! │
        │  They are used during save!            │
        └────────────────────────────────────────┘ """

    if Path(sourcefilename).suffix == '.png':
        # Reading image as list
        X, Y, Z, maxcolors, image3D, info = pnglpng.png2list(sourcefilename)

    elif Path(sourcefilename).suffix in ('.ppm', '.pgm', '.pbm'):
        # Reading image as list
        X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(sourcefilename)

    else:
        raise ValueError('Extension not recognized')

    """ ┌─────────────────────────────────────────────────────────────────────────┐
        │ Converting list to bytes of PPM-like structure "preview_data" in memory │
        └────────────────────────────────────────────────────────────────────────-┘ """
    preview_data = pnmlpnm.list2bin(image3D, maxcolors, show_chessboard=True)

    """ ┌────────────────────────────────────────────────┐
        │ Now showing "preview_data" bytes using Tkinter │
        └────────────────────────────────────────────────┘ """
    preview = PhotoImage(data=preview_data)

    zoom_show = {  # What to show below preview
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
    zoom_do = {  # What to do to preview; "zoom" zooms in, "subsample" zooms out
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

    preview = zoom_do[zoom_factor]
    zanyato.config(image=preview, compound='none', borderwidth=1, background=zanyato.master['background'])
    # binding zoom on preview click
    zanyato.bind('<Control-Button-1>', zoomIn)  # Ctrl + left click
    zanyato.bind('<Double-Control-Button-1>', zoomIn)  # Ctrl + left click too fast
    zanyato.bind('<Alt-Button-1>', zoomOut)  # Alt + left click
    zanyato.bind('<Double-Alt-Button-1>', zoomOut)  # Alt + left click too fast
    sortir.bind_all('<MouseWheel>', zoomWheel)  # Wheel
    # enabling zoom buttons
    butt_plus.config(state='normal', cursor='hand2')
    butt_minus.config(state='normal', cursor='hand2')
    # updating zoom label display
    label_zoom.config(text=zoom_show[zoom_factor])
    # enabling "Save as..."
    menu01.entryconfig('Save binary PNM...', state='normal')  # Instead of name numbers from 0 may be used
    menu01.entryconfig('Save ascii PNM...', state='normal')
    menu01.entryconfig('Save PNG...', state='normal')

    UINormal()


def SaveAsPNM(bin):
    """Once pressed on any of Save PNM"""

    # Adjusting "Save to" formats to be displayed according to channel number
    if Z < 3:
        format = [('Portable grey map', '.pgm')]
        extension = ('Portable grey map', '.pgm')
        filetype = 'PGM'
    else:
        format = [('Portable pixel map', '.ppm')]
        extension = ('Portable pixel map', '.ppm')
        filetype = 'PPM'

    # Open "Save as..." file
    savefilename = filedialog.asksaveasfilename(
        title='Save {ext} file'.format(ext=filetype),
        filetypes=format,
        defaultextension=extension,
    )
    if savefilename == '':
        return

    """ ┌────────────────────────────────────────────────────┐
        │ Saving "savefilename" in format depending on "bin" │
        └───────────────────────────────────────────────────-┘ """
    UIBusy()
    pnmlpnm.list2pnm(savefilename, image3D, maxcolors, bin)
    UINormal()


def SaveAsPNG():
    """Once pressed on Save PNG"""

    # Open "Save as..." file
    savefilename = filedialog.asksaveasfilename(
        title='Save PNG file',
        filetypes=[('Portable network graphics', '.png')],
        defaultextension=('Portable network graphics', '.png'),
    )
    if savefilename == '':
        return

    # Creating dummy info
    info = {}
    # Fixing color mode. The rest is fixed with pnglpng v. 25.01.07.
    if maxcolors > 255:
        info['bitdepth'] = 16
    else:
        info['bitdepth'] = 8

    """ ┌───────────────────────────────────┐
        │ Feeding list to PyPNG via pnglpng │
        └──────────────────────────────────-┘ """
    UIBusy()
    pnglpng.list2png(savefilename, image3D, info)
    UINormal()


def zoomIn(event=None):
    global zoom_factor, preview
    zoom_factor = min(zoom_factor + 1, 4)  # max zoom 5
    preview = PhotoImage(data=preview_data)
    preview = zoom_do[zoom_factor]
    zanyato.config(image=preview, compound='none')
    # updating zoom factor display
    label_zoom.config(text=zoom_show[zoom_factor])
    # reenabling +/- buttons
    butt_minus.config(state='normal', cursor='hand2')
    if zoom_factor == 4:  # max zoom 5
        butt_plus.config(state='disabled', cursor='arrow')
    else:
        butt_plus.config(state='normal', cursor='hand2')


def zoomOut(event=None):
    global zoom_factor, preview
    zoom_factor = max(zoom_factor - 1, -4)  # min zoom 1/5
    preview = PhotoImage(data=preview_data)
    preview = zoom_do[zoom_factor]
    zanyato.config(image=preview, compound='none')
    # updating zoom factor display
    label_zoom.config(text=zoom_show[zoom_factor])
    # reenabling +/- buttons
    butt_plus.config(state='normal', cursor='hand2')
    if zoom_factor == -4:  # min zoom 1/5
        butt_minus.config(state='disabled', cursor='arrow')
    else:
        butt_minus.config(state='normal', cursor='hand2')


def zoomWheel(event):
    if event.delta < 0:
        zoomOut()
    if event.delta > 0:
        zoomIn()


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """

# Starting values
zoom_factor = 0
X = Y = Z = maxcolors = None
sourcefilename = 'None'

sortir = Tk()

sortir.title('PNMViewer')
sortir.geometry('+200+100')
sortir.minsize(128, 128)

# Main dialog icon is PPM as well!
sortir.iconphoto(True, PhotoImage(data=b'P6\n2 2\n255\n\xff\x00\x00\xff\xff\x00\x00\x00\xff\x00\xff\x00'))

menu01 = Menu(sortir, tearoff=False)  # Main menu, currently one "File" entry

menu01.add_command(label='Open...', state='normal', accelerator='Ctrl+O', command=GetSource)
menu01.add_separator()
menu01.add_command(label='Save binary PNM...', state='disabled', command=lambda: SaveAsPNM(bin=True))
menu01.add_command(label='Save ascii PNM...', state='disabled', command=lambda: SaveAsPNM(bin=False))
menu01.add_command(label='Save PNG...', state='disabled', command=SaveAsPNG)
menu01.add_separator()
menu01.add_command(label='Info', command=ShowInfo)
menu01.add_separator()
menu01.add_command(label='Exit', state='normal', accelerator='Ctrl+Q', command=DisMiss)

sortir.bind('<Button-3>', ShowMenu)
sortir.bind_all('<Alt-f>', ShowMenu)
sortir.bind_all('<Control-o>', GetSource)
sortir.bind_all('<Control-q>', DisMiss)

frame_img = Frame(sortir, borderwidth=2, relief='groove')
frame_img.pack(side='top')

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
zanyato.pack(side='top', padx=0, pady=(0, 2))

frame_zoom = Frame(frame_img, width=300, borderwidth=2, relief='groove')
frame_zoom.pack(side='bottom')

butt_plus = Button(frame_zoom, text='+', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', borderwidth=1, command=zoomIn)
butt_plus.pack(side='left', padx=0, pady=0, fill='both')

butt_minus = Button(frame_zoom, text='-', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', borderwidth=1, command=zoomOut)
butt_minus.pack(side='right', padx=0, pady=0, fill='both')

label_zoom = Label(frame_zoom, text='Zoom 1:1', font=('courier', 8), state='disabled')
label_zoom.pack(side='left', anchor='n', padx=2, pady=0, fill='both')

sortir.mainloop()
