# -*- coding: utf-8 -*-
""" PyCorrFit
    Paul Müller, Biotec - TU Dresden

    Module tools - chooseimport
    Displays a window that lets the user choose what type
    of data (AC1, AC2, CC12, CC21) he wants to import.

    Dimensionless representation:
    unit of time        : 1 ms
    unit of inverse time: 10³ /s
    unit of distance    : 100 nm
    unit of Diff.coeff  : 10 µm²/s
    unit of inverse area: 100 /µm²
    unit of inv. volume : 1000 /µm³
"""


import numpy as np
import wx

import models as mdls
import doc
import selectcurves


class ChooseImportTypes(wx.Dialog):
    """ This class is used for importing single files from the "Current" menu.
        The model function is defined by the model that is in use.
    """
    # This tool is derived from a wx.frame.
    def __init__(self, parent, curvedict):
        # parent is the main frame of PyCorrFit
        self.parent = parent
        # init
        super(ChooseImportTypes, self).__init__(parent=parent, 
            title="Choose types", size=(250, 200))
        self.keys = list()
         ## Content
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.boxes = dict()
        textinit = wx.StaticText(self.panel, label=doc.chooseimport)
        self.sizer.Add(textinit)
        thekeys = curvedict.keys()
        thekeys.sort()
        for key in thekeys:
            label = key + " (" + str(len(curvedict[key])) + " curves)"
            check = wx.CheckBox(self.panel, label=label)
            self.boxes[key] = check
            self.sizer.Add(check)
            self.Bind(wx.EVT_CHECKBOX, self.OnSetkeys, check)
        btnok = wx.Button(self.panel, wx.ID_OK, 'OK')
        # Binds the button to the function - close the tool
        self.Bind(wx.EVT_BUTTON, self.OnClose, btnok)
        self.sizer.Add(btnok)
        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)
        #Icon
        if parent.MainIcon is not None:
            wx.Dialog.SetIcon(self, parent.MainIcon)
        self.Show(True)


    def OnClose(self, event=None):
        # This is a necessary function for PyCorrFit.
        # Do not change it.
        self.EndModal(wx.ID_OK)
        #self.Show
        #self.Destroy()


    def OnSetkeys(self, event = None):
        self.keys = list()
        for key in self.boxes.keys():
            if self.boxes[key].Value == True:
                self.keys.append(key)


