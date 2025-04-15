#!/usr/bin/env python3

"""Test shell for `PyPNM<https://github.com/Dnyarri/PyPNM/>`_ module - Tkinter-based viewer.

Viewer does not use PPM file directly to display it with Tkinter PhotoImage(file=...) -
instead, it loads image file (in this case - PPM, PGM, or PBM, just because it's a demo
for PyPNM module anyway), then constructs PPM-like bytes data object in memory, and then
displays it using Tkinter PhotoImage(data=...).
For example, it's able to display ascii PGM and PPM, not directly supported by Tkinter,
since it recodes them to binary on the fly.

"""

__author__ = 'Ilya Razmanov'
__copyright__ = '(c) 2025 Ilya Razmanov'
__credits__ = 'Ilya Razmanov'
__license__ = 'unlicense'
__version__ = '2.16.15.17'
__maintainer__ = 'Ilya Razmanov'
__email__ = 'ilyarazmanov@gmail.com'
__status__ = 'Production'

from tkinter import Button, Frame, Label, Menu, PhotoImage, Tk, filedialog
from tkinter.messagebox import showinfo

from pypnm import pnmlpnm


def DisMiss():
    """Kill dialog and continue"""
    sortir.destroy()


def UINormal():
    """Normal UI state"""
    zanyato.config(state='normal', cursor='arrow')
    sortir.update()


def UIBusy():
    """Busy UI state"""
    zanyato.config(state='disabled', cursor='wait')
    sortir.after(1, sortir.update())  # Otherwise cursor never updates
    sortir.update()


def ShowMenu(event):
    """Pop menu up (or sort of drop it down)"""
    menu01.post(event.x_root, event.y_root)


def ShowInfo():
    """Show program and module version"""
    showinfo(
        title='Program information',
        message=f'PNMViewer ver. {__version__}\nModules:\n{pnmlpnm.__name__} ver. {pnmlpnm.__version__}',
        detail=f'Image: {sourcefilename}\nX={X}, Y={Y}, Z={Z}, maxcolors={maxcolors}',
    )


def GetSource(event=None):
    """Opening source image and redefining other controls state"""

    global zoom_factor, zoom_do, zoom_show, preview, preview_data
    global X, Y, Z, maxcolors, image3D, sourcefilename
    zoom_factor = 0

    sourcefilename = filedialog.askopenfilename(title='Open PPM/PGM file to view', filetypes=[('Portable map formats', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        return

    UIBusy()

    """ ┌────────────────────────────────────────┐
        │ Loading file, converting data to list. │
        │  NOTE: maxcolors, image3D are GLOBALS! │
        │  This is required for preview to work. │
        └────────────────────────────────────────┘ """

    X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(sourcefilename)

    """ ┌─────────────────────────────────────────────────────────────────────────┐
        │ Converting list to bytes of PPM-like structure "preview_data" in memory │
        └────────────────────────────────────────────────────────────────────────-┘ """
    preview_data = pnmlpnm.list2bin(image3D, maxcolors)

    """ ┌────────────────────────────────────────────────┐
        │ Now showing "preview_data" bytes using Tkinter │
        └────────────────────────────────────────────────┘ """
    preview = PhotoImage(data=preview_data)

    zoom_show = {  # Text to show below preview
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
    zoom_do = {  # Actions to zoom preview; "zoom" zooms in, "subsample" zooms out
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
    zanyato.config(image=preview, compound='none', foreground='grey')
    # binding zoom on preview click
    zanyato.bind('<Control-Button-1>', zoomIn)  # Ctrl + left click
    zanyato.bind('<Double-Control-Button-1>', zoomIn)  # Ctrl + left click too fast
    zanyato.bind('<Alt-Button-1>', zoomOut)  # Alt + left click
    zanyato.bind('<Double-Alt-Button-1>', zoomOut)  # Alt + left click too fast
    zanyato.bind('<MouseWheel>', zoomWheel)  # Wheel
    # enabling zoom buttons
    butt_plus.config(state='normal', cursor='hand2')
    butt_minus.config(state='normal', cursor='hand2')
    # updating zoom label display
    label_zoom.config(text=zoom_show[zoom_factor])
    # enabling "Save as..."
    menu01.entryconfig('Save binary PNM...', state='normal')  # Instead of name numbers from 0 may be used
    menu01.entryconfig('Save ascii PNM...', state='normal')

    UINormal()


def SaveAsBin():
    """Once pressed on Save binary"""

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
        title=f'Save {filetype} file',
        filetypes=format,
        defaultextension=extension,
    )
    if savefilename == '':
        return

    """ ┌───────────────────────────────────────────────────────┐
        │ Converting list to bytes and saving as "savefilename" │
        └──────────────────────────────────────────────────────-┘ """
    UIBusy()
    pnmlpnm.list2pnm(savefilename, image3D, maxcolors)
    UINormal()


def SaveAsAscii():
    """Once pressed on Save ASCII"""

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
        title=f'Save {filetype} file',
        filetypes=format,
        defaultextension=extension,
    )
    if savefilename == '':
        return

    """ ┌────────────────────────────────────────────────────────┐
        │ Converting list to string and saving as "savefilename" │
        └───────────────────────────────────────────────────────-┘ """
    UIBusy()
    pnmlpnm.list2pnmascii(savefilename, image3D, maxcolors)
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
sourcefilename = X = Y = Z = maxcolors = None

sortir = Tk()

sortir.title('PNMViewer')
sortir.geometry('+200+100')

# Main dialog icon is PPM as well!
sortir.iconphoto(True, PhotoImage(data=b'P6\n2 2\n255\n\xff\x00\x00\xff\xff\x00\x00\x00\xff\x00\xff\x00'))

menu01 = Menu(sortir, tearoff=False)  # Main menu, currently one "File" entry

menu01.add_command(label='Open...', state='normal', command=GetSource)
menu01.add_command(label='Save binary PNM...', state='disabled', command=SaveAsBin)
menu01.add_command(label='Save ascii PNM...', state='disabled', command=SaveAsAscii)
menu01.add_separator()
menu01.add_command(label='Info', command=ShowInfo)
menu01.add_separator()
menu01.add_command(label='Exit', state='normal', command=DisMiss)

sortir.bind('<Button-3>', ShowMenu)

frame_img = Frame(sortir, borderwidth=2, relief='groove')
frame_img.pack(side='top')

zanyato = Label(
    frame_img,
    text='Preview area.\nDouble click to open,\nRight click for a menu.\nWhen opened,\nCtrl+Click to zoom in,\nAlt+Click to zoom out.',
    font=('helvetica', 12),
    justify='center',
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

butt_plus = Button(frame_zoom, text='+', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', command=zoomIn)
butt_plus.pack(side='left', padx=0, pady=0, fill='both')

butt_minus = Button(frame_zoom, text='-', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', command=zoomOut)
butt_minus.pack(side='right', padx=0, pady=0, fill='both')

label_zoom = Label(frame_zoom, text='Zoom 1:1', font=('courier', 8), state='disabled')
label_zoom.pack(side='left', anchor='n', padx=2, pady=0, fill='both')

sortir.mainloop()
