import json
import os
import shutil
import threading
import time
import winsound
import win32gui
import pyautogui
import tkinter as tk
import numpy as np
from datetime import date, datetime
from PIL import Image, ImageGrab
from zipfile import ZipFile
from matplotlib import colors
from matplotlib import cm
from matplotlib import pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.interpolate import interp1d

# -------------------------------------------------
# Constants
# -------------------------------------------------

default_img_path = "assets/CUOS-med.png"
date_default = {
    "year": "0001",
    "month": "01",
    "day": "01"
}
default_filename = "setup.json"


# -------------------------------------------------
# Generic Data Manipulation
# -------------------------------------------------

def get_suffix(word, delimeter):
    """ Returns the part of word after the last instance of 'delimeter' """
    while delimeter in word:
        word = word.partition(delimeter)[2]
    return word


def get_terminal_path(path):
    """
    Returns the last step of a path
    Edge cases:
    -Delimeters: / or \\ or mixed
    -Ends with delimeter or not
    """
    # Convert "\\" to "/"
    while "\\" in path:
        part = path.partition("\\")
        path = part[0] + "/" + part[2]
    if path[-1] == "/":
        path = path[0:-1]
    return get_suffix(path, "/")

# -------------------------------------------------
# Message Windows
# -------------------------------------------------
class NoticeWindow:
    '''
    GUI template for notice messages, such as progress updates
    '''

    def __init__(self, txt):
        self.root = tk.Tk()
        self.root.title("Notice")
        self.root.iconbitmap("assets/UM.ico")
        self.root.geometry("500x50")
        self.lbl = tk.Label(self.root, text=txt)
        self.lbl.pack(padx=10, pady=10)
        self.root.mainloop()


class ErrorWindow:
    """
    GUI template for error messages
    """

    def __init__(self, txt):
        self.root = tk.Tk()
        self.root.title("Error")
        self.root.iconbitmap("assets/UM.ico")
        self.root.geometry("500x50")
        self.lbl = tk.Label(self.root, text="Error: " + txt)
        self.lbl.pack()
        winsound.PlaySound("SystemExit", winsound.SND_ASYNC)
        self.root.mainloop()


# -------------------------------------------------
# Image display
# -------------------------------------------------

