import wx
import json

class Container(wx.Frame):
    
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=(200, 100))

        self.control = wx.TextCtrl(self, size=(10,50))

        self.CreateStatusBar()

        menu = wx.Menu()
        menu.Append(wx.ID_ANY, "&About", " Info")
        menu.AppendSeparator()

        exitItem = menu.Append(wx.ID_EXIT, "E&xit", " Kill it")
        self.Bind(wx.EVT_MENU, self.onExit, exitItem)

        menuBar = wx.MenuBar()
        menuBar.Append(menu, "&File")
        self.SetMenuBar(menuBar)
        self.Show(True)


    def onExit(self, event):
        self.Close(True)


with open('config.json') as f:
    c = json.load(f)
    title = c["title"]

app = wx.App(False)
frame = Container(None, title)
app.MainLoop()






"""
import matplotlib
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure

class MainFrame(wx.Frame): 
    def __init__(self): 
        wx.Frame.__init__(self, None, wx.NewId(), "Main") 
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.figure = Figure(figsize=(1,2))
        self.axe = self.figure.add_subplot(111)
        self.figurecanvas = FigureCanvas(self, -1, self.figure)

        self.buttonPlot = wx.Button(self, wx.NewId(), "Plot")
        self.buttonClear = wx.Button(self, wx.NewId(), "Clear")

        self.sizer.Add(self.figurecanvas, proportion=1, border=5, flag=wx.ALL | wx.EXPAND)
        self.sizer.Add(self.buttonPlot, proportion=0, border=2, flag=wx.ALL)
        self.sizer.Add(self.buttonClear, proportion=0, border=2, flag=wx.ALL)
        self.SetSizer(self.sizer)

        self.figurecanvas.Bind(wx.EVT_LEFT_DCLICK, self.on_dclick)
        self.buttonPlot.Bind(wx.EVT_BUTTON, self.on_button_plot)
        self.buttonClear.Bind(wx.EVT_BUTTON, self.on_button_clear)

        self.subframe_opened = False

    def on_dclick(self, evt):
        self.subframe = SubFrame(self, self.figure)
        self.subframe.Show(True)
        self.subframe_opened = True

    def on_button_plot(self, evt):
        self.axe.plot(range(10), color='green')
        self.figurecanvas.draw()

    def on_button_clear(self, evt):
        if self.subframe_opened:
            self.subframe.Close()
        self.figure.set_canvas(self.figurecanvas)
        self.axe.clear()
        self.figurecanvas.draw()


class SubFrame(wx.Frame): 
    def __init__(self, parent, figure): 
        wx.Frame.__init__(self, parent, wx.NewId(), "Sub")
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.figurecanvas = FigureCanvas(self, -1, figure)
        self.sizer.Add(self.figurecanvas, proportion=1, border=5, flag=wx.ALL | wx.EXPAND)
        self.SetSizer(self.sizer)

        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_close(self, evt):
        self.GetParent().subframe_opened = False
        evt.Skip()



class MyApp(wx.App):
    def OnInit(self):
        frame = MainFrame()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True

app = MyApp(0)
app.MainLoop()    
"""
