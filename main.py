import datetime
import inspect
import tkinter as tk
from tkinter import *
from tkinter import messagebox

import settings

# Global BOOLVar to check if data was pasted or downloaded
notams = []  # Global list for NOTAMs
today = (datetime.datetime.now().strftime("%y%m%d"))  # Todays date
lst = []
AIRPORTS = []  # List of Airports to download
downloaded = []
database = []
'''
zip(ICAO, NOTAM[], dateofdownload)
'''
# def ticker():
#     for AIRPORT in AIRPORTS:
#
# def downloadNOTAMs(AIRPORT):
#

with settings.Settings() as settings:
    pass


class NotamClass(object):
    def __init__(self, val: str, startdate: str, enddate: str, PERM: bool = None, EST: bool = None):
        """
        This is a class for NOTAM atributes.

        Attributes:
            val (str): The value of NOTAM.
            startdate : The date in B) of NOTAM. This method converts it to datetime.date type.
            enddate : The date in C) of NOTAM. This method converts it to datetime.date type.
            PERM (bool): The BOOL value of Permament of NOTAM.
            EST (bool): The BOOL value of Estimated time of NOTAM.
        Methods:
            convertShort(date: str): converts 10 elements string with date to datetime.data format
            convertLong(date: str: converts 24 elements string with date to datetime.data format
            setPERM(optional val: bool): sets value of NOTAM object PERM attribute to val or True if empty
            setEST(optional val: bool): sets value of NOTAM object EST attribute to val or True if empty
        """
        self.val = val
        self.PERM = PERM
        self.EST = EST
        if len(str(startdate)) == 24:
            self.startdate = self.convertLong(startdate)
        if len(str(enddate)) == 24:
            self.enddate = self.convertLong(enddate)
        if len(str(startdate)) == 10:
            self.startdate = self.convertShort(startdate)
            self.enddate = self.convertShort(enddate)

    def convertShort(self, date: str) -> datetime.date:
        return datetime.date(int(str(20) + str(date[0:2])), int(date[2:4]), int(date[4:6]))

    def convertLong(self, date: str) -> datetime.date:
        return datetime.date(int(str(20) + date[2:4]), int(date[5:7]), int(date[8:10]))

    def setPERM(self, val: bool = True):
        self.PERM = val

    def setEST(self, val: bool = True):
        self.EST = val

    def printNOTAM(self):  #
        gui.entry.text.insert(END, self.val + '\n\n')

    # TODO: Zrobić metodę do wrzucania do entry


class DataB(object):
    def __init__(self, ICAOcode, notamy):
        self.ICAOcode = ICAOcode
        self.notamy = notamy


