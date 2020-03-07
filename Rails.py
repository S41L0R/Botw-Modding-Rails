# Import libraries
import clipboard
import math
import oead
#from tkinter import *
#from tkinter import ttk

# Set up points
X = [1, 3, 2]
Y = [1, 7, 15]
Z = [1, 5, 4]

# Set up HashID
HashID = "0x0"

# Set up other preferences
IsClosed = "false"
RailType = "Bezier"
Translate = [100, 50, 25]

# Set up index for NextDistance
NextDistanceIndex = []

# Set up array for NextDistance
NextDistanceArray = []

# Set up CurrentPoint. This keeps track of what point you're editing in the GUI.
CurrentPoint = 0

#Set up FilePath
FilePath = ""


#Set up window position
WindowX = 587
WindowY = 152
def WriteToFile(InputText):
    InputBytes = oead.byml.from_text(InputText)
    BYML = oead.byml.to_binary(InputBytes, True, 2)
    Yaz0 = oead.yaz0.compress(BYML)
    with open(FilePath, "wb") as OutputFile:
        WrittenOutputFile = OutputFile.write(Yaz0)
def InsertRail(Input, RailString):
    if (Input.find("Rails: []") == -1):
        OutputText = Input + "\n" + RailString
    else:
        OutputText = Input + "Rails:" + "\n" + RailString

    print(OutputText)
    #clipboard.copy(OutputText)
    print(RailString)
    WriteToFile(OutputText)
def ReadFromFile(RailString):
    #FilePath = top.PathEntry.get()
    with open(FilePath, 'rb') as InputFile:
        ReadInputFile = InputFile.read()
        DeYaz0 = oead.yaz0.decompress(ReadInputFile)
        DeBYML = oead.byml.from_binary(DeYaz0)
        Output = oead.byml.to_text(DeBYML)

        InsertRail(Output, RailString)
        with open("backup/backup.smubin", 'wb') as BackupFile:
            BackupFile.write(ReadInputFile)


def CoreCalculation():
    #Grab all the needed variables
    global X
    global Y
    global Z
    global HashId
    global IsClosed
    global RailType
    global Translate
    global NextDistanceIndex
    global NextDistanceArray
    global CurrentPoint
    global FilePath

    with open("DefaultPath.txt", "r") as Path:
        FilePath = Path.read()

    X[CurrentPoint] = int(top.XEntry.get())
    Y[CurrentPoint] = int(top.YEntry.get())
    Z[CurrentPoint] = int(top.ZEntry.get())

    NextDistanceIndexCounter = 0
    MidpointCounter = -1
    XSum = 0
    YSum = 0
    ZSum = 0
    # Set HashId
    HashID = top.HashIDEntry.get()
    #Set IsClosed
    IsClosed = top.IsClosedDropdown.get()
    #Set RailType
    RailType = top.RailTypeDropdown.get()
    # Set NextDistanceIndex
    while NextDistanceIndexCounter < len(X)-1:
        NextDistanceIndex.append(NextDistanceIndexCounter)
        print(NextDistanceIndexCounter)
        NextDistanceIndexCounter = NextDistanceIndexCounter + 1
    # Calculate distance formula for NextDistance
    for LineNum in NextDistanceIndex:
        NextDistance = math.sqrt((X[1+LineNum]-X[0+LineNum])**2+(Y[1+LineNum]-Y[0+LineNum])**2+(Z[1+LineNum]-Z[0+LineNum])**2)
        NextDistanceArray.append(NextDistance)
    #Calculate midpoint for Translate
    while MidpointCounter < len(X)-1:
        MidpointCounter += 1
        print("MidPointCounter: " + str(MidpointCounter))
        XSum += X[MidpointCounter]
        YSum += Y[MidpointCounter]
        ZSum += Z[MidpointCounter]
    Translate[0] = XSum/len(X)
    Translate[1] = YSum/len(Y)
    Translate[2] = ZSum/len(Z)

    # Create one-time initial string + first point string
    InitString = ("- HashId: !u " + HashID + "\n" + "  IsClosed: " + str(IsClosed) + "\n" + "  RailPoints:" + "\n" + "  - '!Parameters': {IsAdjustPosAndDirToPoint: false, WaitASKeyName: Search, WaitFrame: 60.0}" + "\n" + "    NextDistance: " + str(NextDistanceArray[0]) + "\n" + "    PrevDistance: " + str(-1) + "\n" + "    Translate: " + "[" + str(X[0]) + ", " + str(Y[0]) + ", " + str(Z[0]) + "]" + "\n" + "    UnitConfigName: GuidePoint")
    PrevDistance = str(NextDistanceArray[0])

    # Create repeatable main body string
    BodyString = ""
    for PointNum in range(1, len(X)-1):
        BodyString = (BodyString + "\n" + "  - '!Parameters': {IsAdjustPosAndDirToPoint: false, WaitFrame: 0.0}" + "\n" + "    NextDistance: " + str(NextDistanceArray[PointNum]) + "\n" + "    PrevDistance: " + str(PrevDistance) + "\n" + "    Translate: " + "[" + str(X[PointNum]) + ", " + str(Y[PointNum]) + ", " + str(Z[PointNum]) + "]" + "\n" + "    UnitConfigName: GuidePoint")
        PrevDistance = NextDistanceArray[PointNum]
    # Create One-time end string + end point string
    EndString = ("\n" + "  - '!Parameters': {IsAdjustPosAndDirToPoint: false, WaitASKeyName: Search, WaitFrame: 60.0}" + "\n" + "    NextDistance: " + str(-1) + "\n" + "    PrevDistance: " + str(PrevDistance) + "\n" + "    Translate: " + "[" + str(X[-1]) + ", " + str(Y[-1]) + ", " + str(Z[-1]) + "]" + "\n" + "    UnitConfigName: GuidePoint" + "\n" + "  RailType: " + RailType + "\n" + "  Translate: " + str(Translate) + "\n" + "  UnitConfigName: Guide")
    FinalString = (InitString + BodyString + EndString)
    clipboard.copy(FinalString)
    print(FinalString)
    ReadFromFile(FinalString)



