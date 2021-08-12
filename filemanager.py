from tkinter import filedialog as fd

class FileManager:
    def __init__(self):
        pass

    def askFile(self, title):
        asked = fd.askopenfilename(title=title, filetypes=(("PDF Files", "*.pdf"), ))
        self.askedFile = asked

    def askDir(self, title):
        askedDir = fd.askdirectory(title=title)
        self.askedDir = askedDir