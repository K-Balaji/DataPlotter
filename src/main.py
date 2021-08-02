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
root.minsize(900, 720)
root.state('zoomed')

theme = "dark"

# Frame
plots_frame = Frame(root)
plots_frame.place(x=30, y=240)

# Table Array
table_array: list[list[Entry]] = []

class DataPoint:
    def __init__(self, label: str = "", column1: str = "", column2: str = "", data_file: str = ""):
        self.label = label
        self.column1 = column1
        self.column2 = column2
        self.data_file = data_file
        self.basename_title = basename(data_file).replace(".csv", "").replace(".xlsx", "")
    
    def setFile(self, file: str):
        self.data_file = file
        self.basename_title = basename(file).replace(".csv", "").replace(".xlsx", "")
    
    def setCol1(self, col1: str):
        self.column1 = col1
    
    def setCol2(self, col2: str):
        self.column2 = col2
    
    def setLabel(self, label: str):
        self.label = label
    
    def getFile(self):
        data_table.update_from_table()

        file = askopenfilename(filetypes=[("CSV Files", "*.csv"), ("Excel Files", "*.xlsx")])
        if file == "":
            return
        else:
            self.data_file = file
            self.basename_title = basename(file).replace(".csv", "").replace(".xlsx", "")
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
        
        data_table.update_from_dataset()
                

# Data Set
dataset: list[DataPoint] = []

class Table:
    def update_from_dataset(self):
        global plots_frame
        table_array.clear()
        plots_frame.destroy()
        plots_frame = Frame(root)
        plots_frame.place(x=30, y=240)
        for i in range(len(dataset)):
            table_array.append([])
            for j in range(5):
                if j != 4:
                    if theme == "dark":
                        entry = Entry(plots_frame, width=16, font=("Arial", "16"), foreground="white", background="black")
                    else:
                        entry = Entry(plots_frame, width=16, font=("Arial", "16"), foreground="black", background="white")
                    entry.grid(row=i, column=j)
                    if j == 0:
                        entry.insert(END, dataset[i].label)
                    elif j == 1:
                        entry.insert(END, dataset[i].column1)
                    elif j == 2:
                        entry.insert(END, dataset[i].column2)
                    else:
                        entry.insert(END, dataset[i].data_file)
                    
                    table_array[i].append(entry)
                else:
                    if theme == "dark":
                        button = Button(plots_frame, text="Open File", relief="groove", activebackground="gray", activeforeground="white", foreground="white", background="black", command=dataset[i].getFile, borderwidth=4)
                    else:
                        button = Button(plots_frame, text="Open File", relief="groove", activebackground="gray", activeforeground="black", foreground="black", background="white", command=dataset[i].getFile, borderwidth=4)
                    button.grid(row=i, column=j)
    
    def update_from_table(self):
        for i in range(len(table_array)):
            for j in range(4):
                if j == 0:
                    dataset[i].setLabel(table_array[i][j].get())
                elif j == 1:
                    dataset[i].setCol1(table_array[i][j].get())
                elif j == 2:
                    dataset[i].setCol2(table_array[i][j].get())
                else:
                    dataset[i].setFile(table_array[i][j].get())

data_table = Table()
data_table.update_from_dataset()

# Preview
preview = Text(root, wrap="none", font=('Arial', '14'), height=864, background='#8c03fc', foreground='white')
preview.pack(expand=True, fill=Y)
preview.place(x=900, y=0)

# Labels
text1 = Label(root, text="Label", font=('Arial', '16'), bg='#070091', fg='white')
text1.place(x=100, y=200)
text2 = Label(root, text="Column 1\\Primary", font=('Arial', '16'), bg='#070091', fg='white')
text2.place(x=240, y=200)
text3 = Label(root, text="Column 2\\Secondary", font=('Arial', '16'), bg='#070091', fg='white')
text3.place(x=420, y=200)
text4 = Label(root, text="File Path", font=('Arial', '16'), bg='#070091', fg='white')
text4.place(x=680, y=200)

