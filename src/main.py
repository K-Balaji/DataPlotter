from tkinter import Frame, OptionMenu, StringVar, Tk, Entry, Button, Label, Text, END, Y
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

# Frame
plots_frame = Frame(root)
plots_frame.place(x=130, y=240)

class DataPoint:
    def __init__(self, label: str = "", column1: str = "", column2: str = "", data_file: str = ""):
        self.label = label
        self.column1 = column1
        self.column2 = column2
        self.data_file = data_file
        self.basename_title = basename(data_file).replace(".csv", "").replace(".xlsx", "")
    
    def setFile(self, file: str):
        self.data_file = file
        self.basename_title = basename(data_file).replace(".csv", "").replace(".xlsx", "")
        try:
            file = read_file(self.data_file)
            if len(file) > 2500:
                showinfo("Data Plotter", "Number of rows greater than 2500. Please reduce the number of rows to avoid"
                             "performance issues")
                return
        except:
            showinfo("Data Plotter", "Error Parsing File")
            return
    
    def setCol1(self, col1: str):
        self.column1 = col1
    
    def setCol2(self, col2: str):
        self.column2 = col2
    
    def setLabel(self, label: str):
        self.label = label
    
    def getFile(self):
        file = askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Sheets", "*.xlsx")])
        if file == "":
            return
        else:
            self.data_file = file
            self.basename_title = basename(data_file).replace(".csv", "").replace(".xlsx", "")
            try:
                file = read_file(self.data_file)
                if len(file) > 2500:
                    showinfo("Data Plotter", "Number of rows greater than 2500. Please reduce the number of rows to avoid"
                                 "performance issues")
                    return
            except:
                showinfo("Data Plotter", "Error Parsing File")
                return
            preview.delete(1.0, END)
            preview.insert(1.0, read_file(self.data_file))

# Data Set
dataset: list[DataPoint] = [DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv"),DataPoint("GDP", "year", "income", "C:\\Users\\balajik\\Documents\\Python_Codes\\canada_per_capita_income.csv")]

class Table:
    def __init__(self):
        for i in range(len(dataset)):
            for j in range(5):
                if j != 4:
                    entry = Entry(plots_frame, width=12, font=("Arial", "16"))
                    entry.grid(row=i, column=j)
                    if j == 0:
                        entry.insert(END, dataset[0].label)
                    elif j == 1:
                        entry.insert(END, dataset[0].column1)
                    elif j == 2:
                        entry.insert(END, dataset[0].column2)
                    else:
                        entry.insert(END, dataset[0].data_file)
                else:
                    button = Button(plots_frame, text="Open File", relief="groove", activebackground="black", activeforeground="white", command=dataset[i].getFile, borderwidth=4)
                    button.grid(row=i, column=j)

Table()

# Files/Data
file = ""
column1 = []
column2 = []
data_file = ""
basename_title = ""
'''
# Text Fields
column1Text = Entry(root, font=('Arial', '16'))
column1Text.place(x=550, y=280)
column2Text = Entry(root, font=('Arial', '16'))
column2Text.place(x=550, y=325)
labelText = Entry(root, font=("Arial", "16"))
labelText.place(x=550, y=235)
'''

# Preview
preview = Text(root, wrap="none", font=('Arial', '14'), height=864, background='#8c03fc', foreground='white')
preview.pack(expand=True, fill=Y)
preview.place(x=900, y=0)

# Labels
text1 = Label(root, text="Label", font=('Arial', '16'), bg='#070091', fg='white')
text1.place(x=190, y=200)
text2 = Label(root, text="Column 1", font=('Arial', '16'), bg='#070091', fg='white')
text2.place(x=310, y=200)
text3 = Label(root, text="Column 2", font=('Arial', '16'), bg='#070091', fg='white')
text3.place(x=450, y=200)
text4 = Label(root, text="File Path", font=('Arial', '16'), bg='#070091', fg='white')
text4.place(x=610, y=200)

# Dropdown Menu
graph_label = StringVar(root, "Select Graph")
graphs = OptionMenu(root, graph_label, *["Line Graph", "Bar Graph", "Horizontal Bar Graph", "Pie Chart", "Scatter Plot", "Area Chart"])
graphs.place(x=400, y=140)

theme_label = StringVar(root, "Graph Theme")
graphs = OptionMenu(root, theme_label, *[style for style in plt.style.available])
graphs.place(x=720, y=30)

def read_file(filename: str):
    if filename.endswith(".xlsx"):
        return read_excel(filename)
    else:
        return read_csv(filename)

def createGraph():
    plt.clf()
    if graph_label.get() == "Bar Graph":
        for datapoint in dataset:
            file = read_file(datapoint.data_file)
            plt.bar(file[datapoint.column1], file[datapoint.column2], label=datapoint.label)
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
            plt.title("Data Plotter - Bar Graph")
        plt.legend()
    elif graph_label.get() == "Line Graph":
        for datapoint in dataset:
            file = read_file(datapoint.data_file)
            plt.plot(file[datapoint.column1], file[datapoint.column2], label=datapoint.label)
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
            plt.title("Data Plotter - Line Graph")
        plt.legend()
    elif graph_label.get() == "Horizontal Bar Graph":
        file = read_file(dataset[0].data_file)
        plt.barh(file[dataset[0].column2], file[dataset[0].column1], label=dataset[0].label)
        plt.xlabel(dataset[0].column2.title())
        plt.ylabel(dataset[0].column1.title())
        plt.title("Data Plotter - Horizontal Bar Graph")
    elif graph_label.get() == "Pie Chart":
        file = read_file(dataset[0].data_file)
        plt.pie(file[dataset[0].column1], labels=file[dataset[0].column2])
        plt.title("Data Plotter - Pie Chart")
    elif graph_label.get() == "Scatter Plot":
        for datapoint in dataset:
            file = read_file(datapoint.data_file)
            plt.scatter(file[datapoint.column1], file[datapoint.column2], label=datapoint.label)
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
            plt.title("Data Plotter - Scatter Plot")
            plt.legend()
    elif graph_label.get() == "Area Chart":
        for datapoint in dataset:
            file = read_file(datapoint.data_file)
            plt.stackplot(file[datapoint.column1], file[datapoint.column2], labels=[datapoint.label])
            plt.title("Data Plotter - Area Chart")
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
            plt.legend(loc='upper left')
    else:
        raise Exception("GraphValue not recognized")

'''
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
'''

def graphWindow():
    plt.get_current_fig_manager().window.wm_iconbitmap("./icon.ico")
    plt.get_current_fig_manager().set_window_title(f"Data Plotter {graph_label.get()} - {basename_title}")
    if theme_label.get() == "Graph Theme":
        plt.style.use('bmh')
    else:
        plt.style.use(theme_label.get())

def plotGraph():
    # if not getColumnData():
    #     return

    if graph_label.get() == "Select Graph":
        showinfo("Data Plotter", "Select type of graph")
    else:
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
            if len(read_file(file)) > 2500:
                showinfo("Data Plotter", "Number of rows greater than 2500. Please reduce the number of rows to avoid "
                                 "performance issues")
        except:
            showinfo("Data Plotter", "Error Parsing File")
            return

    # text3.config(text=f"File :          {basename(file)}")
    preview.delete(1.0, END)
    preview.insert(1.0, data_file)


# Buttons
plotButton = Button(root, text="Plot", relief="groove", activebackground="black", activeforeground="white",
                    font=('Arial', '16'), command=plotGraph)
plotButton.place(x=430, y=620)

root.mainloop()
