from tkinter import filedialog as fd

class FileManager:
    def __init__(self):
        pass

    def askFile(self, title):
        asked = fd.askopenfilename(title=title, filetypes=(("PDF Files", "*.pdf"), ))
        self.askedFile = asked

        return asked
    
    def askFiles(self, title):
        asked = fd.askopenfilenames(title=title, filetypes=(("PDF Files", "*.pdf"), ))
        self.askedFiles = asked
        return asked

    def askDir(self, title):
        askedDir = fd.askdirectory(title=title)
        self.askedDir = askedDir

        return askedDir

    def askSaveAs(self, title, initFile):
        asked = fd.asksaveasfilename(title=title, initialfile=initFile, filetypes=(("PDF Files", "*.pdf"), ))

        self.asksaveasfilename = asked

        return asked