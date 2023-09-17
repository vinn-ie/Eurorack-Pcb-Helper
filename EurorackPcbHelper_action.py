import os
import wx
from pcbnew import *

from.EPH_InputDialog import InputDialog
from .EPH_CreateModule import CreateModule

class EurorackPcbHelper(ActionPlugin):
    def defaults(self):
        self.name = "Eurorack PCB Helper"
        self.category = "Design Tools"
        self.description = "Plugin to assist in generating Eurorack PCBs and Faceplates"
        self.show_toolbar_button = False
        # self.icon_file_name = os.path.join(os.path.dirname(__file__), 'icon.png')

    def Run(self):
        # Show the custom dialog and process user input
        dlg = InputDialog(None, title="Eurorack PCB Helper")
        result = dlg.ShowModal()

        if result == wx.ID_OK:
            input = dlg.GetChoices()
            CreateModule(input)
            
        dlg.Destroy()