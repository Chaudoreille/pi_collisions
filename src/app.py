import wx
from window import PiFrame


def main():
    # When this module is run (not imported) then create the app,
    # the frame, show it and start the event loop
    app = wx.App()
    frame = PiFrame(None, title="Collision counter")
    frame.SetSize(0, 0, 1000, 500)
    frame.Show()
    app.MainLoop()


if __name__ == '__main__':
    main()