def plot_image(img_path, root, base=-1, colormap=cm.magma,
               vmin=0, vmax=255, flipud=False,
               display_process="Raw Image"):
    """
    Plots image using plt.imshow and tk.Canvas
    Still in development and to be tested

    Input:
        -img_path: string, filepath to plt.imread-acceptable source
        -k: float, scale factor
        -ratio: float, aspect ratio (W:H)
        -base: int, W/H dimensions at k=1.0
        -flipud: bool, whether or not to flip img vertically
    Output:
        -tuple: (tkinter Canvas of plt Figure, plt subplot)

    Note: plt subplot garbage collection must be handled on application end
    """
    # Create image plot
    img = Image.open(img_path)
    dimensions = get_from_file("dimensions", "dimensions.json")
    ratio = dimensions["ratio"]
    base_size = 2.5
    fig, plot1 = plt.subplots(1, subplot_kw={'aspect': 'auto'},
                              figsize=(ratio * base_size, base_size))
    xleft, xright = plot1.get_xlim()
    ybottom, ytop = plot1.get_ylim()
    plot1.set_aspect(abs((xright - xleft) / (ybottom - ytop)) * ratio)
    img_arr = np.asarray(img)
    if flipud:
        img_arr = np.flipud(img_arr)

    # Manage plot based on selected display process
    if display_process == "Raw Image":
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        plot1.tick_params(axis='both', which='both',
                          bottom=False, left=False, labelbottom=False,
                          labelleft=False)
        plot1.imshow(img_arr, rasterized=True, aspect='auto')
    elif display_process == "Color Map":
        plt.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01)
        plot1.tick_params(axis='both', which='both',
                          bottom=False, left=False, labelbottom=False,
                          labelleft=False)
        plot1.imshow(img_arr, vmin=vmin, vmax=vmax, cmap=colormap,
                     rasterized=True, aspect='auto')
    elif display_process == "ESPEC 1":
        plt.subplots_adjust(left=0.18, right=0.95, top=0.95, bottom=0.18)
        """ Developed by Yong Ma for daq_Yong_2021_espec_PMT.py"""
        dispersion1 = np.loadtxt('./dispersion_20210106_e1.txt')
        f1 = interp1d(dispersion1[0], dispersion1[1], fill_value='extrapolate')
        espec1_start = 0
        espec1_end = 1392
        pixels1 = np.arange(0, (espec1_end - espec1_start))
        meter_per_pixel1 = 0.2 / (1235 - 41)
        Lip_pxiel1 = pixels1 * meter_per_pixel1
        energy_itp1 = f1(Lip_pxiel1[::-1])
        lanex1totcc = 0.15
        cmap_bella = colors.LinearSegmentedColormap.from_list('cmap_bella',
                                                              ['white', 'blue', 'red', 'yellow'], 201)
        try:
            bg1 = np.mean(img_arr[50:200, espec1_start:espec1_end], axis=0)
            espec1 = img_arr[250:600, espec1_start:espec1_end] - bg1
            theta1 = np.arange(0, 600 - 250) * meter_per_pixel1 / lanex1totcc * 1000
            extent = (energy_itp1.min(), energy_itp1.max(), theta1.min(), theta1.max())
            plot1.imshow(espec1, extent=extent, vmin=vmin, vmax=vmax, cmap=cmap_bella, aspect='auto')
            plot1.set_ylabel(r'$\rm \theta \ [mrad]$')
            plot1.set_xlabel(r'Energy [MeV]')
        except ValueError:
            error_text = "Image incompatible with ESPEC 1 processing \n"
            error_text += "File path: " + img_path
            ErrorWindow(error_text)
            return
    elif display_process == "ESPEC 2":
        plt.subplots_adjust(left=0.18, right=0.95, top=0.95, bottom=0.18)
        """ Developed by Yong Ma for daq_Yong_2021_espec_PMT.py"""
        dispersion2 = np.loadtxt('./dispersion_20210106_e2.txt')
        f2 = interp1d(dispersion2[0], dispersion2[1], fill_value='extrapolate')
        espec2_start = 114
        espec2_end = 2469
        pixels2 = np.arange(0, (espec2_end - espec2_start))
        meter_per_pixel2 = 0.23 / (2654 - 495)
        Lip_pxiel2 = pixels2 * meter_per_pixel2
        energy_itp2 = f2(Lip_pxiel2[::-1])
        lanex2totcc = 0.3
        cmap_bella = colors.LinearSegmentedColormap.from_list('cmap_bella',
                                                              ['white', 'blue', 'red', 'yellow'], 201)
        try:
            bg2 = np.mean(img_arr[50:500, espec2_start:espec2_end], axis=0)
            espec2 = img_arr[400:1300, espec2_start:espec2_end] - bg2
            theta2 = np.arange(0, 1300 - 400) * meter_per_pixel2 / lanex2totcc * 1000
            extent = (energy_itp2.min(), energy_itp2.max(), theta2.min(), theta2.max())

            plot1.imshow(espec2, extent=extent, vmin=vmin, vmax=vmax, cmap=cmap_bella, aspect='auto')
            plot1.set_ylabel(r'$\rm \theta \ [mrad]$')
            plot1.set_xlabel(r'Energy [MeV]')
        except ValueError:
            error_text = "Image incompatible with ESPEC 2 processing \n"
            error_text += "File path: " + img_path
            ErrorWindow(error_text)
            return
    else:
        plot1.tick_params(axis='both', which='both',
                          bottom=False, left=False, labelbottom=False,
                          labelleft=False)
        plot1.imshow(img_arr, rasterized=True, aspect='auto')

    # Return tk.Canvas
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas = canvas.get_tk_widget()
    if base == -1:
        base = dimensions["img_size"]
    canvas.configure(width=ratio * base, height=base)
    return canvas, fig


def delete_img(img):
    '''
    Handles cleanly deleting image sources across types:
    -plt.Figure
    -PIL.PhotoImage
    -tkinter.Canvas
    -np.ndarray
    '''
    if type(img) == Figure:
        plt.close(img)
    else:
        del img


def max_num_in_dir(path):
    '''
    Returns the max numbered file in a given directory
    Expects all files in directory to be pics in convention:
    YYYYMMDD_diagnostic_s###
    '''
    pic_names = os.listdir(path)
    nums = []
    for name in pic_names:
        pic = name.partition(".")[0]
        pic = pic.partition("_s")[2]
        try:
            pic = int(pic)
            nums.append(pic)
        except:
            ErrorWindow("Bad filename: " + name)
    if (len(nums) == 0):
        return None
    else:
        return max(nums)