import sys

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    from tkinter import filedialog
    py3 = True

import Gui_Support

top = 0

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    root.iconbitmap('Rails.ico')
    global top
    top = Toplevel1 (root)
    Gui_Support.init(root, top)
    root.mainloop()

w = None
def create_Toplevel1(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_Toplevel1(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    global top
    top = Toplevel1 (w)
    Gui_Support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_Toplevel1():
    global w
    w.destroy()
    w = None

# Define the functions to move through points
def NextPoint():
    global CurrentPoint
    global top
    global X
    global Y
    global Z
    global WindowX
    global WindowY
    global HashID
    # This isn't needed for some reason.
    global root

    print(CurrentPoint + 1)
    X[CurrentPoint] = int(top.XEntry.get())
    Y[CurrentPoint] = int(top.YEntry.get())
    Z[CurrentPoint] = int(top.ZEntry.get())
    print(X)
    print(Y)
    print(Z)
    if (CurrentPoint < len(X)-1):
        CurrentPoint = CurrentPoint + 1
    HashID = top.HashIDEntry.get()
    WindowX = root.winfo_x()
    WindowY = root.winfo_y()
    top = Toplevel1 (root)


def PrevPoint():
    global CurrentPoint
    global top
    global X
    global Y
    global Z
    global WindowX
    global WindowY
    global HashID
    # This isn't needed for some reason.
    global root

    print(CurrentPoint + 1)
    X[CurrentPoint] = int(top.XEntry.get())
    Y[CurrentPoint] = int(top.YEntry.get())
    Z[CurrentPoint] = int(top.ZEntry.get())
    print(X)
    print(Y)
    print(Z)
    if (CurrentPoint > 0):
        CurrentPoint = CurrentPoint - 1
    HashID = top.HashIDEntry.get()
    WindowX = root.winfo_x()
    WindowY = root.winfo_y()
    top = Toplevel1 (root)

def AddPoint():
    global X
    global Y
    global Z
    X.append(0)
    Y.append(0)
    Z.append(0)

def RemovePoint():
    global X
    global Y
    global Z
    global CurrentPoint
    global WindowX
    global WindowY
    # This isn't needed for some reason.
    global root

    if len(X) > 2:
        if CurrentPoint >= len(X)-1:
            CurrentPoint = len(X)-2
        X.pop()
        Y.pop()
        Z.pop()
    WindowX = root.winfo_x()
    WindowY = root.winfo_y()
    top = Toplevel1 (root)

def EnterPath():
    global FilePath

    with open("DefaultPath.txt", "r") as Path:
        FilePath = Path.read()
    top.PathEntry = filedialog.askopenfilename(initialdir=FilePath, title="Select File to Modify")
    #top.PathEntry.place(relx=0.225, rely=--0.65, relheight=0.047, relwidth=0.165)


class Toplevel1:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''

        global X
        global Y
        global Z
        global HashID
        global WindowX
        global WindowY

        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("600x450+"+str(WindowX)+"+"+str(WindowY))
        top.minsize(120, 1)
        top.maxsize(1684, 1031)
        top.resizable(1, 1)
        top.title("Rails")
        top.configure(background="#d9d9d9")
        top.configure(cursor="arrow")

        self.Button1 = tk.Button(top)
        self.Button1.place(relx=-0.017, rely=-0.022, height=464, width=147)
        self.Button1.configure(activebackground="#ececec")
        self.Button1.configure(activeforeground="#000000")
        self.Button1.configure(background="#747474")
        self.Button1.configure(borderwidth="5")
        self.Button1.configure(command=PrevPoint)
        self.Button1.configure(disabledforeground="#a3a3a3")
        self.Button1.configure(foreground="#000000")
        self.Button1.configure(highlightbackground="#a3a3a3")
        self.Button1.configure(highlightcolor="black")
        self.Button1.configure(pady="0")
        self.Button1.configure(relief="sunken")
        self.Button1.configure(text='''Previous''')

        self.Button2 = tk.Button(top)
        self.Button2.place(relx=0.767, rely=-0.022, height=464, width=147)
        self.Button2.configure(activebackground="#ececec")
        self.Button2.configure(activeforeground="#000000")
        self.Button2.configure(background="#747474")
        self.Button2.configure(borderwidth="5")
        self.Button2.configure(command=NextPoint)
        self.Button2.configure(disabledforeground="#a3a3a3")
        self.Button2.configure(foreground="#000000")
        self.Button2.configure(highlightbackground="#d9d9d9")
        self.Button2.configure(highlightcolor="black")
        self.Button2.configure(pady="0")
        self.Button2.configure(text='''Next''')

        self.Button3 = tk.Button(top)
        self.Button3.place(relx=0.600, rely=--0.55, height=100, width=100)
        self.Button3.configure(activebackground="#ececec")
        self.Button3.configure(activeforeground="#000000")
        self.Button3.configure(background="#fca103")
        self.Button3.configure(borderwidth="5")
        self.Button3.configure(command=EnterPath)
        self.Button3.configure(disabledforeground="#a3a3a3")
        self.Button3.configure(foreground="#000000")
        self.Button3.configure(highlightbackground="#d9d9d9")
        self.Button3.configure(highlightcolor="black")
        self.Button3.configure(pady="0")
        self.Button3.configure(relief="flat")
        self.Button3.configure(text='''Select File \n (to Modify)''')

        self.Button4 = tk.Button(top)
        self.Button4.place(relx=0.7750, rely=--0.7, height=135, width=135)
        self.Button4.configure(activebackground="#ececec")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#8b00db")
        self.Button4.configure(borderwidth="5")
        self.Button4.configure(command=AddPoint)
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(relief="flat")
        self.Button4.configure(text='''Add Point''')

        self.Button4 = tk.Button(top)
        self.Button4.place(relx=-0.005, rely=--0.7, height=135, width=135)
        self.Button4.configure(activebackground="#ececec")
        self.Button4.configure(activeforeground="#000000")
        self.Button4.configure(background="#8b00db")
        self.Button4.configure(borderwidth="5")
        self.Button4.configure(command=RemovePoint)
        self.Button4.configure(disabledforeground="#a3a3a3")
        self.Button4.configure(foreground="#000000")
        self.Button4.configure(highlightbackground="#d9d9d9")
        self.Button4.configure(highlightcolor="black")
        self.Button4.configure(pady="0")
        self.Button4.configure(relief="flat")
        self.Button4.configure(text='''Remove Point''')

        self.Button5 = tk.Button(top)
        self.Button5.place(relx=0.600, rely=--0.77, height=100, width=100)
        self.Button5.configure(activebackground="#ececec")
        self.Button5.configure(activeforeground="#000000")
        self.Button5.configure(background="#0000c7")
        self.Button5.configure(borderwidth="5")
        self.Button5.configure(command=CoreCalculation)
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(relief="flat")
        self.Button5.configure(text='''Insert Rail''')


        self.XEntry = ttk.Entry(top)
        self.XEntry.place(relx=0.383, rely=0.356, relheight=0.047, relwidth=0.21)

        self.XEntry.configure(takefocus="")
        self.XEntry.configure(cursor="xterm")

        self.XEntry.insert(0, X[CurrentPoint])

        self.YEntry = ttk.Entry(top)
        self.YEntry.place(relx=0.383, rely=0.467, relheight=0.047, relwidth=0.21)

        self.YEntry.configure(takefocus="")
        self.YEntry.configure(cursor="xterm")

        self.YEntry.insert(0, Y[CurrentPoint])

        self.ZEntry = ttk.Entry(top)
        self.ZEntry.place(relx=0.383, rely=0.578, relheight=0.047, relwidth=0.21)

        self.ZEntry.configure(takefocus="")
        self.ZEntry.configure(cursor="xterm")

        self.ZEntry.insert(0, Z[CurrentPoint])

        self.HashIDEntry = ttk.Entry(top)
        self.HashIDEntry.place(relx=0.225, rely=--0.85, relheight=0.047, relwidth=0.165)

        self.HashIDEntry.configure(takefocus="")
        self.HashIDEntry.configure(cursor="xterm")

        self.HashIDEntry.insert(0, HashID)



        self.CurrnetPointLabel = ttk.Label(top)
        self.CurrnetPointLabel.place(relx=0.45, rely=0.1, height=19, width=45)
        self.CurrnetPointLabel.configure(background="#d9d9d9")
        self.CurrnetPointLabel.configure(foreground="#000000")
        self.CurrnetPointLabel.configure(font="TkDefaultFont")
        self.CurrnetPointLabel.configure(relief="flat")
        self.CurrnetPointLabel.configure(anchor='center')
        self.CurrnetPointLabel.configure(justify='center')
        self.CurrnetPointLabel.configure(text="Point " + str(CurrentPoint+1))

        self.XLabel = ttk.Label(top)
        self.XLabel.place(relx=0.45, rely=0.311, height=19, width=45)
        self.XLabel.configure(background="#d9d9d9")
        self.XLabel.configure(foreground="#000000")
        self.XLabel.configure(font="TkDefaultFont")
        self.XLabel.configure(relief="flat")
        self.XLabel.configure(anchor='center')
        self.XLabel.configure(justify='center')
        self.XLabel.configure(text='''X''')

        self.YLabel = ttk.Label(top)
        self.YLabel.place(relx=0.45, rely=0.422, height=19, width=45)
        self.YLabel.configure(background="#d9d9d9")
        self.YLabel.configure(foreground="#000000")
        self.YLabel.configure(font="TkDefaultFont")
        self.YLabel.configure(relief="flat")
        self.YLabel.configure(anchor='center')
        self.YLabel.configure(justify='center')
        self.YLabel.configure(text='''Y''')

        self.ZLabel = ttk.Label(top)
        self.ZLabel.place(relx=0.45, rely=0.533, height=19, width=45)
        self.ZLabel.configure(background="#d9d9d9")
        self.ZLabel.configure(foreground="#000000")
        self.ZLabel.configure(font="TkDefaultFont")
        self.ZLabel.configure(relief="flat")
        self.ZLabel.configure(anchor='center')
        self.ZLabel.configure(justify='center')
        self.ZLabel.configure(text='''Z''')

        self.HashIDLabel = ttk.Label(top)
        self.HashIDLabel.place(relx=0.265, rely=0.80, height=19, width=45)
        self.HashIDLabel.configure(background="#d9d9d9")
        self.HashIDLabel.configure(foreground="#000000")
        self.HashIDLabel.configure(font="TkDefaultFont")
        self.HashIDLabel.configure(relief="flat")
        self.HashIDLabel.configure(anchor='center')
        self.HashIDLabel.configure(justify='center')
        self.HashIDLabel.configure(text='''HashID''')

        self.IsClosedLabel = ttk.Label(top)
        self.IsClosedLabel.place(relx=0.435, rely=0.90, height=19, width=50)
        self.IsClosedLabel.configure(background="#d9d9d9")
        self.IsClosedLabel.configure(foreground="#000000")
        self.IsClosedLabel.configure(font="TkDefaultFont")
        self.IsClosedLabel.configure(relief="flat")
        self.IsClosedLabel.configure(anchor='center')
        self.IsClosedLabel.configure(justify='center')
        self.IsClosedLabel.configure(text='''IsClosed''')

        self.RailTypeLabel = ttk.Label(top)
        self.RailTypeLabel.place(relx=0.265, rely=0.90, height=19, width=50)
        self.RailTypeLabel.configure(background="#d9d9d9")
        self.RailTypeLabel.configure(foreground="#000000")
        self.RailTypeLabel.configure(font="TkDefaultFont")
        self.RailTypeLabel.configure(relief="flat")
        self.RailTypeLabel.configure(anchor='center')
        self.RailTypeLabel.configure(justify='center')
        self.RailTypeLabel.configure(text='''RailType''')

        self.IsClosedDropdown = ttk.Combobox(top)
        self.IsClosedDropdown.place(relx=0.400, rely=--0.95, relheight=0.047, relwidth=0.165)
        self.IsClosedValueList = ['true','false',]
        self.IsClosedDropdown.configure(values=self.IsClosedValueList)
        self.IsClosedDropdown.configure(takefocus="")

        self.RailTypeDropdown = ttk.Combobox(top)
        self.RailTypeDropdown.place(relx=0.225, rely=--0.95, relheight=0.047, relwidth=0.165)
        self.RailTypeValueList = ['Linear','Bezier',]
        self.RailTypeDropdown.configure(values=self.RailTypeValueList)
        self.RailTypeDropdown.configure(takefocus="")

if __name__ == '__main__':
    vp_start_gui()