# Dropdown Menu
graph_label = StringVar(root, "Select Graph")
graphs = OptionMenu(root, graph_label, *["Line Graph", "Bar Graph", "Horizontal Bar Graph", "Pie Chart", "Scatter Plot", "Area Chart"])
graphs.place(x=400, y=125)
graphs.config(bg="BLACK", fg="WHITE")
graphs.config(activebackground="BLACK", activeforeground="WHITE")
graphs["menu"].config(bg="BLACK", fg="WHITE")
graphs["highlightthickness"] = 0

theme_label = StringVar(root, "Graph Theme")
themes = OptionMenu(root, theme_label, *[style for style in plt.style.available])
themes.place(x=720, y=30)
themes.config(bg="BLACK", fg="WHITE")
themes.config(activebackground="BLACK", activeforeground="WHITE")
themes["menu"].config(bg="BLACK", fg="WHITE")
themes["highlightthickness"] = 0

def read_file(filename: str):
    if filename.endswith(".xlsx"):
        return read_excel(filename)
    else:
        return read_csv(filename)

def createGraph() -> bool:
    plt.clf()
    if graph_label.get() == "Bar Graph":
        for datapoint in dataset:
            if datapoint.data_file == "":
                showinfo("Data Plotter", "Please select a data file")
                return False
            file = read_file(datapoint.data_file)
            try:
                plt.bar(file[datapoint.column1], file[datapoint.column2], label=datapoint.label)
            except:
                showinfo("Data Plotter", "One or more columns didn't exist")
                return
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
        plt.legend()
    elif graph_label.get() == "Line Graph":
        for datapoint in dataset:
            if datapoint.data_file == "":
                showinfo("Data Plotter", "Please select a data file")
                return False
            file = read_file(datapoint.data_file)
            try:
                plt.plot(file[datapoint.column1], file[datapoint.column2],label=datapoint.label)
            except:
                showinfo("Data Plotter", "One or more columns didn't exist")
                return
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
        plt.legend()
    elif graph_label.get() == "Horizontal Bar Graph":
        if len(table_array) > 1:
            showinfo("Data Plotter", "Horizontal Bar Graph takes only the first set of data given")
        if dataset[0].data_file == "":
            showinfo("Data Plotter", "Please select a data file")
            return False
        file = read_file(dataset[0].data_file)
        try:
            plt.barh(file[dataset[0].column2], file[dataset[0].column1], label=dataset[0].label)
        except:
            showinfo("Data Plotter", "One or more columns didn't exist")
            return
        plt.xlabel(dataset[0].column2.title())
        plt.ylabel(dataset[0].column1.title())
    elif graph_label.get() == "Pie Chart":
        if len(table_array) > 1:
            showinfo("Data Plotter", "Pie Chart takes only the first set of data given")
        if dataset[0].data_file == "":
            showinfo("Data Plotter", "Please select a data file")
            return False
        file = read_file(dataset[0].data_file)
        try:
            plt.pie(file[dataset[0].column1], labels=file[dataset[0].column2])
        except:
            showinfo("Data Plotter", "One or more columns didn't exist")
            return
    elif graph_label.get() == "Scatter Plot":
        for datapoint in dataset:
            if datapoint.data_file == "":
                showinfo("Data Plotter", "Please select a data file")
                return False
            file = read_file(datapoint.data_file)
            try:
                plt.scatter(file[datapoint.column1], file[datapoint.column2], label=datapoint.label)
            except:
                showinfo("Data Plotter", "One or more columns didn't exist")
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
            plt.legend()
    elif graph_label.get() == "Area Chart":
        for datapoint in dataset:
            if datapoint.data_file == "":
                showinfo("Data Plotter", "Please select a data file")
                return False
            file = read_file(datapoint.data_file)
            try:
                plt.stackplot(file[datapoint.column1], file[datapoint.column2], labels=[datapoint.label])
            except:
                showinfo("Data Plotter", "One or more columns didn't exist")
                return
            plt.xlabel(datapoint.column1.title())
            plt.ylabel(datapoint.column2.title())
            plt.legend(loc='upper left')
    else:
        raise Exception("GraphValue not recognized")
    
    return True

def graphWindow():
    plt.get_current_fig_manager().window.wm_iconbitmap("./icon.ico")
    plt.get_current_fig_manager().set_window_title(f"Data Plotter - {graph_label.get()}")
    plt.title(f"Data Plotter - {graph_label.get()}")
    if theme_label.get() == "Graph Theme":
        plt.style.use('bmh')
    else:
        plt.style.use(theme_label.get())

