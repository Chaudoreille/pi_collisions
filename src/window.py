import wx
from block import Block


class CollisionFrame(wx.Frame):
    def __init__(self, *args, **kw):
        # ensure the parent is initialized
        super(CollisionFrame, self).__init__(*args, **kw)

        self.buttons = {}
        self.display_elements = {}
        self.timer = wx.Timer(self)
        self.panel = wx.Panel(self, wx.ID_ANY)

        # init User Interface
        self.init_UI()

    def init_UI(self):
        self.CreateStatusBar()
        self.SetStatusText("Welcome to Collision Counter")

        self.create_buttons()

        # create sizers for buttons

        self.Centre()

        # Initiate the "drawing board"
        self.blocks = [Block(10, 10), Block(200, 100)]

        self.Bind(wx.EVT_PAINT, self.on_paint)
        self.Centre()
        self.Show(True)

    def create_buttons(self):
        play_button = wx.Button(self.panel, wx.ID_ANY, "Play")
        play_button.Bind(wx.EVT_BUTTON, self.on_play)

        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        hbox.Add(play_button, 0, wx.ALIGN_BOTTOM | wx.BOTTOM, 5)
        vbox.Add(hbox, 1, wx.ALIGN_CENTER)

        self.panel.SetSizer(vbox)
        self.buttons["play"] = play_button

    # def on_edit_blocks(self, event):
    #     """ Edit Block masses. """
    #     pass

    def on_timer(self, event):
        # execute every 10 ms
        pass

    def on_paint(self, event):
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

    def on_play(self, event):
        if not self.timer.IsRunning():
            self.timer.Start(10)  # 10ms intervals
            self.buttons["play"].SetLabel("Stop")
        else:
            self.timer.Stop()
            self.buttons["play"].SetLabel("Play")
