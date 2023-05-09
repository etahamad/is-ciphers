from tkinter import *
from tkinter import filedialog, messagebox
from PIL import Image

class SteganographyGUI:
    def __init__(self, master):
        self.master = master
        master.title("Steganography")

        # create labels and buttons
        self.label1 = Label(master, text="Enter message:")
        self.label1.pack()
        self.entry1 = Entry(master, width=50)
        self.entry1.pack()

        self.label2 = Label(master, text="Choose image:")
        self.label2.pack()
        self.button1 = Button(master, text="Browse", command=self.choose_image)
        self.button1.pack()

        self.label3 = Label(master, text="")
        self.label3.pack()

        self.encode_button = Button(master, text="Encode", command=self.encode_message, state=DISABLED)
        self.encode_button.pack(side=LEFT)

        self.decode_button = Button(master, text="Decode", command=self.decode_message, state=DISABLED)
        self.decode_button.pack(side=RIGHT)

        self.quit_button = Button(master, text="Quit", command=master.quit)
        self.quit_button.pack(side=BOTTOM)

    # function to choose image
    def choose_image(self):
        self.filename = filedialog.askopenfilename(title="Select File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        if self.filename:
            self.image = Image.open(self.filename)

            self.label3.config(text=f"Selected image: {self.filename}")
            self.encode_button.config(state=NORMAL)
            self.decode_button.config(state=NORMAL)

    # function to encode message into image
    def encode_message(self):
        message = self.entry1.get().strip()

        if not message:
            messagebox.showerror("Error", "Please enter a message")
            return

        if not self.image:
            messagebox.showerror("Error", "Please choose an image")
            return

        new_image = Image.new(self.image.mode, self.image.size)
        new_image.putdata(list(modPix(self.image.getdata(), message)))
        new_filename = filedialog.asksaveasfilename(title="Save As", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

        if new_filename:
            new_image.save(new_filename)
            messagebox.showinfo("Success", "Message encoded successfully!")

    # function to decode message from image
    def decode_message(self):
        if not self.image:
            messagebox.showerror("Error", "Please choose an image")
            return

        decoded_message = decode()
        messagebox.showinfo("Decoded Message", decoded_message)

# function to convert encoding data into 8-bit binary form using ASCII value of characters
def genData(data):
    newd = []
    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

# function to modify pixels according to the 8-bit binary data and finally return them
def modPix(pix, data):
    datalist = genData(data)
    lendata = len(datalist)
    imdata = iter(pix)
    for i in range(lendata):
        pix = [value for value in imdata.__next__()[:3] +
               imdata.__next__()[:3] +
               imdata.__next__()[:3]]
        for j in range(0, 8):
            if (datalist[i][j] == '0' and pix[j]% 2 != 0):
                pix[j] -= 1
            elif (datalist[i][j] == '1' and pix[j] % 2 == 0):
                if(pix[j] != 0):
                    pix[j] -= 1
                else:
                    pix[j] += 1
        if (i == lendata - 1):
            if (pix[-1]% 2 == 0):
                if(pix[-1] != 0):
                    pix[-1] -= 1
                else:
                    pix[-1] += 1
        else:
            if (pix[-1]% 2 != 0):
                pix[-1] -= 1
        pix = tuple(pix)
        yield pix[0:3]
        yield pix[3:6]
        yield pix[6:9]

# function to decode data from image
def decode():
    img = filedialog.askopenfilename(title="Select File", filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])
    if not img:
        messagebox.showerror("Error", "Please choose an image")
        return

    image = Image.open(img, 'r')
    data = ''
    imgdata = iter(image.getdata())

    while (True):
        pixels = [value for value in imgdata.__next__()[:3] +
                                 imgdata.__next__()[:3] +
                                 imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in pixels[:8]:
            if (i % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data

root = Tk()
my_gui = SteganographyGUI(root)
root.mainloop()