def plotGraph():
    if graph_label.get() == "Select Graph":
        showinfo("Data Plotter", "Select type of graph")
    else:
        data_table.update_from_table()
        graphWindow()
        if createGraph():
            plt.show()

def addRow():
    data_table.update_from_table()
    if len(dataset) >= 10:
        showinfo("Data Plotter", "Can't add more than 10 plots")
        return
    dataset.append(DataPoint())
    data_table.update_from_dataset()

def changeTheme():
    global theme
    global data_table

    theme = "dark" if theme == "light" else "light"
    data_table.update_from_table()
    data_table.update_from_dataset()
    if theme == "light":
        graphs.config(bg="WHITE", fg="BLACK")
        graphs.config(activebackground="WHITE", activeforeground="BLACK")
        graphs["menu"].config(bg="WHITE", fg="BLACK")

        themes.config(bg="WHITE", fg="BLACK")
        themes.config(activebackground="WHITE", activeforeground="BLACK")
        themes["menu"].config(bg="WHITE", fg="BLACK")
        
        arrowButton.config(activebackground="GRAY", activeforeground="BLACK")
        arrowButton.config(background="WHITE", foreground="BLACK")

        plotButton.config(activebackground="GRAY", activeforeground="BLACK")
        plotButton.config(background="WHITE", foreground="BLACK")

        minusButton.config(activebackground="GRAY", activeforeground="BLACK")
        minusButton.config(background="WHITE", foreground="BLACK")

        themeButton.config(activebackground="GRAY", activeforeground="BLACK")
        themeButton.config(background="WHITE", foreground="BLACK")

        root.configure(background='#2185ff')

        text1.config(background="#2185ff", foreground="black")
        text2.config(background="#2185ff", foreground="black")
        text3.config(background="#2185ff", foreground="black")
        text4.config(background="#2185ff", foreground="black")

        preview.config(background="#ff47ed", foreground="black")
    else:
        graphs.config(bg="BLACK", fg="WHITE")
        graphs.config(activebackground="BLACK", activeforeground="WHITE")
        graphs["menu"].config(bg="BLACK", fg="WHITE")

        themes.config(bg="BLACK", fg="WHITE")
        themes.config(activebackground="BLACK", activeforeground="WHITE")
        themes["menu"].config(bg="BLACK", fg="WHITE")

        arrowButton.config(activebackground="GRAY", activeforeground="WHITE")
        arrowButton.config(background="BLACK", foreground="WHITE")

        plotButton.config(activebackground="GRAY", activeforeground="WHITE")
        plotButton.config(background="BLACK", foreground="WHITE")

        minusButton.config(activebackground="GRAY", activeforeground="WHITE")
        minusButton.config(background="BLACK", foreground="WHITE")
        
        themeButton.config(activebackground="GRAY", activeforeground="WHITE")
        themeButton.config(background="BLACK", foreground="WHITE")

        root.configure(background='#070091')
        text1.config(background="#070091", foreground="white")
        text2.config(background="#070091", foreground="white")
        text3.config(background="#070091", foreground="white")
        text4.config(background="#070091", foreground="white")        

        preview.config(background="#8c03fc", foreground="white")

def removeRow():
    global dataset

    data_table.update_from_table()
    dataset = dataset[:-1]
    data_table.update_from_dataset()

# Buttons
arrowButton = Button(root, text="+", relief="groove", activebackground="gray", activeforeground="white", background="black", foreground="white", font=("Arial", '14'), command=addRow)
arrowButton.place(x=395, y=580)

minusButton = Button(root, text="-", relief="groove", activebackground="gray", activeforeground="white", background="black", foreground="white", font=("Arial", '14'), command=removeRow)
minusButton.place(x=455, y=580)

plotButton = Button(root, text="Plot", relief="groove", activebackground="gray", activeforeground="white", background="black", foreground="white", font=('Arial', '16'), command=plotGraph)
plotButton.place(x=410, y=640)

themeButton = Button(root, text="Switch Theme", relief="groove", activebackground="gray", activeforeground="white", background="black", foreground="white", command=changeTheme)
themeButton.place(x=30, y=30)

root.mainloop()
