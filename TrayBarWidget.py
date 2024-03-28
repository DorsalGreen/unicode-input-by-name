import wx
import wx.adv
import images
import meta

class TrayBarWidget(wx.adv.TaskBarIcon):
    def __init__(self, parentWindow):
        wx.adv.TaskBarIcon.__init__(self)
        
        self.mainWindow = parentWindow
        
        #Show the icon in the taskbar
        self.SetIcon(images.upsilon16.Icon, meta.APPNAME)

        #self.Bind(wx.adv.EVT_TASKBAR_CLICK, self.on_hotkey)
        self.Bind(wx.adv.EVT_TASKBAR_LEFT_UP, self.OnLeftClick)
        # Bind the ID from the context menu to this function
        self.Bind(wx.EVT_MENU, self.OnTaskBarClose, id=1)

    def CreatePopupMenu(self):
        # Create the Pop-Up-menu
        menu = wx.Menu(style = wx.MENU_TEAROFF)
        
        # Create the items for the menu
        item = wx.MenuItem(menu, 1, text="Quit")
        menu.Append(item)
        return menu

    def OnTaskBarClose(self, event):
        self.mainWindow.on_exitProgram(event)

    def OnLeftClick(self, event):
        self.mainWindow.on_hotkey(event)