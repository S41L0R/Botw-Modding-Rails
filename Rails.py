# Import libraries
import clipboard
import math
import oead
import zlib
import os
from tkinter import messagebox
#from tkinter import ttk

# Set up points
X = [1.0, 3.0, 2.0]
Y = [1.0, 7.0, 15.0]
Z = [1.0, 5.0, 4.0]

# Set up HashID
HashID = "Auto"

# Set up other preferences
IsClosed = "true"
RailType = "Bezier"
Translate = [100, 50, 25]

# Set up index for NextDistance
NextDistanceIndex = []

# Set up array for NextDistance
NextDistanceArray = []

# Set up CurrentPoint. This keeps track of what point you're editing in the GUI.
CurrentPoint = 0

#Set up paths
FilePath = ""
FolderPath = ""


#Set up window position
WindowX = 587
WindowY = 152




# Set up paramDict

paramDict = [{
    "IsAdjustPosAndDirToPoint": "false",
    "WaitASKeyName": "Search",
    "WaitFrame": "60.0"
},
{
    "IsAdjustPosAndDirToPoint": "false",
    "WaitASKeyName": "Search",
    "WaitFrame": "60.0"
},
{
    "IsAdjustPosAndDirToPoint": "false",
    "WaitASKeyName": "Search",
    "WaitFrame": "60.0"
}]




#Define WriteToFile - this writes your data to the static file.
def WriteToFile(InputText):
    InputBytes = oead.byml.from_text(InputText)
    BYML = oead.byml.to_binary(InputBytes, True, 2)
    Yaz0 = oead.yaz0.compress(BYML)
    with open(FilePath, "wb") as OutputFile:
        WrittenOutputFile = OutputFile.write(Yaz0)

#Define InsertRail - This takes the unedited static file text and injects the rail into it.
#It then calls WriteToFile.
def InsertRail(Input, RailString):
    if (Input.find("Rails: []") == -1):
        OutputText = Input + "\n" + RailString
    else:
        OutputText = Input + "Rails:" + "\n" + RailString

    #print(OutputText)
    #clipboard.copy(OutputText)
    #print(RailString)
    WriteToFile(OutputText)

#Define ReadFromFile. This reads all the data in the file and stores it as a string.
#It then calls InsertRail, only if Continue is passed into it as true.
#This functionality is for when you don't want to continue through, and just want to read the file.
def ReadFromFile(RailString, Continue, CurrentPath):
    #FilePath = top.PathEntry.get()
    with open(CurrentPath, 'rb') as InputFile:
        ReadInputFile = InputFile.read()
        DeYaz0 = oead.yaz0.decompress(ReadInputFile)
        DeBYML = oead.byml.from_binary(DeYaz0)
        Output = oead.byml.to_text(DeBYML)
        if (Continue == True):
            InsertRail(Output, RailString)
            with open("backup/backup.smubin", 'wb') as BackupFile:
                BackupFile.write(ReadInputFile)
        elif (Continue == False):
            return Output