def to_3_digit(num):
    '''
    Returns a 3-digit string of the input positive int
    Returns '999' if num is more than three digits
    Returns '000' if num is negative
    '''
    num = int(num)
    if (num < 0):
        return "000"
    elif (num >= 999):
        return "999"
    elif (num > 99):
        return str(num)
    elif (num > 9):
        return "0" + str(num)
    else:
        return "00" + str(num)


def get_shot_num(path):
    ''' Returns the shot number (in str) of an image at path 'path' '''
    if ("_s" in path):
        out = path.partition("_s")[2]
    elif ("shot" in path):
        out = path.partition("shot")[2]
    else:
        out = path
    out = out.partition(".")[0]
    return out


# -------------------------------------------------
# File management
# -------------------------------------------------

def get_from_file(key, filename=default_filename):
    '''
    Returns value of key in dict stored in filename
    File must be .json and contain only a dict
    '''
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    if not key in data.keys():
        ErrorWindow('Key "' + key + '" does not exist.')
        return ""
    return data[key]


def edit_file(key, value, filename=default_filename):
    '''
    Sets value of key in dict stored in filename
    File must be .json and contain only a dict
    '''
    with open(filename, "r") as read_file:
        data = json.load(read_file)
    if not key in data.keys():
        ErrorWindow('Key "' + key + '" does not exist.')
        return ""
    data[key] = value
    with open(filename, "w") as write_file:
        json.dump(data, write_file)


def save_most_recent(src, dest, diag, num,
                     extensions=["png", "jpg", "jpeg", "tif", "tiff"]):
    '''
    Copies the most recently edited file in the source directory into the
    destination
    
    Inputs:
    -src: string, source file
    -dest: string, destination directory
    -diag: string, name of diagnostic
    -num: int/string, shot number
    -extensions: list of strings, supported file types
    '''
    # Identify most recent file
    files = os.listdir(src)
    new_files = []
    for file in files:
        ext = get_suffix(file, ".").lower()
        if ext in extensions:
            new_files.append(src + "/" + file)
            continue
    path = max(new_files, key=os.path.getctime)
    num = to_3_digit(num)

    # Copy raw data
    ext = get_suffix(path, ".")
    today = get_today()
    name = diag + "_" + today.strftime("%Y%m%d")
    name += "_s" + to_3_digit(num) + "." + ext
    shutil.copy(path, os.path.join(dest, name))


def get_today():
    '''
    Returns a datetime.date object representing today.
    If there has been a date set manually, it uses that.
    Otherwise, it uses date.today()
    '''
    today = get_from_file("date", "setup.json")
    if (today != date_default):
        y = int(today["year"])
        m = int(today["month"])
        d = int(today["day"])
        return date(y, m, d)
    else:
        return date.today()

def get_timestamp():
    """ Returns filepath-friendly timestamp """
    timestamp = str(datetime.now())
    while ":" in timestamp:
        partition = timestamp.partition(":")
        timestamp = partition[0] + "-" + partition[2]
    return timestamp


def save_plots(num, shotrundir, book):
    '''
    Saves a screenshot, cropped to include only the recent display

    Inputs:
    -num: int/str, shot number
    -shotrundir: str, shot run directory
    -delay: numeral, seconds to delay before taking screenshot
    '''

    # Define threads
    def thread_a(book):
        """ Switches tab to Recent Image Display """
        book.select('.!frame.!notebook.!frame5')

    def thread_b(num, shotrundir, delay):
        """ Saves screenshot """
        # Delay to leave time for tab switching
        time.sleep(delay)

        # Take and crop screenshot
        img = ImageGrab.grab()

        def windowEnumerationHandler(hwnd, top_windows):
            top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

        # Set active window
        top_windows = []
        win32gui.EnumWindows(windowEnumerationHandler, top_windows)
        window_name = "Data Acquisition and Display"
        for i in top_windows:
            if window_name in i[1]:
                win32gui.ShowWindow(i[0], 5)
                try:
                    win32gui.SetForegroundWindow(i[0])
                except:
                    pass
                break

        # Save screenshot to clipboard
        pyautogui.keyDown("alt")
        pyautogui.press("printscreen")
        pyautogui.keyUp("alt")

        # Generate file name
        dest = os.path.join(shotrundir, "Aggregated Plots")
        if not (os.path.isdir(dest)):
            os.mkdir(dest)
        filename = "plot_agg_s" + to_3_digit(num)
        ext = ".png"
        # Check for duplicates
        if os.path.isfile(os.path.join(dest, filename) + ext):
            # Add "_v#" tag for alternate save
            base = os.path.join(dest, filename)
            base = base.partition(ext)[0]
            tag = "_v"
            num = 1
            while os.path.isfile(base + tag + str(num) + ext):
                num += 1
            filename += tag + str(num)
        filename += ext

        # Save screenshot to disk
        im = ImageGrab.grabclipboard()
        if isinstance(im, Image.Image):
            im.save(os.path.join(dest, filename))

    # Get dimensions
    dimensions = get_from_file("dimensions", "dimensions.json")
    delay = dimensions["time_delay"]

    # Operate
    t1 = threading.Thread(target=thread_b, args=(num, shotrundir, delay))
    t1.start()
    thread_a(book)

