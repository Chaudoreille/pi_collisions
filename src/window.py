import wx
from block import Block


class PiFrame(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent is initialized
        super(PiFrame, self).__init__(*args, **kw)

        # create a menu bar
        self.makeMenuBar()

        # create sizers for buttons
        self.panel = wx.Panel(self, wx.ID_ANY)
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        self.playBtn = wx.Button(self.panel, wx.ID_ANY, "play")
        self.playBtn.Bind(wx.EVT_BUTTON, self.MoveBlocks())

        hbox.Add(self.playBtn, 0, wx.ALIGN_BOTTOM | wx.BOTTOM, 5)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER)

        self.panel.SetSizer(vbox)
        self.Centre()

        # create a status bar
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Collision Counter")
        self.InitUI()

    def MoveBlocks(self):
        pass

    def makeMenuBar(self):
        """
        A menu bar is composed of menus, which are composed of menu items.
        This method builds a set of menus and binds handlers to be called
        when the menu item is selected.
        """

        # Make a file menu with Hello and Exit items
        fileMenu = wx.Menu()

        # the "\t..." syntax defines an accelerator key that also triggers
        # the same event
        helloItem = fileMenu.Append(-1, "&Hello...\tCtrl-H",
                                    "Help string shown in status bar for this \
                                    menu item")
        fileMenu.AppendSeparator()

        # When using a stock ID we don't need to specify the menu item's label
        exitItem = fileMenu.Append(wx.ID_EXIT)

        # Now a help menu for the about item
        helpMenu = wx.Menu()
        aboutItem = helpMenu.Append(wx.ID_ABOUT)

        # Make the menu bar and add the two menus to it. The '&' defines
        # that the next letter is the "mnemonic" for the menu item. On the
        # plateforms that support it thise letters are underlined and can be
        # triggered from the keyboard.
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu, "&File")
        menuBar.Append(helpMenu, "&Help")

        # Give the menu bar to the frame
        self.SetMenuBar(menuBar)

        # Finally associate a handler function with the EVT_MENU event for
        # each of the menu items. That means that when that menu item is
        # activated then the associated handler function will be called.
        self.Bind(wx.EVT_MENU, self.OnHello, helloItem)
        self.Bind(wx.EVT_MENU, self.OnExit, exitItem)
        self.Bind(wx.EVT_MENU, self. OnAbout, aboutItem)

    def InitUI(self):
        # Initiate the "drawing board"
        self.blocks = [Block(10, 10), Block(200, 100)]

        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Centre()
        self.Show(True)

    def OnEditBlocks(self, event):
        """ Edit Block masses. """
        pass

    def OnPaint(self, event):
        dc = wx.PaintDC(self)
        controlPanelHeight = 42
        bottomWindow = 78
        framePadding = 10

        frame = {
            "top": framePadding,
            "bottom": self.GetSize()[1] - bottomWindow -
            controlPanelHeight - framePadding,
            "left": framePadding,
            "right": self.GetSize()[0] - 2 * framePadding
        }
        # controlPanel = {
        #     "top": self.GetSize()[1] - bottomWindow - controlPanelHeight,
        #     "bottom": self.GetSize()[1] - bottomWindow,
        #     "left": 0,
        #     "right": self.GetSize()[0],
        # }

        # set Background color
        dc.SetBackground(wx.Brush("white"))
        dc.Clear()

        # draw frame
        dc.SetBrush(wx.Brush("black"))
        dc.DrawLine(frame["left"], frame["bottom"],
                    frame["left"], frame["top"])
        dc.DrawLine(frame["left"], frame["bottom"],
                    frame["right"], frame["bottom"])

        # this draws the little "solid wall" hash lines on left border
        height = frame["bottom"]

        while height >= frame["top"] + 10:
            dc.DrawLine(frame["left"] - 10, height, frame["left"], height - 10)
            height -= 15

        # define a mass multiplier so that the blocks are (almost)
        # always in frame. Scale both blocks with the multiplier
        # We order blocks by size. biggest block defines mutliplier first
        self.blocks.sort(key=lambda x: x.mass)
        biggestBlock = self.blocks[-1]
        smallestBlock = self.blocks[0]

        multiplier = 0.1 * (frame["right"] - frame["left"]) / biggestBlock.mass

        # if smallest block isn't visible, we make it visible
        # fixed minimum of 5x5 pixels
        # and the bigger block will scale accordingly
        # a too big of a difference between the two blocks will make
        # the bigger block go out of frame.
        if (smallestBlock.mass * multiplier < 5):
            multiplier = 5 / smallestBlock.mass

        minimalWindowHeight = biggestBlock.mass * multiplier + bottomWindow
        + controlPanelHeight + 2 * framePadding

        # if window is too small to display the bigger block,
        # we enlarge the window to display the block (to screen size limit)
        if (minimalWindowHeight > self.GetSize()[1]):
            self.SetSize(0, 0, minimalWindowHeight * 2, minimalWindowHeight)

        # draw Blocks in frame
        # 0 is top-left for wxPython but bottom-left on frame.
        # Taking that in consideration, all our drawings on Y axis will be
        # "substracted" from frame["bottom"]
        for block in self.blocks:
            dc.SetBrush(wx.Brush(wx.Colour(255, 255, 0)))
            dc.DrawRectangle(frame["left"] + block.x,
                             frame["bottom"] - block.mass * multiplier + 1,
                             block.mass * multiplier, block.mass * multiplier)

    # example function
    def OnExit(self, event):
        """ Close the frame, terminating the application."""
        self.Close(True)

    # example function // no use
    def OnHello(self, event):
        """Say hello to the user."""
        wx.MessageBox('Hello user!')

    # example function
    def OnAbout(self, event):
        """Display an About Dialog"""
        wx.MessageBox("Set masses for 2 blocks and ravel\
                      before their number of collisions",
                      "About Collision counter",
                      wx.OK | wx.ICON_INFORMATION)