#This creates the railstring.
def CoreCalculation(Continue):
    #Grab all the needed variables
    global X
    global Y
    global Z
    global HashID
    global IsClosed
    global RailType
    global Translate
    global NextDistanceIndex
    global NextDistanceArray
    global CurrentPoint
    global FilePath
    global FolderPath
    global FinalString



    #Read DefaultPath and save it as FilePath
    try:
        FolderPath = top.PathEntry
        if (FolderPath == ""):
            with open("DefaultPath.txt", "r") as Path:
                FolderPath = Path.read()
    except AttributeError:
        messagebox.showerror("You messed up.", "You need to specify the seciton folder!")
        print("You need to specify the seciton folder!")
        return
    #Find new HashID
    HighestHashID = 0
    for i in os.listdir(FolderPath):
        if os.path.isfile(os.path.join(FolderPath,i)) and 'Dynamic' in i:
            FilePath = FolderPath + "//" + i
    LineList = ReadFromFile(None, False, FilePath).splitlines()
    HashIDReadCurrentLine = 0;
    for line in LineList:
        #print("Line: " + line)
        if ("- HashId" in line):
            splitLine = line.split()
            CurrentHashID = int(splitLine[3], 0)
            if (CurrentHashID > HighestHashID):
                HighestHashID = CurrentHashID
        HashIDReadCurrentLine += 1;

    for i in os.listdir(FolderPath):
        if os.path.isfile(os.path.join(FolderPath,i)) and 'Static' in i:
            FilePath = FolderPath + "//" + i
    LineList = ReadFromFile(None, False, FilePath).splitlines()
    HashIDReadCurrentLine = 0;
    for line in LineList:
        #print("Line: " + line)
        if ("- HashId" in line):
            splitLine = line.split()
            CurrentHashID = int(splitLine[3], 0)
            if (CurrentHashID > HighestHashID):
                HighestHashID = CurrentHashID
        HashIDReadCurrentLine += 1;

    #print("HighestHashID: " + str(HighestHashID))
    HashID = str(hex(HighestHashID + 1))
    #print(HashID)


    X[CurrentPoint] = float(top.XEntry.get())
    Y[CurrentPoint] = float(top.YEntry.get())
    Z[CurrentPoint] = float(top.ZEntry.get())

    NextDistanceIndexCounter = 0
    MidpointCounter = -1
    XSum = 0
    YSum = 0
    ZSum = 0
    # Set HashId
    if (top.HashIDEntry.get() != "Auto"):
        HashID = str(hex(int(top.HashIDEntry.get(), 0)))
    #Set IsClosed
    IsClosed = top.IsClosedDropdown.get()
    #Set RailType
    RailType = top.RailTypeDropdown.get()
    print(RailType)
    if (RailType != "Bezier" and RailType != "Linear"):
        messagebox.showerror("You messed up.", "Please specify RailType! It can only be Bezier or Linear.")
        print("Please specify RailType! It can only be Bezier or Linear.")
        return
    # Set NextDistanceIndex
    while NextDistanceIndexCounter < len(X)-1:
        NextDistanceIndex.append(NextDistanceIndexCounter)
        #print(NextDistanceIndexCounter)
        NextDistanceIndexCounter = NextDistanceIndexCounter + 1
    # Calculate distance formula for NextDistance
    for LineNum in NextDistanceIndex:
        NextDistance = math.sqrt((X[1+LineNum]-X[0+LineNum])**2+(Y[1+LineNum]-Y[0+LineNum])**2+(Z[1+LineNum]-Z[0+LineNum])**2)
        NextDistanceArray.append(NextDistance)
    #Calculate midpoint for Translate
    while MidpointCounter < len(X)-1:
        MidpointCounter += 1
        #print("MidPointCounter: " + str(MidpointCounter))
        XSum += X[MidpointCounter]
        YSum += Y[MidpointCounter]
        ZSum += Z[MidpointCounter]
    Translate[0] = XSum/len(X)
    Translate[1] = YSum/len(Y)
    Translate[2] = ZSum/len(Z)

    # Create one-time initial string + first point string
    FirstLastDist = math.sqrt((X[-1]-X[0])**2+(Y[-1]-Y[0])**2+(Z[-1]-Z[0])**2)
    if (IsClosed == "true"):
        print("yay")
        InitString = ("- HashId: !u " + HashID + "\n" + "  IsClosed: " + str(IsClosed) + "\n" + "  RailPoints:" + "\n" + f"  - '!Parameters': {paramDict[0]}" + "\n" + "    NextDistance: " + str(NextDistanceArray[0]) + "\n" + "    PrevDistance: " + str(FirstLastDist) + "\n" + "    Translate: " + "[" + str(X[0]) + ", " + str(Y[0]) + ", " + str(Z[0]) + "]" + "\n" + "    UnitConfigName: GuidePoint")
    elif (IsClosed == "false"):
        InitString = ("- HashId: !u " + HashID + "\n" + "  IsClosed: " + str(IsClosed) + "\n" + "  RailPoints:" + "\n" + f"  - '!Parameters': {paramDict[0]}" + "\n" + "    NextDistance: " + str(NextDistanceArray[0]) + "\n" + "    PrevDistance: " + str(NextDistanceArray[0]) + "\n" + "    Translate: " + "[" + str(X[0]) + ", " + str(Y[0]) + ", " + str(Z[0]) + "]" + "\n" + "    UnitConfigName: GuidePoint")
    else:
        messagebox.showerror("You messed up.", "Please specify IsClosed! It can only be true or false.")
        print("Please specify IsClosed! It can only be true or false.")
        return

    # Create repeatable main body string
    BodyString = ""
    PrevDistance = str(NextDistanceArray[0])
    for PointNum in range(1, len(X)-1):
        BodyString = (BodyString + "\n" + f"  - '!Parameters': {paramDict[PointNum]}" + "\n" + "    NextDistance: " + str(NextDistanceArray[PointNum]) + "\n" + "    PrevDistance: " + str(PrevDistance) + "\n" + "    Translate: " + "[" + str(X[PointNum]) + ", " + str(Y[PointNum]) + ", " + str(Z[PointNum]) + "]" + "\n" + "    UnitConfigName: GuidePoint")
        PrevDistance = NextDistanceArray[PointNum]
    # Create One-time end string + end point string
    if (IsClosed == "true"):
        print("yay2")
        EndString = ("\n" + f"  - '!Parameters': {paramDict[-1]}" + "\n" + "    NextDistance: " + str(FirstLastDist) + "\n" + "    PrevDistance: " + str(PrevDistance) + "\n" + "    Translate: " + "[" + str(X[-1]) + ", " + str(Y[-1]) + ", " + str(Z[-1]) + "]" + "\n" + "    UnitConfigName: GuidePoint" + "\n" + "  RailType: " + RailType + "\n" + "  Translate: " + str(Translate) + "\n" + "  UnitConfigName: Guide")
    elif (IsClosed == "false"):
        EndString = ("\n" + f"  - '!Parameters': {paramDict[-1]}" + "\n" + "    NextDistance: " + str(PrevDistance) + "\n" + "    PrevDistance: " + str(PrevDistance) + "\n" + "    Translate: " + "[" + str(X[-1]) + ", " + str(Y[-1]) + ", " + str(Z[-1]) + "]" + "\n" + "    UnitConfigName: GuidePoint" + "\n" + "  RailType: " + RailType + "\n" + "  Translate: " + str(Translate) + "\n" + "  UnitConfigName: Guide")
    FinalString = (InitString + BodyString + EndString)
    #print(FinalString)
    ReadFromFile(FinalString, Continue, FilePath)

