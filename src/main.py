from tkinter import OptionMenu, StringVar, Tk, Entry, Button, Label, Text, END, Y
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showinfo
from matplotlib import pyplot as plt
from pandas import read_csv, read_excel
from os.path import basename

# Main Window
root = Tk()
root.configure(background='#070091')
root.title("Data Plotter")
root.iconbitmap("./icon.ico")
root.minsize(900, 550)
root.state('zoomed')

# Files/Data
file = ""
column1 = []
column2 = []
data_file = ""
basename_title = ""
dataset = []

class DataPoint:
    def __init__(self, label: str = "", column1: str = "", column2: str = "", data_file: str = "", basename_title: str = data_file.replace(".csv", "").replace(".xlsx", "")):
        self.label = label
        self.column1 = column1
        self.column2 = column2
        self.data_file = data_file
        self.basename_title = basename_title
    
    def setFile(self, file: str):
        self.data_file = file
        self.basename_title = file.replace(".csv", "").replace(".xlsx", "")
    
    def setCol1(self, col1: str):
        self.column1 = col1
    
    def setCol2(self, col2: str):
        self.column2 = col2
    
    def setLabel(self, label: str):
        self.label = label

def createGraph():
    '''Plot all datapoints'''

# Text Fields
column1Text = Entry(root, font=('Arial', '16'))
column1Text.place(x=550, y=280)
column2Text = Entry(root, font=('Arial', '16'))
column2Text.place(x=550, y=325)
labelText = Entry(root, font=("Arial", "16"))
labelText.place(x=550, y=235)

# Preview
preview = Text(root, wrap="none", font=('Arial', '14'), height=864, background='#8c03fc', foreground='white')
preview.pack(expand=True, fill=Y)
preview.place(x=900, y=0)

# Labels
text1 = Label(root, text="Column Name for X Axis/Primary Value : ", font=('Arial', '16'), bg='#070091', fg='white')
text1.place(x=110, y=280)
text2 = Label(root, text="Column Name for Y Axis/Secondary Value : ", font=('Arial', '16'), bg='#070091', fg='white')
text2.place(x=80, y=325)
text3 = Label(root, text="File :           Not selected", font=('Arial', '16'), bg='#070091', fg='white')
text3.place(x=435, y=370)
text4 = Label(root, text=" Graph : ", font=('Arial', '16'), bg='#070091', fg='white')
text4.place(x=410, y=140)
text5 = Label(root, text="Label : ", font=('Arial', '16'), bg='#070091', fg='white')
text5.place(x=420, y=235)

# Dropdown Menu
graph_label = StringVar(root, "Select Graph")
graphs = OptionMenu(root, graph_label, *["Line Graph", "Bar Graph", "Horizontal Bar Graph", "Pie Chart", "Scatter Plot", "Area Chart"])
graphs.place(x=550, y=140)

theme_label = StringVar(root, "Graph Theme")
graphs = OptionMenu(root, theme_label, *[style for style in plt.style.available])
graphs.place(x=720, y=10)

def getColumnData() -> bool:
    global column1
    global column2

    try:
        column1 = list(data_file[str(column1Text.get())])
        column2 = list(data_file[str(column2Text.get())])
        return True
    except:
        showinfo("Data Plotter", "One or both columns doesn't exist")
        return False

def graphWindow():
    plt.get_current_fig_manager().window.wm_iconbitmap("./icon.ico")
    plt.get_current_fig_manager().set_window_title(f"Data Plotter {graph_label.get()} - {basename_title}")
    if theme_label.get() == "Graph Theme":
        plt.style.use('bmh')
    else:
        plt.style.use(theme_label.get())

def plotGraph():
    if not getColumnData():
        return

    createGraph()
    plt.show()

    '''
    if graph_label.get() == "Select Graph":
        showinfo("Data Plotter", "Please select type of graph")
        return

    elif graph_label.get() == "Line Graph":
        graphWindow()
        plt.plot(column1, column2, label=labelText.get())
        plt.xlim([min(column1), max(column1)])
        plt.ylim([min(column2), max(column2)])
        plt.title(f"Line Graph - {basename_title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.legend()
        plt.show()

    elif graph_label.get() == "Bar Graph":
        graphWindow()
        plt.bar(column1, column2, label=labelText.get())
        plt.title(f"Bar Graph - {basename_title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.legend()
        plt.show()

    elif graph_label.get() == "Horizontal Bar Graph":
        graphWindow()
        plt.barh(column2, column1)
        plt.title(f"Horizontal Bar Graph - {basename_title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.show()

    elif graph_label.get() == "Pie Chart":
        graphWindow()
        plt.pie(column1, labels=column2)
        plt.title(f"Pie Chart - {basename_title}")
        plt.show()
    
    elif graph_label.get() == "Scatter Plot":
        graphWindow()
        plt.scatter(column1, column2, label=labelText.get())
        plt.title(f"Scatter Plot - {basename_title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.legend()
        plt.show()

    elif graph_label.get() == "Area Chart":
        graphWindow()
        plt.stackplot(column1, column2, labels=[labelText.get()])
        plt.title(f"Area Chart - {basename_title}")
        plt.xlabel(str(column1Text.get()).title())
        plt.ylabel(str(column2Text.get()).title())
        plt.legend(loc='upper left')
        plt.show()

    else:
        raise Exception("Graph Value not recognized")
    '''


def openFile():
    global file
    global data_file
    global basename_title

    file = askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Sheets", "*.xlsx")])
    if file == "":
        return
    else:
        try:
            if file.endswith(".csv"):
                data_file = read_csv(file)
            elif file.endswith(".xlsx"):
                data_file = read_excel(file)
            else:
                showinfo("Data Plotter", "Improper File Extension")

        except:
            showinfo("Data Plotter", "Error Parsing File")
            return

    if len(data_file) > 2500:
        showinfo("Data Plotter", "Number of rows greater than 2500. Please reduce the number of rows to avoid "
                                 "performance issues")
        return

    text3.config(text=f"File :          {basename(file)}")
    preview.delete(1.0, END)
    preview.insert(1.0, data_file)
    basename_title = basename(file).replace(".csv", "").replace(".xlsx", "")


# Buttons
fileButton = Button(root, text="Open File", relief="groove", activebackground="black", activeforeground="white",
                    font=('Arial', '16'), command=openFile)
fileButton.place(x=550, y=420)
plotButton = Button(root, text="Plot", relief="groove", activebackground="black", activeforeground="white",
                    font=('Arial', '16'), command=plotGraph)
plotButton.place(x=500, y=520)

root.mainloop()
