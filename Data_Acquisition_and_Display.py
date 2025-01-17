import Startup
import Sidebar_Dialog
import Helpers
import Menu_Bar
import Main_tab
import Diagnostic_Parameters
import Image_Display_Single
import Image_Display_Newest
import Upload_Settings
import Save_Controls

from tkinter import ttk
import tkinter as tk
import sys


# -------------------------------------------------
# GUI
# -------------------------------------------------

class AcquisitionDisplay:
    '''
    Master top-level GUI for data acquisition and display
    '''

    def __init__(self):
        Startup.startup(self)

        self.root = tk.Tk()
        self.root.title("Data Acquisition and Display")
        self.root.iconbitmap("assets/UM.ico")
        self.root.state('zoomed')

        self.update_funcs = []
        self.workspace_load_funcs = []
        self.workspace_save_funcs = []

        # Organization
        self.fr_sidebar = Sidebar_Dialog.UI(self.root)
        self.fr_sidebar.grid(row=0, column=1)

        self.bookframe = tk.Frame()
        self.bookframe.grid(row=0, column=0)
        self.book = ttk.Notebook(self.bookframe)

        self.tab_main = ttk.Frame(self.book)
        self.tab_diag_params = ttk.Frame(self.book)
        self.tab_single_image = ttk.Frame(self.book)
        self.tab_montage = ttk.Frame(self.book)
        self.tab_newest = ttk.Frame(self.book)
        self.tab_upload = ttk.Frame(self.book)

        self.book.add(self.tab_main, text="Main")
        self.book.add(self.tab_diag_params, text="Diagnostic Parameters")
        self.book.add(self.tab_single_image, text="Single Image Display")
        self.book.add(self.tab_newest, text="Recent Image Display")
        self.book.add(self.tab_upload, text="Upload Settings")

        self.book.pack(expand=1, fill="both")

        # Imported Widgets
        self.fr_main = Main_tab.UI(self.tab_main)
        self.fr_main.pack()

        self.fr_single_image = Image_Display_Single.UI(self.tab_single_image)
        self.fr_single_image.pack()
        self.update_funcs.append(self.fr_single_image.update_all)
        self.add_wksp_funcs(self.fr_single_image)

        self.fr_recent_image = Image_Display_Newest.UI(self.tab_newest)
        self.fr_recent_image.pack()
        self.update_funcs.append(self.fr_recent_image.update_diagnostics)

        self.fr_upload = Upload_Settings.UI(self.tab_upload)
        self.fr_upload.pack()

        ''' Parameter frames loaded last to allow passing full update_funcs '''
        self.fr_diag_params = Diagnostic_Parameters.UI(self.tab_diag_params,
                                                       self.update_funcs)
        self.fr_diag_params.pack()
        self.add_wksp_funcs(self.fr_diag_params)

        wksp_diag = self.fr_diag_params.get_workspace
        self.fr_save = Save_Controls.UI(self.root, wksp_diag, self.update_funcs, self.book)
        self.fr_save.grid(row=1, column=0)

        # File Menu
        '''
        Identical in function to General Parameters, but uses a dropdown
        file menu instead of a whole frame
        '''
        self.menubar = Menu_Bar.UI(self.root, self.workspace_load_funcs,
                                   self.workspace_save_funcs, self.update_funcs)
        self.root.config(menu=self.menubar)

    def add_wksp_funcs(self, frame):
        '''
        Adds functions for saving and loading workspace data for a
        particular tab's frame
        '''
        load = frame.load_from_workspace
        self.workspace_load_funcs.append(load)
        save = frame.get_workspace
        self.workspace_save_funcs.append(save)

    def open(self):
        self.root.mainloop()

    def close(self):
        self.root.quit()
        quit()


# -------------------------------------------------
# Execution
# -------------------------------------------------

if __name__ == "__main__":
    '''
    Example code for running the GUI
    '''
    acq = AcquisitionDisplay()
    try:
        acq.open()
    except:
        acq.close()
        # Doesn't catch errors inside mainloop
        error_message = "(unhandled) " + str(sys.exc_info()[0])
        error_message += "\nClosed Data Acquisition and Display"
        Helpers.ErrorWindow(error_message)
