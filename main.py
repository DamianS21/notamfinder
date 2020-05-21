import datetime
import tkinter as tk
from tkinter import messagebox
from tkinter import *

# Global BOOLVar to check if data was pasted or downloaded
notam = []  # Global list for NOTAMs strings
today = (datetime.datetime.now().strftime("%y%m%d"))  # Todays date
lst = []

import settings


def settings_window():
    win3 = Tk()
    label_sett = Label(win3, text="ICAO API key")
    label_sett.grid(row=0, column=0)
    icaoapikey = Entry(win3, width=45)
    icaoapikey.grid(row=0, column=1)
    icaoapikey.insert(0, settings.ICAO_API_key)
    savebutton = Button(win3, text="Save settings", width=20, command=lambda: savesettings(icaoapikey.get()))
    savebutton.grid(row=1, column=1)
    win.wait_window(win3)


def savesettings(icaoapikey):
    settings.ICAO_API_key = icaoapikey
    settings.exit()


def window():
    win2 = Tk()
    aprtcode = Entry(win2, width=6)
    aprtcode.grid(row=0, column=0)
    searchbutton = Button(win2, text="NOTAM load", width=20, command=lambda: notam_download(aprtcode.get()))
    searchbutton.grid(row=1, column=0)
    win.wait_window(win2)


def check_NOTAM(datefrom, dateto, notamfrom, notamto):
    if (datefrom <= notamfrom and dateto >= notamto) or (
            datefrom <= notamfrom <= dateto <= notamto) or (
            notamfrom <= datefrom <= notamto <= dateto) or (
            notamfrom <= datefrom <= notamto and dateto <= notamto):
        return True
    else:
        return False


def notam_download(aprt_to_download):
    import requests
    import json
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
        return
    entry.text.delete('1.0', END)
    notam.clear()
    for x in json_data:
        entry.text.insert(END, x['all'] + '\n\n')
        notam.append(x['all'])
    download_flag.set(True)  # Setting download flag to true


class Rama(tk.Frame):
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

    def highlight(self, event=None):
        self.text.tag_remove("keyword", 1.0, 'end')
        self.text.tag_configure("keyword", background='yellow', relief='raised')
        keywords = entrykeywords.get()
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


def insert_to_focus_in(_):
    entrydate2.delete(0, tk.END)
    entrydate2.config(fg='black')


def insert_to_focus_out(_):
    if (entrydate2.get() == ""):
        entrydate2.delete(0, tk.END)
        entrydate2.config(fg='grey')
        entrydate2.insert(0, "UFN")


def handle_enter(txt):
    print(full_name_entry.get())
    win.focus()


def remove(string):
    return string.replace(" ", "")


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
    if (entrydate2.get() == "" or entrydate2.get() == "UFN"):
        dateto = datetime.date(2999, 1, 1)
    else:
        to = entrydate2.get()
        dateto = datetime.date(int(str(20) + to[0:2]), int(to[2:4]), int(to[4:6]))
    frm = entrydate1.get()
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
        elif C[i][-3:] == "EST":
            datesC.append(datetime.date(9999, 1, 1))
            if ESTvar.get() == 1:
                lst.append(notam[i])
                lst.append(" ")
        else:
            datesC.append(datetime.date(int(str(20) + C[i][0:2]), int(C[i][2:4]), int(C[i][4:6])))
            if (check_NOTAM(datefrom, dateto, datesB[i], datesC[i])):
                lst.append(notam[i])
                lst.append(" ")
    for x in lst:
        output.text.insert(END, x + '\n')
pass

try:
    while True:
        win = Tk()
        menu = Menu(win)
        win.resizable(width=False, height=True)
        ESTvar = BooleanVar()
        ESTvar.set(True)
        listone = Menu(tearoff=0)
        listone.add_checkbutton(label="EST", onvalue=1, offvalue=0, variable=ESTvar)
        PERMvar = BooleanVar()
        PERMvar.set(True)
        listone.add_checkbutton(label="PERM", onvalue=1, offvalue=0, variable=PERMvar)
        download_flag = BooleanVar()
        download_flag.set(False)
        listone.add_checkbutton(label="NOTAMs downloaded", onvalue=1, offvalue=0, variable=download_flag)
        listone.add_command(label="Settings...", command=settings_window)
        menu.add_cascade(label="Settings", menu=listone)
        l1 = Label(win, text="From:")
        l2 = Label(win, text="To:")
        scroll = Scrollbar(win)
        entry = Rama(win)

        entrydate1 = Entry(win, width=6)
        entrydate1.insert(END, today)
        entrydate2 = Entry(win, width=6, bg='white', fg='grey')
        entrydate2.bind("<FocusIn>", insert_to_focus_in)
        entrydate2.bind("<FocusOut>", insert_to_focus_out)
        entrydate2.bind("<Return>", handle_enter)
        entrydate2.insert(0, "UFN")
        entrykeywords = Entry(win, width=35)
        entrykeywords.insert(END, "ILS RWY DME VOR")
        keywords = entrykeywords.get()
        keywordstags = keywords.split(" ")
        button = Button(win, text="NOTAM FILTR", width=20, command=finder)
        button2 = Button(win, text="NOTAM download", width=20, command=window)
        output = Rama(win)

        # Positioning the widgets
        entry.grid(row=1, column=0)
        l1.grid(row=0, column=0, sticky=E, padx=125)
        l2.grid(row=0, column=0, sticky=E, padx=50)
        entrydate1.grid(row=0, column=0, sticky=E, padx=75)
        entrydate2.grid(row=0, column=0, sticky=E, padx=0)
        entrykeywords.grid(row=0, column=0, sticky=W, padx=5)
        button.grid(row=0, column=3, padx=20, sticky=E)
        button2.grid(row=0, column=3, padx=0, sticky=W)
        output.grid(row=1, column=3)

        win.config(menu=menu)

        win.mainloop()
        break
except KeyboardInterrupt:
    print('\n')
