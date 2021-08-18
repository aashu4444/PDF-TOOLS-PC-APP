import PyPDF2
import io
from PIL import Image
import fitz

class Tool():
    """A Class for having next level operation of a pdf file"""

    # A blank pdf writer object
    pdf_writer = PyPDF2.PdfFileWriter()
    
    def __init__(self, fileSrc):
        self.src = fileSrc
        self.obj = open(self.src, "rb") # Open the pdf file in read binary mode


    @staticmethod
    def copyPagesFromReader(Reader, Writer):
        """Copy pages from PyPDF2's Reader Object to writer object"""
        for i in range(Reader.getNumPages()):
            Writer.addPage(Reader.getPage(i))


    def encrypt(self, password, saveTo, close=True):
        """
        A method for encrypting a pdf file
        password: the password to a in the pdf file
        saveTo: Where to save the encrypted pdf file
        close: close all opened file objects, Default is True
        """

        # Set password on the pdf file
        self.pdf_writer.encrypt(password)

        # Create a new blank pdf file
        savePath = open(saveTo, "wb")
        
        # Write the binary data the the blank pdf file
        self.pdf_writer.write(savePath)

        # If user wants to close all opened file object then close them
        if close:
            self.obj.close()

    def decrypt(self, password, saveTo, close=True):
        """
        A method for decrypting a pdf file
        password: password of the pdf file
        saveTo: Where to save the decrypted pdf file
        close: close all opened file objects, Default is True
        """

        # Create a new PyPDF2.PdfFileReader object
        reader = PyPDF2.PdfFileReader(self.obj)

        # Remove password from the pdf file
        reader.decrypt(password)

        # Set the pdf_reader to new reader object that is decrypted
        self.pdf_reader = reader

        # Save the decrypted pdf file
        # The splitPages method is used because if user wants to save entered pages of the pdf file
        self.splitPages(saveTo)


    @staticmethod
    def save_pdf(writer, saveTo):
        """
        A static method to save a pdf file
        writer: the writer object whose data to be saved
        saveTo: location, where to save the pdf file
        """
        savePath = open(saveTo, "wb")
        
        writer.write(savePath)

    def remove_links(self, saveTo, close=True):
        """
        A method to remove links from a pdf file
        saveTo: Where to save the pdf file
        close: close all opened file objects, Default is True
        """
        
        # Remove links from the pdf file
        self.pdf_writer.removeLinks()

        # Save the pdf file after removing links
        Tool.save_pdf(self.pdf_writer, saveTo)

        # If user wants to close all opened file object then close them
        if close:
            
            self.obj.close()

        return self.pdf_writer

    def remove_images(self, saveTo, close=True):
        """
        A method to remove images from a pdf file
        saveTo: Where to save the pdf file
        close: close all opened file objects, Default is True
        """

        # Remove links from the pdf file
        self.pdf_writer.removeImages()

        # Save the pdf file after removing links
        Tool.save_pdf(self.pdf_writer, saveTo)

        # If user wants to close all opened file object then close them
        if close:
            
            self.obj.close()

        return self.pdf_writer

    def save_operation_pages(self, saveTo, close=True):
        """
        A method to save operatiion pages as a pdf file from PyPDF2.PdfFileWriter object
        saveTo: Where to save the operation pages as a pdf file
        close: close all opened file objects, Default is True
        """
        
        # Save the operation pages
        Tool.save_pdf(self.pdf_writer, saveTo)

        # If user wants to close all opened file object then close them
        if close:
            
            self.obj.close()

    def extract_images(self, saveTo=None):
        file = self.src
        pdf_file = fitz.open(file)
        dstImages = []


        for current_page_index in self.pages:

            for image_index, img in enumerate(pdf_file.getPageImageList(current_page_index)):
                xref = img[0]
                image = fitz.Pixmap(pdf_file, xref)

                imageName = "{}/image{}-{}.png".format(saveTo,current_page_index, image_index)

                #if it is a is GRAY or RGB image
                if image.n < 5:        
                    image.writePNG(imageName)

                #if it is CMYK: convert to RGB first
                else:                
                    new_image = fitz.Pixmap(fitz.csRGB, image)

                    new_image.writePNG(imageName)

                dstImages.append(imageName)

        Tool.dstImages = dstImages

    def splitPages(self, saveTo, close=True):
        if self.requested_pages[0] == "all":
            for i in range(self.pdf_reader.getNumPages()):
                self.pdf_writer.addPage(self.pdf_reader.getPage(i))

        else:
            pages = []
            for i in self.requested_pages:
                if "-" in str(i):
                    ranges = i.split("-")

                    pages.extend(list(range(int(ranges[0])-1, int(ranges[1]) )))
                
                else:
                    pages.append(i-1)
            for i in pages:
                self.pdf_writer.addPage(self.pdf_reader.getPage(i))

        writePath = open(saveTo, "wb")

        self.pdf_writer.write(writePath)

        writePath.close()

        return self.pdf_reader, self.pdf_writer

    def merge_pdf(self, position=None, fileobjs=None, saveTo=None, pages=None):
        """
        Combines 1 or more pdf files into one pdf file.
        fileobjs: tuple: contains path of pdf files to merge
        saveTo: Where to save the pdf file
        """


        # If user not given the position then set it to the length of uploaded pdf file
        if position == None or position == "":
            position = int(self.pdf_reader.getNumPages())
        
        else:
            position = int(position)

        # Create a blank pdf file merger object
        merger = PyPDF2.PdfFileMerger()

        fileobjs = list(fileobjs)

        merger.merge(position=0,fileobj=open(self.src, "rb"))

        # Convert the file src in fileobjs to a python's file object
        for index, item in enumerate(fileobjs):
            fileobjs[index] = open(item, "rb")
        
        for i in fileobjs:
            merger.merge(position=position,fileobj=i, pages=(pages[0], pages[1] if pages[1] != "end" else int(PyPDF2.PdfFileReader(i).getNumPages())))
        
        # Save the merged pdf file
        Tool.save_pdf(merger, saveTo)