class TextFrame(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        self.text = tk.Text(self, wrap="word", width=50, height=60)
        ysb = tk.Scrollbar(self, orient="vertical", command=self.text.yview)
        self.text.configure(yscrollcommand=ysb.set)
        ysb.grid(row=0, column=1, sticky="ns")
        self.text.grid(row=0, column=0, sticky="nsew")
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.text.bind("<Any-KeyRelease>", self.highlight)
        self.text.bind("<Any-ButtonRelease>", self.highlight)
        self.text.bind("<Enter>", self.highlight)

    def highlight(self, event=None):
        self.readOnly()
        self.text.tag_remove("keyword", 1.0, 'end')
        self.text.tag_configure("keyword", background='yellow', relief='raised')
        keywords = gui.get_tags()
        if keywords:
            keywordstags = list(filter(None, keywords.split(" ")))  # Deleting empty elements from Keywordtags list
            for x in keywordstags:
                index = '1.0'
                while index:
                    index = self.text.search(x, index, nocase=True, stopindex=END)
                    if index:
                        lastindex = '%s+%dc' % (index, len(x))
                        self.text.tag_add("keyword", index, lastindex)
                        index = lastindex

    def readOnly(self, event=None):
        if event is None:
            # Read-only if NOTAMs were downloaded
            if gui.download_flag.get() == False:
                self.text.config(state=NORMAL)
            else:
                self.text.config(state=DISABLED)
        if event is 'Normal':
            self.text.config(state=NORMAL)
        elif event is 'Disabled':
            self.text.config(state=DISABLED)


def remove(string):
    return string.replace(" ", "")


def check_NOTAM(datefrom, dateto, notamfrom, notamto):
    if (datefrom <= notamfrom and dateto >= notamto) or (
            datefrom <= notamfrom <= dateto <= notamto) or (
            notamfrom <= datefrom <= notamto <= dateto) or (
            notamfrom <= datefrom <= notamto and dateto <= notamto):
        return True
    else:
        return False


class NotamDownloadClass:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.master.title("Download")
        self.master.resizable(width=False, height=False)
        self.master.lift()
        self.master.focus_force()
        self.label_download = Label(self.frame, text="ICAO:").pack(side=LEFT)

        self.master.bind("<Escape>", (lambda event: gui.on_tl_close()))  # Closing window with ESC button

        global searchbuttontext
        self.searchbuttontext = tk.StringVar()
        self.searchbuttontext.set("Download NOTAM / Enter")
        self.aprtcode = Entry(self.frame, width=6)
        self.aprtcode.pack(side=LEFT)
        self.aprtcode.bind('<Return>', (lambda event: self.notam_download(self.aprtcode.get())))
        self.aprtcode.focus()
        self.searchbutton = Button(self.frame, textvariable=self.searchbuttontext, width=20,
                                   command=lambda: self.notam_download(self.aprtcode.get())).pack(side=LEFT)
        self.frame.mainloop()

    def notam_download(self, aprt_to_download, *args):
        stack = inspect.stack()  # Function to check what class called this function

        gui.entry.readOnly('Normal')
        gui.entry.text.delete('1.0', END)
        downloaded = []
        notamloc = []
        print(aprt_to_download)
        if not aprt_to_download in gui.AIRPORTS:
            gui.scrollbar['menu'].add_command(label=aprt_to_download, command=tk._setit(gui.variable, aprt_to_download))
            gui.AIRPORTS.append(aprt_to_download)
        for obj in database:
            if obj.notamy != []:
                downloaded.append(obj.ICAOcode)
        if not aprt_to_download in downloaded or stack[1][0].f_locals[
            "self"].__class__.__name__ == "NotamDownloadClass":  #
            if len(aprt_to_download) == 4:
                import requests
                import json
                gui.entry.readOnly('Normal')
                # entry.text.delete('1.0', END)
                gui.entry.text.insert(END, "Downloading " + aprt_to_download + " NOTAMS...")
                gui.entry.text.update()
                if remove(settings.ICAO_API_key) == "":
                    tk.messagebox.showwarning("Warning",
                                              "You are downloading NOTAMS from ICAO API without API KEY\nAdd your API KEY in Settings")
                params = {
                    'api_key': settings.ICAO_API_key,
                    'format': 'json',
                    'criticality': '',
                    'locations': aprt_to_download
                }
                icao_URL = settings.ICAO_URL
                count = 0
                json_data = []
                while (json_data == [] and count < 5):
                    response = requests.get(icao_URL, params=params)
                    json_data = json.loads(response.text)
                    count += 1
                    gui.entry.text.insert(END, "\nAttempt " + str(count))
                    gui.entry.text.update()
                if (json_data == [] or response.status_code != 200):
                    tk.messagebox.showerror("Error", "Error occurred while downloading data from ICAO API")
                    try:
                        searchbuttontext.set("Error. Try again")
                    except:
                        pass
                gui.entry.text.delete('1.0', END)  # NOTAMs downloaded
                notamloc.clear()
                for x in json_data:
                    notamloc.append(NotamClass(x['all'], x['startdate'], x['enddate']))
                try:
                    searchbuttontext.set("Download Done")
                except:
                    pass
                database.append(DataB(aprt_to_download, notamloc))
            else:
                tk.messagebox.showerror(title="Error", message="Enter Airport ICAO code you want to download")
                self.master.lift()
                self.master.focus_force()
                self.aprtcode.focus()
                return
        else:
            notamloc = database[downloaded.index(aprt_to_download)].notamy
        for i in range(len(notamloc)):
            notamloc[i].printNOTAM()
        gui.download_flag.set(True)  # Setting download flag to true
        gui.entry.readOnly('Disabled')
        global notams
        notams = notamloc


# TODO: Zrobić listę NOTAMów do pobrania w tle


class SettingWindowClass:
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.buttontext = tk.StringVar()
        self.buttontext.set("Save settings")

        self.master.title("NOTAM setting")
        self.master.resizable(width=False, height=False)
        Label(self.frame, text="ICAO API key").grid(row=0, column=0)
        Label(self.frame, text="Default Tags").grid(row=1, column=0)
        Label(self.frame, text="ICAO airports to download").grid(row=2, column=0)
        self.icaoapikey = Entry(self.frame, width=45)
        self.icaoapikey.grid(row=0, column=1)
        self.icaoapikey.insert(0, settings.ICAO_API_key)
        self.defaulttags = Entry(self.frame, width=45)
        self.defaulttags.grid(row=1, column=1)
        self.defaulttags.insert(0, settings.DefaultTags)
        self.defaultAIRPORTS = Entry(self.frame, width=45)
        self.defaultAIRPORTS.grid(row=2, column=1)
        self.defaultAIRPORTS.insert(0, settings.DefaultAIRPORTS)
        global AIRPORTS
        AIRPORTS = self.defaultAIRPORTS.get().split(" ")
        self.master.bind("<Escape>", (lambda event: gui.on_tl_close()))  # Closing window with ESC button

        Button(self.frame, textvariable=self.buttontext, width=20,
               command=lambda: self.savesettings(self.icaoapikey.get(), self.defaulttags.get(),
                                                 self.defaultAIRPORTS.get())).grid(row=3, column=1)

    def savesettings(self, ICAO_API_key, DefaultTags, DefaultAIRPORTS):
        settings.ICAO_API_key = ICAO_API_key
        settings.DefaultTags = DefaultTags
        settings.DefaultAIRPORTS = DefaultAIRPORTS
        settings.exit()
        gui.getAIRPORTs()
        self.buttontext.set("Saved.")


class MainWin(tk.Frame, NotamDownloadClass):
    def __init__(self, parent, controller):
        self.parent = parent
        Frame.__init__(self, parent)
        self.options_toplevel = None
        self.controller = controller
        # Defining  Variables
        self.ESTvar = BooleanVar()
        self.ESTvar.set(True)

        self.PERMvar = BooleanVar()
        self.PERMvar.set(True)

        self.download_flag = BooleanVar()
        self.download_flag.set(False)
        global downloaded  # temporary #TODO: Naprawić aby to nie był global
        global database
        if len(database) > 0:
            print("0", database[0].notamy)

        self.initUI()
        self.menubar(self.controller)
        self.boxes()
        self.entryboxes()
        self.buttons()
        self.labels()
        self.listtest()
        self.getAIRPORTs()

    def initUI(self):
        self.parent.title("NOTAM downloader and NOTAM filter")
        self.parent.resizable(width=False, height=True)
        self.pack()

    def listtest(self):
        self.AIRPORTS = settings.DefaultAIRPORTS.split(" ")
        self.variable = StringVar(self)
        self.variable.set("Choose Airport")  # default value
        self.scrollbar = OptionMenu(self, self.variable, *self.AIRPORTS)
        self.variable.trace("w", self.showAirports)
        self.scrollbar.grid(row=1, column=0, sticky=W, padx=5)
        self.scrollbar.config(bg="WHITE")

    def getAIRPORTs(self, *args):
        self.AIRPORTS = settings.DefaultAIRPORTS.split(" ")
        self.scrollbar['menu'].delete(0, 'end')
        for AIRPORT in self.AIRPORTS:
            self.scrollbar['menu'].add_command(label=AIRPORT, command=tk._setit(self.variable, AIRPORT))

    def showAirports(self, *args):
        self.notam_download(self.variable.get())

    def menubar(self, controller):
        menubar = Menu(controller)
        menu = Menu(menubar, tearoff=0)
        menu.add_checkbutton(label="Always EST", onvalue=1, offvalue=0, variable=self.ESTvar)
        menu.add_checkbutton(label="Always PERM", onvalue=1, offvalue=0, variable=self.PERMvar)
        menu.add_checkbutton(label="NOTAMs downloaded from ICAO", onvalue=1, offvalue=0, variable=self.download_flag,
                             command=self.download_change)
        menu.add_command(label="Settings...", command=self.new_window_settings)
        menubar.add_cascade(label="File", menu=menu)
        controller.config(menu=menubar)

    def boxes(self):
        # global entry
        # global output
        self.entry = TextFrame(self)
        self.entry.grid(row=2, column=0)
        self.output = TextFrame(self)
        self.output.grid(row=2, column=3)

    def entryboxes(self):
        self.entrydate1 = Entry(self, width=6)
        self.entrydate1.insert(END, today)
        self.entrydate1.bind("<FocusOut>", self.from_insert_to_focus_out)
        self.entrydate2 = Entry(self, width=6, bg='white', fg='grey')
        self.entrydate2.bind("<FocusIn>", self.insert_to_focus_in)
        self.entrydate2.bind("<FocusOut>", self.insert_to_focus_out)
        self.entrydate2.bind("<Return>", (lambda event: self.handle_enter()))
        self.entrydate2.insert(0, "UFN")
        self.entrykeywords = Entry(self, width=35)
        self.entrykeywords.insert(END, settings.DefaultTags)
        self.entrydate1.grid(row=0, column=0, sticky=E, padx=75)
        self.entrydate2.grid(row=0, column=0, sticky=E, padx=0)
        self.entrykeywords.grid(row=0, column=0, sticky=W, padx=5)

    def buttons(self):
        Button(self, text="NOTAM FILTR", width=20, command=self.finder).grid(row=0, column=3, padx=20, sticky=E)
        Button(self, text="Force NOTAM download", width=20, command=self.new_window_download).grid(row=0, column=3,
                                                                                                   padx=0, sticky=W)

    def finder(self):
        self.output.readOnly('Normal')
        self.output.text.delete('1.0', END)
        self.output.text.config
        self.output.text.update()
        x = []
        y = []
        z = []
        B = []
        C = []
        lst = []
        notamtext = []
        if gui.get_entrydate2() == "" or gui.get_entrydate2() == "UFN":
            dateto = datetime.date(2999, 1, 1)
        else:
            to = gui.get_entrydate2()
            dateto = datetime.date(int(str(20) + to[0:2]), int(to[2:4]), int(to[4:6]))
        frm = gui.get_entrydate1()
        datefrom = datetime.date(int(str(20) + frm[0:2]), int(frm[2:4]), int(frm[4:6]))
        re = gui.entry.text.get("1.0", END)
        if (gui.download_flag.get() == False and remove(re).rstrip(
                "\n") != ''):  # Check if there are any values(notams) in left textbox and if the download_flag is
            # set to True
            notams.clear()
            notamtext.clear()
            notamtext.extend(re.split("\n\n"))
        elif (remove(re).rstrip("\n") == ''):
            tk.messagebox.showerror("Error", "Brak NOTAMów")
        if gui.download_flag.get() == True:
            for i in range(len(notams)):
                notamtext.append(notams[i].val)
        for i in range(len(notamtext)):
            x.append(notamtext[i].find("B)"))
            y.append(notamtext[i].find("C)"))
            if notamtext[i].find("D)") < 0:
                z.append(notamtext[i].find("E)"))
            else:
                z.append(notamtext[i].find("D)"))
            if (int(z[i] - 1) - int(y[i] + 2)) > 14:  # Protection for maximum elements in C) Date
                z[i] = int(y[i] + 2) + 14
            B.append(remove(notamtext[i][int(x[i] + 2):int(y[i] - 1)]))
            C.append(remove(notamtext[i][int(y[i] + 2):int(z[i] - 1)]))
            if C[i] == "PERM":
                if gui.download_flag.get() == True:
                    notams[i].setPERM()
                else:
                    notams.append(NotamClass(notamtext[i], B[i], str(9912312359), True, False))
            elif C[i][-3:] == "EST" or C[i][-1:] == "E":
                if gui.download_flag.get() == True:
                    notams[i].setEST()
                else:
                    notams.append(NotamClass(notamtext[i], B[i], C[i], False, True))
            else:
                if gui.download_flag.get() == False:
                    notams.append(NotamClass(notamtext[i], B[i], C[i], False, False))
        for i in range(len(notams)):
            if notams[i].PERM == True:
                if gui.PERMvar.get() == 1:
                    lst.append(notams[i].val)
                    lst.append(" ")
            elif notams[i].EST == True:
                if gui.ESTvar.get() == 1:
                    lst.append(notams[i].val)
                    lst.append(" ")
                else:
                    if (check_NOTAM(datefrom, dateto, notams[i].startdate, notams[i].enddate)):
                        lst.append(notams[i].val)
                        lst.append(" ")
            else:
                if (check_NOTAM(datefrom, dateto, notams[i].startdate, notams[i].enddate)):
                    lst.append(notams[i].val)
                    lst.append(" ")
        for a in lst:
            gui.output.text.insert(END, a + '\n')
        gui.output.readOnly('Disabled')

    def labels(self):
        l1 = Label(self, text="From:").grid(row=0, column=0, sticky=E, padx=125)
        l2 = Label(self, text="To:").grid(row=0, column=0, sticky=E, padx=50)

    def insert_to_focus_in(self, *args):
        self.entrydate2.delete(0, tk.END)
        self.entrydate2.config(fg='black')

    def insert_to_focus_out(self, *args):
        if (self.entrydate2.get() == ""):
            self.entrydate2.delete(0, tk.END)
            self.entrydate2.config(fg='grey')
            self.entrydate2.insert(0, "UFN")

    def from_insert_to_focus_out(self, *args):
        if (self.entrydate1.get() == ""):
            self.entrydate1.insert(END, today)

    def handle_enter(self):
        self.focus()

    def download_change(self):
        if gui.download_flag.get() == False and (
                remove(gui.entry.text.get("1.0", END)).rstrip("\n") != '' or remove(
            gui.output.text.get("1.0", END)).rstrip(
            "\n") != ''):
            MsgBox = tk.messagebox.askquestion('Download Flag change', 'This action will clear entry and output '
                                                                       'boxes. Are you sure?',
                                               icon='warning')
            if MsgBox == 'yes':
                gui.entry.text.config(state=NORMAL)
                gui.output.text.config(state=NORMAL)
                gui.entry.text.delete('1.0', END)
                gui.output.text.delete('1.0', END)
            if MsgBox == 'no':
                gui.download_flag.set(True)  # Setting download flag to true

    def get_entrydate1(self):
        return self.entrydate1.get()

    def get_entrydate2(self):
        return self.entrydate2.get()

    def get_tags(self):
        return self.entrykeywords.get()

    def new_window_settings(self, *args):
        if self.options_toplevel is None:
            self.options_toplevel = tk.Toplevel(self.master)
            self.options_toplevel.protocol('WM_DELETE_WINDOW', self.on_tl_close)
            self.app1 = SettingWindowClass(self.options_toplevel)

    def new_window_download(self, *args):
        if self.options_toplevel is None:
            self.options_toplevel = tk.Toplevel(self.master)
            self.options_toplevel.protocol('WM_DELETE_WINDOW', self.on_tl_close)
            self.app2 = NotamDownloadClass(self.options_toplevel)

    def on_tl_close(self, *args):
        self.options_toplevel.destroy()
        self.options_toplevel = None


def main():
    global gui
    win = Tk()
    gui = MainWin(win, win)
    gui.pack()
    win.mainloop()


if __name__ == '__main__':
    main()
