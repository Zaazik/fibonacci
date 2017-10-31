import logging

import os
import threading
from time import sleep
from tkinter import Tk, Button, Text
from tkinter.filedialog import askopenfilename
from tkinter import messagebox
module_logger = logging.getLogger(__name__)
import sys

import re

from io import StringIO

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage

l = []


def waiting():
    while True:
        sleep(1)
        try:
            val = l.pop(0)
        except IndexError:
            continue
        else:
            pars_pdf(val)


t1 = threading.Thread(target=waiting, args=[])
t1.start()


def calc(path):
    broken = list()
    broken_count = list()
    with open(path, "r") as file:
        GAS = list()
        count = 0
        for line in file.readlines():
            if "Площа (га):" in line or re.match("^\d+\.\d+(\sга)$", line):
                count += 1
                g = 0
                for n in line.split():
                    try:
                        g = float(re.findall("\d+\.\d+", n)[0])
                    except IndexError:
                        try:
                            g = int(re.findall("\d+", n)[0])
                        except IndexError:
                            pass
                if g > 50:
                    broken.append(line)
                    broken_count.append(g)
                else:
                    GAS.append(g)
        module_logger.info("%s" % path.split('/')[-1].split('.')[0].upper())
        module_logger.info("Общая площадь (ГА) : %s" % round(sum(GAS), 5))
        module_logger.info("Количество уникальных участков : %s" % (len(GAS) + len(broken)))

        if len(broken)>1:
            module_logger.info("Сумма площади участков которые выше 50 ГА : %s" % sum(broken_count))
            module_logger.info("Площать которая возможно вносит ошибку")
            for broken in broken:
                module_logger.info("=====> " + broken + "\n")
    os.remove(path)


def pars_pdf(path):
    module_logger.info("Extracting PDF to TXT %s", path.split("/")[-1])
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    text_path = path.replace(".pdf", ".txt")
    with open(text_path, "w") as txt:
        module_logger.info("Creating TXT file %s" % text_path)
        txt.write(text)
    calc(text_path)


class simpleapp_tk(Tk):
    def __init__(self, parent):
        Tk.__init__(self, parent)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.parent = parent

        self.grid()

        self.mybutton = Button(self, text="Открсть PDF файл", command=open_file)
        self.mybutton.grid(column=0, row=0, sticky='EW')

        self.mytext = Text(self, state="disabled")
        self.mytext.grid(column=0, row=1)

    def on_closing(self):
        if messagebox.askokcancel("Quit", "Do you want to quit?"):
            self.destroy()
            os._exit(1)





class MyHandlerText(logging.StreamHandler):
    def __init__(self, textctrl):
        logging.StreamHandler.__init__(self)  # initialize parent
        self.textctrl = textctrl

    def emit(self, record):
        msg = self.format(record)
        self.textctrl.config(state="normal")
        self.textctrl.insert("end", msg + "\n")
        self.flush()
        self.textctrl.config(state="disabled")


# t1 = threading.Thread(target=worker, args=[])
#     t1.start()
#
#     root.mainloop()
#     t1.join()
def open_file():
    files = []

    filename = askopenfilename()
    if filename.endswith(".pdf"):
        module_logger.info(filename.split("/")[-1])
    if filename.endswith(".pdf"):
        l.append(filename)


if __name__ == "__main__":

    # create Tk object instance
    app = simpleapp_tk(None)
    app.title('СЧЁТЧИК')

    # setup logging handlers using the Tk instance created above
    # the pattern below can be used in other threads...
    # ...to allow other thread to send msgs to the gui
    # in this example, we set up two handlers just for demonstration (you could add a fileHandler, etc)
    stderrHandler = logging.StreamHandler()  # no arguments => stderr
    module_logger.addHandler(stderrHandler)
    guiHandler = MyHandlerText(app.mytext)
    module_logger.addHandler(guiHandler)
    module_logger.setLevel(logging.INFO)

    # start Tk
    app.mainloop()