def zip_shot_run_dir():
    """
    Compresses the shot run directory into .zip files by shot num and returns folder path
    Folder: ./(shotrundir)/Zipped_Shots_(shotrundir name)
    .zip files: (shotrundir name)_shot###
    Files within .zip files: diagnostic_shot### (same name as origin)
    """
    shotrundir = get_from_file("shotrundir")
    shotrundir_name = get_terminal_path(shotrundir)

    # Make zipped shots folder
    folder_name = os.path.join(shotrundir, "Zipped_Shots_" + shotrundir_name)
    if not os.path.isdir(folder_name):
        os.mkdir(folder_name)
    else:
        folder_num = 2
        while True:
            new_name = folder_name + "_" + str(folder_num)
            if not os.path.isdir(new_name):
                folder_name = new_name
                os.mkdir(folder_name)
                break
            folder_num += 1

    # Get files zipped
    shot_num = 1
    while True:
        shot_num_str = "s" + to_3_digit(shot_num)
        files_of_shot = []
        for diagnostic in os.listdir(shotrundir):
            diagnostic = os.path.join(shotrundir, diagnostic)
            if "Zipped_Shots_" in diagnostic:
                print("continue for zipped shots: ", diagnostic)
                continue
            if not os.path.isdir(diagnostic):
                print("continue for invalid path: ", diagnostic)
                continue
            # Identify all shots of this number in the diagnostic
            files = os.listdir(diagnostic)
            files_of_shot_in_diagnostic = []
            for file_name in files:
                if shot_num_str in file_name:
                    file_name = os.path.join(diagnostic, file_name)
                    files_of_shot_in_diagnostic.append(file_name)
            # Identify most recent version of shot number
            if len(files_of_shot_in_diagnostic) > 1:
                file_of_shot = max(files_of_shot_in_diagnostic, key=os.path.getctime)
                file_of_shot_path = os.path.join(shotrundir, diagnostic, file_of_shot)
                files_of_shot.append(file_of_shot_path)
            elif len(files_of_shot_in_diagnostic) == 1:
                file_of_shot = files_of_shot_in_diagnostic[0]
                file_of_shot_path = os.path.join(shotrundir, diagnostic, file_of_shot)
                files_of_shot.append(file_of_shot_path)
            else:
                print("No valid files")

        # Exit
        if not files_of_shot:
            break
        print("files of shot:")
        for file in files_of_shot:
            print(file)

        # Zip files
        shot_folder_name = shotrundir_name + "_Shot"
        shot_folder_name += to_3_digit(shot_num)
        shot_folder_name = os.path.join(folder_name, shot_folder_name)
        for file_path in files_of_shot:
            file_name = get_suffix(file_path, "\\")
            file_name = os.path.join(folder_name, file_name)
            shutil.copy(file_path, file_name)
        zip_file = ZipFile(shot_folder_name + ".zip", "w")
        base_dir = os.getcwd()
        os.chdir(folder_name)
        for file in os.listdir("./"):
            if ".zip" not in file:
                print("Added: ", file)
                zip_file.write(file)
                os.remove(file)
        os.chdir(base_dir)
        zip_file.close()
        shot_num += 1

    print(folder_name)
    return folder_name

    # Identify ".." of folder_name
    suffix = get_terminal_path(folder_name)
    return folder_name.partition(suffix)[0]
    #return folder_name
