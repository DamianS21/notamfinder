import datetime
import settings
import tkinter as tk
from tkinter import messagebox
from tkinter import *

# Global BOOLVar to check if data was pasted or downloaded
notam = []  # Global list for NOTAMs strings
today = (datetime.datetime.now().strftime("%y%m%d"))  # Todays date
lst = []

with settings.Settings() as settings:
    pass


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
        # Read-only if NOTAMs were downloaded
        if download_flag.get() == False:
            self.text.config(state=NORMAL)
        else:
            self.text.config(state=DISABLED)

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


def finder():
    output.text.delete('1.0', END)
    output.text.update()
    lst = []
    x = []
    y = []
    z = []
    B = []
    C = []
    datesB = []
    datesC = []
    if (gui.get_entrydate2() == "" or gui.get_entrydate2() == "UFN"):
        dateto = datetime.date(2999, 1, 1)
    else:
        to = gui.get_entrydate2()
        dateto = datetime.date(int(str(20) + to[0:2]), int(to[2:4]), int(to[4:6]))
    frm = gui.get_entrydate1()
    datefrom = datetime.date(int(str(20) + frm[0:2]), int(frm[2:4]), int(frm[4:6]))

    re = entry.text.get("1.0", END)
    if (download_flag.get() == False and remove(re).rstrip(
            "\n") != ''):  # Check if there are any values(notams) in left textbox and if the download_flag is set to True
        notam.clear()
        notam.extend(re.split("\n\n"))
    elif (remove(re).rstrip("\n") == ''):
        tk.messagebox.showerror("Error", "Brak NOTAMów")

    for i in range(len(notam)):
        x.append(notam[i].find("B)"))
        y.append(notam[i].find("C)"))
        if notam[i].find("D)") < 0:
            z.append(notam[i].find("E)"))
        else:
            z.append(notam[i].find("D)"))
        if (int(z[i] - 1) - int(y[i] + 2)) > 14:  # Protection for maximum elements in C) Date
            z[i] = int(y[i] + 2) + 14
        B.append(remove(notam[i][int(x[i] + 2):int(y[i] - 1)]))
        C.append(remove(notam[i][int(y[i] + 2):int(z[i] - 1)]))
        datesB.append(datetime.date(int(str(20) + B[i][0:2]), int(B[i][2:4]), int(B[i][4:6])))
        if C[i] == "PERM":
            datesC.append(datetime.date(9999, 1, 1))
            if PERMvar.get() == 1:
                lst.append(notam[i])
                lst.append(" ")
        elif C[i][-3:] == "EST" or C[i][-1:] == "E":
            datesC.append(datetime.date(int(str(20) + C[i][0:2]), int(C[i][2:4]), int(C[i][4:6])))
            if ESTvar.get() == 1:
                lst.append(notam[i])
                lst.append(" ")
            else:
                datesC.append(datetime.date(int(str(20) + C[i][0:2]), int(C[i][2:4]), int(C[i][4:6])))
                if (check_NOTAM(datefrom, dateto, datesB[i], datesC[i])):
                    lst.append(notam[i])
                    lst.append(" ")
        else:
            datesC.append(datetime.date(int(str(20) + C[i][0:2]), int(C[i][2:4]), int(C[i][4:6])))
            if (check_NOTAM(datefrom, dateto, datesB[i], datesC[i])):
                lst.append(notam[i])
                lst.append(" ")
    for x in lst:
        output.text.insert(END, x + '\n')


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
        global searchbuttontext
        searchbuttontext = tk.StringVar()
        searchbuttontext.set("Download NOTAM / Enter")
        aprtcode = Entry(self.frame, width=6)
        aprtcode.pack(side=LEFT)
        aprtcode.bind('<Return>', (lambda event: self.notam_download(aprtcode.get())))
        aprtcode.focus()

        self.searchbutton = Button(self.frame, textvariable=searchbuttontext, width=20,
                                   command=lambda: self.notam_download(aprtcode.get())).pack(side=LEFT)
        self.frame.mainloop()

    def notam_download(self, aprt_to_download):
        import requests
        import json
        entry.text.insert(END, "Downloading " + aprt_to_download + " NOTAMS...")
        entry.text.update()
        if remove(settings.ICAO_API_key) == "":
            tk.messagebox.showwarning("Warning",
                                      "You are downloading NOTAMS from ICAO API without API KEY\nAdd your API KEY in Settings")
        params = {
            'api_key': settings.ICAO_API_key,
            'format': 'json',
            'criticality': '',
            'locations': aprt_to_download
        }
        icao_URL = 'https://v4p4sz5ijk.execute-api.us-east-1.amazonaws.com/anbdata/states/notams/notams-realtime-list'
        response = requests.get(icao_URL, params=params)
        json_data = json.loads(response.text)
        if json_data == [] or response.status_code != 200:
            tk.messagebox.showerror("Error", "Error occurred while downloading data from ICAO API")
            searchbuttontext.set("Error. Try again")
            return
        entry.text.delete('1.0', END)
        notam.clear()
        for x in json_data:
            entry.text.insert(END, x['all'] + '\n\n')
            notam.append(x['all'])
        download_flag.set(True)  # Setting download flag to true
        searchbuttontext.set("Download Done")


