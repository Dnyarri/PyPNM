#!/usr/bin/env python3

"""Test shell for pnmlpnm module - Tkinter viewer.

Viewer does not use PPM file directly to display it with Tkinter - it loads file (in this case - PPM or PGM, just because I have my pnmlpnm module anyway), then construct PPM-like bytes data object in memory, and then show it using Tkinter. You may easily check this: Tkinter itself does not show ASCII PPM and PGM, while this viewer does.

"""

from tkinter import Button, Frame, Label, PhotoImage, Tk, filedialog

from pypnm import pnmlpnm


def DisMiss():
    """Kill dialog and continue"""

    sortir.destroy()


def GetSource():
    """Opening source image and redefining other controls state"""

    global zoom_factor, sourcefilename, preview, preview_data
    zoom_factor = 1
    sourcefilename = filedialog.askopenfilename(title='Open PPM/PGM file to view', filetypes=[('Portable map formats', '.ppm .pgm .pbm')])
    if sourcefilename == '':
        return

    """ ┌───────────────────────────────────────┐
        │ Loading file, converting data to list │
        └──────────────────────────────────────-┘ """
    X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(sourcefilename)

    """ ┌─────────────────────────────────────────────────────────────────────────┐
        │ Converting list to bytes of PPM-like structure "preview_data" in memory │
        └────────────────────────────────────────────────────────────────────────-┘ """
    preview_data = pnmlpnm.list2bin(image3D, maxcolors)

    """ ┌────────────────────────────────────────────────┐
        │ Now showing "preview_data" bytes using Tkinter │
        └────────────────────────────────────────────────┘ """
    preview = PhotoImage(data=preview_data)
    preview = preview.zoom(zoom_factor, zoom_factor)  # "zoom" zooms in, "subsample" zooms out
    zanyato.config(text='Source', image=preview, compound='top')
    # enabling zoom
    label_zoom.config(state='normal')
    butt_plus.config(state='normal', cursor='hand2')
    # updating zoom factor display
    label_zoom.config(text=f'Zoom {zoom_factor}:1')
    # enabling "Save as..."
    butt02.config(state='normal', cursor='hand2')
    butt03.config(state='normal', cursor='hand2')


def SaveAsBin():
    """Once pressed on Save as bin"""

    """ ┌───────────────────────────────────────┐
        │ Loading file, converting data to list │
        └──────────────────────────────────────-┘ """
    X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(sourcefilename)

    # Adjusting "Save to" formats to be displayed according to bitdepth
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
    pnmlpnm.list2pnm(savefilename, image3D, maxcolors)


def SaveAsAscii():
    """Once pressed on Save as ASCII"""

    """ ┌───────────────────────────────────────┐
        │ Loading file, converting data to list │
        └──────────────────────────────────────-┘ """
    X, Y, Z, maxcolors, image3D = pnmlpnm.pnm2list(sourcefilename)

    # Adjusting "Save to" formats to be displayed according to bitdepth
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
    pnmlpnm.list2pnmascii(savefilename, image3D, maxcolors)


def zoomIn():
    global zoom_factor, preview
    zoom_factor = min(zoom_factor + 1, 3)  # max zoom 3
    preview = PhotoImage(data=preview_data)
    preview = preview.zoom(zoom_factor, zoom_factor)
    zanyato.config(text='Source', image=preview, compound='top')
    # updating zoom factor display
    label_zoom.config(text=f'Zoom {zoom_factor}:1')
    # reenabling +/- buttons
    butt_minus.config(state='normal', cursor='hand2')
    if zoom_factor == 3:  # max zoom 3
        butt_plus.config(state='disabled', cursor='arrow')
    else:
        butt_plus.config(state='normal', cursor='hand2')


def zoomOut():
    global zoom_factor, preview
    zoom_factor = max(zoom_factor - 1, 1)  # min zoom 1
    preview = PhotoImage(data=preview_data)
    preview = preview.zoom(zoom_factor, zoom_factor)
    zanyato.config(text='Source', image=preview, compound='top')
    # updating zoom factor display
    label_zoom.config(text=f'Zoom {zoom_factor}:1')
    # reenabling +/- buttons
    butt_plus.config(state='normal', cursor='hand2')
    if zoom_factor == 1:  # min zoom 1
        butt_minus.config(state='disabled', cursor='arrow')
    else:
        butt_minus.config(state='normal', cursor='hand2')


""" ╔═══════════╗
    ║ Main body ║
    ╚═══════════╝ """

sortir = Tk()

zoom_factor = 1

sortir.title('PNMViewer')
sortir.geometry('+200+100')
sortir.minsize(300, 110)

# Main dialog icon is PPM as well!
icon = PhotoImage(data=b'P6\n2 2\n255\n\xff\x00\x00\xff\xff\x00\x00\x00\xff\x00\xff\x00')
sortir.iconphoto(True, icon)

frame_left = Frame(sortir, borderwidth=2, relief='groove')
frame_left.pack(side='left', anchor='nw')
frame_right = Frame(sortir, borderwidth=2, relief='groove')
frame_right.pack(side='left', anchor='nw')

butt01 = Button(frame_left, text='Open PPM/PGM...', font=('arial', 16), cursor='hand2', justify='center', command=GetSource)
butt01.pack(side='top', padx=4, pady=[2, 12], fill='both')

butt02 = Button(frame_left, text='Save binary PPM/PGM...', font=('arial', 12), cursor='arrow', justify='center', state='disabled', command=SaveAsBin)
butt02.pack(side='top', padx=4, pady=2, fill='both')

butt03 = Button(frame_left, text='Save ASCII PPM/PGM...', font=('arial', 12), cursor='arrow', justify='center', state='disabled', command=SaveAsAscii)
butt03.pack(side='top', padx=4, pady=2, fill='both')

butt99 = Button(frame_left, text='Exit', font=('arial', 16), cursor='hand2', justify='center', command=DisMiss)
butt99.pack(side='bottom', padx=4, pady=[12, 2], fill='both')

zanyato = Label(frame_right, text='Preview area', font=('arial', 10), justify='center', borderwidth=2, relief='groove')
zanyato.pack(side='top')

frame_zoom = Frame(frame_right, width=300, borderwidth=2, relief='groove')
frame_zoom.pack(side='bottom')

butt_plus = Button(frame_zoom, text='+', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', command=zoomIn)
butt_plus.pack(side='left', padx=0, pady=0, fill='both')

butt_minus = Button(frame_zoom, text='-', font=('courier', 8), width=2, cursor='arrow', justify='center', state='disabled', command=zoomOut)
butt_minus.pack(side='right', padx=0, pady=0, fill='both')

label_zoom = Label(frame_zoom, text=f'Zoom {zoom_factor}:1', font=('courier', 8), state='disabled')
label_zoom.pack(side='left', anchor='n', padx=2, pady=0, fill='both')

sortir.mainloop()