def ClipboardCopy():
    global FinalString
    CoreCalculation(False)
    try:
        clipboard.copy(FinalString)
    except NameError:
        return

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
    global IsClosed
    global RailType
    # This isn't needed for some reason.
    global root


    global paramDict
    global optionsRoot
    global optionsWindow

    #print(CurrentPoint + 1)
    X[CurrentPoint] = float(top.XEntry.get())
    Y[CurrentPoint] = float(top.YEntry.get())
    Z[CurrentPoint] = float(top.ZEntry.get())
    IsClosed = top.IsClosedDropdown.get()
    RailType = top.RailTypeDropdown.get()


    try:
        if (optionsWindow.IsAdjustPosAndDirToPoint.get() == "No Entry"):
            del paramDict[CurrentPoint]['IsAdjustPosAndDirToPoint']
        else:
            paramDict[CurrentPoint]['IsAdjustPosAndDirToPoint'] = optionsWindow.IsAdjustPosAndDirToPoint.get()

        if (optionsWindow.WaitASKeyName.get() == "No Entry"):
            del paramDict[CurrentPoint]['WaitASKeyName']
        else:
            paramDict[CurrentPoint]['WaitASKeyName'] = optionsWindow.WaitASKeyName.get()

        if (optionsWindow.WaitFrame.get() == "No Entry"):
            del paramDict[CurrentPoint]['WaitFrame']
        else:
            paramDict[CurrentPoint]['WaitFrame'] = optionsWindow.WaitFrame.get()
    except:
        print("You haven't set that value yet.")

    print(paramDict[CurrentPoint])
    #print(X)
    #print(Y)
    #print(Z)
    if (CurrentPoint < len(X)-1):
        CurrentPoint = CurrentPoint + 1
    if (top.HashIDEntry.get() != "Auto"):
        HashID = str(hex(int(top.HashIDEntry.get(), 0)))
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
    global IsClosed
    global RailType
    # This isn't needed for some reason.
    global root


    global paramDict
    global optionsRoot
    global optionsWindow

    #print(CurrentPoint + 1)
    X[CurrentPoint] = float(top.XEntry.get())
    Y[CurrentPoint] = float(top.YEntry.get())
    Z[CurrentPoint] = float(top.ZEntry.get())
    IsClosed = top.IsClosedDropdown.get()
    RailType = top.RailTypeDropdown.get()


    try:
        if (optionsWindow.IsAdjustPosAndDirToPoint.get() == "No Entry"):
            del paramDict[CurrentPoint]['IsAdjustPosAndDirToPoint']
        else:
            paramDict[CurrentPoint]['IsAdjustPosAndDirToPoint'] = optionsWindow.IsAdjustPosAndDirToPoint.get()

        if (optionsWindow.WaitASKeyName.get() == "No Entry"):
            del paramDict[CurrentPoint]['WaitASKeyName']
        else:
            paramDict[CurrentPoint]['WaitASKeyName'] = optionsWindow.WaitASKeyName.get()

        if (optionsWindow.WaitFrame.get() == "No Entry"):
            del paramDict[CurrentPoint]['WaitFrame']
        else:
            paramDict[CurrentPoint]['WaitFrame'] = optionsWindow.WaitFrame.get()

        if (optionsWindow.Rotate.get() == "No Entry"):
            del paramDict[CurrentPoint]['Rotate']
        else:
            paramDict[CurrentPoint]['Rotate'] = optionsWindow.Rotate.get()
    except:
        print("You haven't set that value yet.")

    print(paramDict[CurrentPoint])
    #print(X)
    #print(Y)
    #print(Z)
    if (CurrentPoint > 0):
        CurrentPoint = CurrentPoint - 1
    if (top.HashIDEntry.get() != "Auto"):
        HashID = str(hex(int(top.HashIDEntry.get(), 0)))
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
    paramDict.append({
        "IsAdjustPosAndDirToPoint": "false",
        "WaitASKeyName": "Search",
        "WaitFrame": "60.0"
    })

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
        paramDict.pop()
    WindowX = root.winfo_x()
    WindowY = root.winfo_y()
    top = Toplevel1 (root)