class SettingWindowClass:  # TODO: Zrobić zmianę przycisku na "Saved" po zapisie
    def __init__(self, master):
        self.master = master
        self.frame = tk.Frame(self.master)
        self.frame.pack()

        self.master.title("NOTAM setting")
        self.master.resizable(width=False, height=False)
        Label(self.frame, text="ICAO API key").grid(row=0, column=0)
        Label(self.frame, text="Default Tags").grid(row=1, column=0)
        self.icaoapikey = Entry(self.frame, width=45)
        self.icaoapikey.grid(row=0, column=1)
        self.icaoapikey.insert(0, settings.ICAO_API_key)
        self.defaulttags = Entry(self.frame, width=45)
        self.defaulttags.grid(row=1, column=1)
        self.defaulttags.insert(0, settings.DefaultTags)
        Button(self.frame, text="Save settings", width=20,
               command=lambda: self.savesettings(self.icaoapikey.get(), self.defaulttags.get())).grid(row=2, column=1)

    def savesettings(self, icaoapikey, defaulttags):
        settings.ICAO_API_key = icaoapikey
        settings.DefaultTags = defaulttags
        settings.exit()


class MainWin(tk.Frame):
    def __init__(self, parent, controller):
        self.parent = parent
        Frame.__init__(self, parent)
        self.options_toplevel = None
        self.controller = controller
        # Defining global Variables
        global ESTvar
        ESTvar = BooleanVar()
        ESTvar.set(True)
        global PERMvar
        PERMvar = BooleanVar()
        PERMvar.set(True)
        global download_flag
        download_flag = BooleanVar()
        download_flag.set(False)

        self.initUI()
        self.menubar(self.controller)
        self.boxes()
        self.entryboxes()
        self.buttons()
        self.labels()

    def initUI(self):
        self.parent.title("NOTAM downloader and NOTAM filter")
        self.parent.resizable(width=False, height=True)
        self.pack()

    def menubar(self, controller):
        menubar = Menu(controller)
        menu = Menu(menubar, tearoff=0)
        menu.add_checkbutton(label="Always EST", onvalue=1, offvalue=0, variable=ESTvar)
        menu.add_checkbutton(label="Always PERM", onvalue=1, offvalue=0, variable=PERMvar)
        menu.add_checkbutton(label="NOTAMs downloaded from ICAO", onvalue=1, offvalue=0, variable=download_flag)
        menu.add_command(label="Settings...", command=self.new_window_settings)
        menubar.add_cascade(label="File", menu=menu)
        controller.config(menu=menubar)

    def boxes(self):
        global entry
        global output
        entry = TextFrame(self)
        entry.grid(row=1, column=0)
        output = TextFrame(self)
        output.grid(row=1, column=3)

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
        Button(self, text="NOTAM FILTR", width=20, command=finder).grid(row=0, column=3, padx=20, sticky=E)
        button2 = Button(self, text="NOTAM download", width=20, command=self.new_window_download).grid(row=0, column=3,
                                                                                                       padx=0, sticky=W)

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
            self.app = SettingWindowClass(self.options_toplevel)

    def new_window_download(self, *args):
        if self.options_toplevel is None:
            self.options_toplevel = tk.Toplevel(self.master)
            self.options_toplevel.protocol('WM_DELETE_WINDOW', self.on_tl_close)
            self.app = NotamDownloadClass(self.options_toplevel)

    def on_tl_close(self, *args):
        self.options_toplevel.destroy()
        self.options_toplevel = None


def main():
    global gui
    win = Tk()
    ESTvar = BooleanVar()
    ESTvar.set(True)
    gui = MainWin(win, win)
    gui.pack()
    win.mainloop()


if __name__ == '__main__':
    main()
