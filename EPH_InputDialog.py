import os
import wx

class InputDialog(wx.Dialog):
    def __init__(self, *args, **kw):
        super(InputDialog, self).__init__(*args, **kw)

        self.InitUI()
        self.SetTitle("Eurorack Options")
        self.CenterOnScreen()  # Center the dialog on screen

    def InitUI(self):
        main_vbox = wx.BoxSizer(wx.VERTICAL)

        # Dropdown for selection
        self.rb = wx.RadioBox(self, label='Select Design Type', choices=['Faceplate', 'PCB'], majorDimension=1, style=wx.RA_SPECIFY_ROWS)
        self.rb.Bind(wx.EVT_RADIOBOX, self.OnRadioBoxChanged)

        # FlexGridSizer for numeric entries
        grid_sizer = wx.FlexGridSizer(2, 2, 10, 10)
        grid_sizer.AddGrowableCol(1, 1)  # Make the second column expandable

        # HP
        self.hp_label = wx.StaticText(self, label='HP:')
        self.hp_value = wx.TextCtrl(self, size=(80, -1))
        grid_sizer.Add(self.hp_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid_sizer.Add(self.hp_value, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, 5)

        # Corner radius
        self.corner_label = wx.StaticText(self, label='Corner radius (mm):')
        self.corner_value = wx.TextCtrl(self, size=(80, -1))
        grid_sizer.Add(self.corner_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid_sizer.Add(self.corner_value, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, 5)

        # Mount Hole Width
        self.mh_width_label = wx.StaticText(self, label='MH Width (mm):')
        self.mh_width_value = wx.TextCtrl(self, size=(80, -1))
        grid_sizer.Add(self.mh_width_label, 0, wx.ALIGN_LEFT | wx.ALL, 5)
        grid_sizer.Add(self.mh_width_value, 0, wx.ALIGN_RIGHT | wx.EXPAND | wx.ALL, 5)

        # Checkboxes
        self.inc_mounting_holes_cb = wx.CheckBox(self, label='Include rear PCB mounting holes')

        # Button
        btn_hbox = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, wx.ID_OK, 'Ok')
        closeButton = wx.Button(self, wx.ID_CANCEL, 'Close')
        btn_hbox.Add(okButton, 0, wx.ALL, 5)
        btn_hbox.Add(closeButton, 0, wx.ALL, 5)

        main_vbox.Add(self.rb, 0, wx.ALL | wx.EXPAND, 5)
        main_vbox.Add(grid_sizer, 0, wx.ALL | wx.EXPAND, 5)
        main_vbox.Add(self.inc_mounting_holes_cb, 0, wx.ALL | wx.EXPAND, 5)
        main_vbox.Add(btn_hbox, 0, wx.ALIGN_CENTER | wx.ALL, 5)

        self.SetSizer(main_vbox) 
        self.OnRadioBoxChanged(None)

    def OnRadioBoxChanged(self, event):
        selection = self.rb.GetStringSelection()
        if selection != "Faceplate":
            self.mh_width_label.Hide()
            self.mh_width_value.Hide()
        else:
            self.mh_width_label.Show()
            self.mh_width_value.Show()

        self.Layout()
        self.Fit()



    def GetChoices(self):
        return {
            "type"      :   self.rb.GetStringSelection(),
            "hp"        :   self.hp_value.GetValue(),
            "rad"       :   self.corner_value.GetValue(),
            "mh_w"      :   self.mh_width_value.GetValue(),
            "pcb_mh"    :   self.inc_mounting_holes_cb.GetValue(),
        }