def EnterPath():
    global FolderPath

    with open("DefaultPath.txt", "r") as Path:
        FolderPath = Path.read()
    #top.PathEntry = filedialog.askopenfilename(initialdir=FilePath, title="Select File to Modify")
    top.PathEntry = filedialog.askdirectory()
    #top.PathEntry.place(relx=0.225, rely=--0.65, relheight=0.047, relwidth=0.165)



def openOptionsWindow():
    global optionsWindow
    global optionsRoot
    optionsRoot = tk.Tk()
    optionsRoot.iconbitmap('Rails.ico')
    optionsWindow = paramLevel(optionsRoot)




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
        self.Button3.configure(text='''Select Folder \n (to Modify)''')

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
        self.Button5.configure(command=lambda: CoreCalculation(True))
        self.Button5.configure(disabledforeground="#a3a3a3")
        self.Button5.configure(foreground="#000000")
        self.Button5.configure(highlightbackground="#d9d9d9")
        self.Button5.configure(highlightcolor="black")
        self.Button5.configure(pady="0")
        self.Button5.configure(relief="flat")
        self.Button5.configure(text='''Insert Rail''')

        self.Button6 = tk.Button(top)
        self.Button6.place(relx=0.400, rely=--0.67, height=100, width=100)
        self.Button6.configure(activebackground="#ececec")
        self.Button6.configure(activeforeground="#000000")
        self.Button6.configure(background="#c70000")
        self.Button6.configure(borderwidth="5")
        self.Button6.configure(command=ClipboardCopy)
        self.Button6.configure(disabledforeground="#a3a3a3")
        self.Button6.configure(foreground="#000000")
        self.Button6.configure(highlightbackground="#d9d9d9")
        self.Button6.configure(highlightcolor="black")
        self.Button6.configure(pady="0")
        self.Button6.configure(relief="flat")
        self.Button6.configure(text='''Copy to Clipboard''')



        self.Button7 = tk.Button(top)
        self.Button7.place(relx=0.405, rely=--0.17, height=25, width=100)
        self.Button7.configure(activebackground="#ececec")
        self.Button7.configure(activeforeground="#000000")
        self.Button7.configure(background="#c70000")
        self.Button7.configure(borderwidth="5")
        self.Button7.configure(command=openOptionsWindow)
        self.Button7.configure(disabledforeground="#a3a3a3")
        self.Button7.configure(foreground="#000000")
        self.Button7.configure(highlightbackground="#d9d9d9")
        self.Button7.configure(highlightcolor="black")
        self.Button7.configure(pady="0")
        self.Button7.configure(relief="flat")
        self.Button7.configure(text='''Parameters''')


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
        self.IsClosedDropdown.insert(0, IsClosed)

        self.RailTypeDropdown = ttk.Combobox(top)
        self.RailTypeDropdown.place(relx=0.225, rely=--0.95, relheight=0.047, relwidth=0.165)
        self.RailTypeValueList = ['Linear','Bezier',]
        self.RailTypeDropdown.configure(values=self.RailTypeValueList)
        self.RailTypeDropdown.configure(takefocus="")
        self.RailTypeDropdown.insert(0, RailType)