class ChooseImportTypesModel(wx.Dialog):
    """ This class shows a dialog displaying options to choose
        model function on import of data
    """
    # This tool is derived from a wx.frame.
    def __init__(self, parent, curvedict, correlations):
        # parent is the main frame of PyCorrFit
        self.parent = parent
        # init
        super(ChooseImportTypesModel, self).__init__(parent=parent, 
            title="Choose types", size=(250, 200))
        self.curvedict = curvedict
        self.kept_curvedict = curvedict.copy() # Can be edited by user
        self.correlations = correlations
        # List of keys that will be imported by our *parent*
        self.typekeys = list()
        # Dictionary of modelids corresponding to indices in curvedict
        self.modelids = dict()
        ## Content
        self.panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.boxes = dict()
        textinit = wx.StaticText(self.panel, label=doc.chooseimportmulti)
        self.sizer.Add(textinit)
        curvekeys = curvedict.keys()
        curvekeys.sort()
        self.curvekeys = curvekeys
        # Dropdown model selections:
        DropdownList = ["No model selected"] # Contains string in model dropdown
        self.DropdownIndex = [None]          # Contains corresponsing model
        modelkeys = mdls.modeltypes.keys()
        modelkeys.sort()
        for modeltype in modelkeys:
            for modelid in mdls.modeltypes[modeltype]:
                DropdownList.append(modeltype+": "+mdls.modeldict[modelid][1])
                self.DropdownIndex.append(modelid)
        self.ModelDropdown = dict()
        dropsizer = wx.FlexGridSizer(rows=len(modelkeys), cols=3, vgap=5, hgap=5)
        self.Buttons = list()
        i = 8000
        for key in curvekeys:
            # Text with keys and numer of curves
            dropsizer.Add( wx.StaticText(self.panel, label=str(key)) )
            label=" ("+str(len(curvedict[key]))+" curves)"
            button = wx.Button(self.panel, i, label)
            i += 1
            self.Bind(wx.EVT_BUTTON, self.OnSelectCurves, button)
            self.Buttons.append(button)
            dropsizer.Add(button)
            # Model selection dropdown
            dropdown = wx.ComboBox(self.panel, -1, DropdownList[0], (15,30),
               wx.DefaultSize, DropdownList, wx.CB_DROPDOWN|wx.CB_READONLY)
            dropsizer.Add( dropdown )
            self.ModelDropdown[key] = dropdown
            self.Bind(wx.EVT_COMBOBOX, self.OnSetkeys, dropdown)
        self.sizer.Add(dropsizer)
        btnok = wx.Button(self.panel, wx.ID_OK, 'OK')
        # Binds the button to the function - close the tool
        self.Bind(wx.EVT_BUTTON, self.OnClose, btnok)
        self.sizer.Add(btnok)
        self.panel.SetSizer(self.sizer)
        self.sizer.Fit(self)
        self.Show(True)

        if parent.MainIcon is not None:
            wx.Dialog.SetIcon(self, parent.MainIcon)
        self.Show(True)


    def OnClose(self, event=None):
        # This is a necessary function for PyCorrFit.
        # Do not change it.
        self.keepcurvesindex = list()
        for key in self.kept_curvedict.keys():
            self.keepcurvesindex += self.kept_curvedict[key]
        for i in np.arange(len(self.keepcurvesindex)):
            self.keepcurvesindex[i] = int(self.keepcurvesindex[i])
        self.EndModal(wx.ID_OK)
        
        #self.Show
        #self.Destroy()


    def OnSelectCurves(self, buttonevent):
        index = buttonevent.GetId() - 8000
        self.buttonindex = index
        curvedict = dict()
        key = self.curvekeys[index]
        corrcurves = dict()
        for i in self.curvedict[key]:
            corrcurves[str(i)] = self.correlations[int(i)]
        Selector = selectcurves.Wrapper_OnImport(self.parent, corrcurves,
                                                  self.OnSelected)

    def OnSelected(self, keep, remove):
        # Set new button label
        for i in np.arange(len(keep)):
            keep[i] = int(keep[i])
        #button = self.Buttons[self.buttonindex]
        label = " ("+str(len(keep))+" curves)"
        #button.SetLabel(label)
        # Add new content to selected key
        SelectedKey = self.curvekeys[self.buttonindex]
        #self.kept_curvedict[SelectedKey] = keep
        # If there are keys with the same amount of correlations,
        # these are assumed to be AC2, CC12, CC21 etc., so we will remove
        # items from them accordingly.
        diff = set(keep).intersection(set(self.curvedict[SelectedKey]))
        indexes = list()
        for i in np.arange(len(self.curvedict[SelectedKey])):
            for number in diff:
                if number == self.curvedict[SelectedKey][i]:
                    indexes.append(i)
        for j in np.arange(len(self.curvekeys)):
            key = self.curvekeys[j]
            if len(self.curvedict[key]) == len(self.curvedict[SelectedKey]):
                newlist = list()
                for index in indexes:
                    newlist.append(self.curvedict[key][index])
                self.kept_curvedict[key] = newlist
                # Also update buttons
                button = self.Buttons[j]
                button.SetLabel(label)


    def OnSetkeys(self, event = None):
        # initiate objects
        self.typekeys = list()
        self.modelids = dict()
        # iterate through all given keys (AC1, AC2, CC12, etc.)
        for key in self.curvedict.keys():
            # get the dropdown selection for a given key
            modelindex = self.ModelDropdown[key].GetSelection()
            # modelindex is -1 or 0, if no model has been chosen
            if modelindex > 0:
                # Append the key to a list of to be imported types
                self.typekeys.append(key)
                # Append the modelid to a dictionary that has indexes
                # belonging to the imported curves in *parent*
                modelid = self.DropdownIndex[modelindex]
                for index in self.curvedict[key]:
                    # Set different model id for the curves
                    self.modelids[index] = modelid
        self.typekeys.sort()

        


        
