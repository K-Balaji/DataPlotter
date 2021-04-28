from tkinter import Tk, Entry, Button, Label, Text, END, Y
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo

from matplotlib import pyplot as plt
from pandas import read_csv

plt.style.use('bmh')

# Main Window
root = Tk()
root.configure(background='black')
root.title("Data Plotter")
root.iconbitmap("../icon.ico")
root.geometry('1200x650')
root.minsize(900, 600)

# Files
file = ""
column1 = []
column2 = []

# Text Fields
column1Text = Entry(root, font=('Arial', '16'))
column1Text.place(x=500, y=230)
column2Text = Entry(root, font=('Arial', '16'))
column2Text.place(x=500, y=275)

# Preview
preview = Text(root, wrap="none", font=('Arial', '14'), height=864)
preview.pack(expand=True, fill=Y)
preview.place(x=900, y=0)

# Labels
text1 = Label(root, text="Column Name for X Axis : ", font=('Arial', '16'), bg='black', fg='white')
text1.place(x=200, y=230)
text2 = Label(root, text="Column Name for Y Axis : ", font=('Arial', '16'), bg='black', fg='white')
text2.place(x=200, y=275)


def getColumnData():
    global column1
    global column2
    try:
        column1 = list(csv_file[str(column1Text.get())])
        column2 = list(csv_file[str(column2Text.get())])
    except:
        showinfo("Data Plotter", "One or both columns doesn't exist")
        return

    plt.plot(column1, column2, '.b-')
    plt.xlim([min(column1), max(column1)])
    plt.ylim([min(column2), max(column2)])
    plt.title("Data Plotter")
    plt.xlabel(str(column1Text.get()).title())
    plt.ylabel(str(column2Text.get()).title())
    plt.show()


def open_file():
    global file
    global csv_file
    file = askopenfilename(defaultextension='.csv', filetypes=[("CSV Files", "*.csv")])
    if file == "":
        return
    else:
        try:
            csv_file = read_csv(file)
        except:
            showinfo("Data Plotter", "Error Parsing CSV File")
            return

    if len(csv_file.index) > 2000:
        showinfo("Data Plotter", "Number of rows greater than 2000. Please reduce the number of rows to avoid "
                                 "performance issues")
        return

    preview.delete(1.0, END)
    preview.insert(1.0, csv_file)


# Buttons
fileButton = Button(root, text="Open File", relief="groove", activebackground="black", activeforeground="white",
                    font=('Arial', '16'), command=open_file)
fileButton.place(x=500, y=330)
plotButton = Button(root, text="Plot", relief="groove", activebackground="black", activeforeground="white",
                    font=('Arial', '16'), command=getColumnData)
plotButton.place(x=600, y=420)

root.mainloop()