class paramLevel:
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
        top.title("Parameters")
        top.configure(background="#d9d9d9")
        top.configure(cursor="arrow")

        self.IsAdjustPosAndDirToPointLabel = ttk.Label(top)
        self.IsAdjustPosAndDirToPointLabel.place(relx=0, rely=0, height=19, width=150)
        self.IsAdjustPosAndDirToPointLabel.configure(background="#d9d9d9")
        self.IsAdjustPosAndDirToPointLabel.configure(foreground="#000000")
        self.IsAdjustPosAndDirToPointLabel.configure(font="TkDefaultFont")
        self.IsAdjustPosAndDirToPointLabel.configure(relief="flat")
        self.IsAdjustPosAndDirToPointLabel.configure(anchor='center')
        self.IsAdjustPosAndDirToPointLabel.configure(justify='center')
        self.IsAdjustPosAndDirToPointLabel.configure(text='''IsAdjustPosAndDirToPoint''')


        self.IsAdjustPosAndDirToPoint = ttk.Combobox(top)
        self.IsAdjustPosAndDirToPoint.place(relx=0.25, rely=--0, relheight=0.047, relwidth=0.165)
        self.IsAdjustPosAndDirToPointValueList = ['true','false', 'No Entry',]
        self.IsAdjustPosAndDirToPoint.configure(values=self.IsAdjustPosAndDirToPointValueList)
        self.IsAdjustPosAndDirToPoint.configure(takefocus="")
        self.IsAdjustPosAndDirToPoint.insert(0, "false")


        self.WaitASKeyNameLabel = ttk.Label(top)
        self.WaitASKeyNameLabel.place(relx=0, rely=0.05, height=19, width=150)
        self.WaitASKeyNameLabel.configure(background="#d9d9d9")
        self.WaitASKeyNameLabel.configure(foreground="#000000")
        self.WaitASKeyNameLabel.configure(font="TkDefaultFont")
        self.WaitASKeyNameLabel.configure(relief="flat")
        self.WaitASKeyNameLabel.configure(anchor='center')
        self.WaitASKeyNameLabel.configure(justify='center')
        self.WaitASKeyNameLabel.configure(text='''WaitASKeyName''')


        self.WaitASKeyName = ttk.Combobox(top)
        self.WaitASKeyName.place(relx=0.25, rely=--0.05, relheight=0.047, relwidth=0.165)
        self.WaitASKeyNameValueList = ['Search','No Entry',]
        self.WaitASKeyName.configure(values=self.WaitASKeyNameValueList)
        self.WaitASKeyName.configure(takefocus="")
        self.WaitASKeyName.insert(0, "Search")


        self.WaitFrameLabel = ttk.Label(top)
        self.WaitFrameLabel.place(relx=0, rely=0.1, height=19, width=150)
        self.WaitFrameLabel.configure(background="#d9d9d9")
        self.WaitFrameLabel.configure(foreground="#000000")
        self.WaitFrameLabel.configure(font="TkDefaultFont")
        self.WaitFrameLabel.configure(relief="flat")
        self.WaitFrameLabel.configure(anchor='center')
        self.WaitFrameLabel.configure(justify='center')
        self.WaitFrameLabel.configure(text='''WaitFrame''')


        self.WaitFrame = ttk.Combobox(top)
        self.WaitFrame.place(relx=0.25, rely=--0.1, relheight=0.047, relwidth=0.165)
        self.WaitFrameValueList = ['60.0','No Entry',]
        self.WaitFrame.configure(values=self.WaitASKeyNameValueList)
        self.WaitFrame.configure(takefocus="")
        self.WaitFrame.insert(0, "60.0")


        self.RotateLabel = ttk.Label(top)
        self.RotateLabel.place(relx=0, rely=0.15, height=19, width=150)
        self.RotateLabel.configure(background="#d9d9d9")
        self.RotateLabel.configure(foreground="#000000")
        self.RotateLabel.configure(font="TkDefaultFont")
        self.RotateLabel.configure(relief="flat")
        self.RotateLabel.configure(anchor='center')
        self.RotateLabel.configure(justify='center')
        self.RotateLabel.configure(text='''Rotate''')


        self.Rotate = ttk.Combobox(top)
        self.Rotate.place(relx=0.25, rely=--0.15, relheight=0.047, relwidth=0.165)
        self.RotateValueList = ['90.0','No Entry',]
        self.Rotate.configure(values=self.RotateValueList)
        self.Rotate.configure(takefocus="")
        self.Rotate.insert(0, "90.0")

if __name__ == '__main__':
    vp_start_gui()
