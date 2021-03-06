"""Module tools - RangeSelector

Select the range in which the parameter should reside for fitting.
"""
import numpy as np
import wx

from pycorrfit import models as mdls
from .. import wxutils


class RangeSelector(wx.Frame):
    # This tool is derived from a wx.frame.
    def __init__(self, Page):
        # parent is the main frame of PyCorrFit
        self.parent = Page.parent
        # Get the window positioning correctly
        pos = self.parent.GetPosition()
        pos = (pos[0]+100, pos[1]+100)
        wx.Frame.__init__(self, parent=self.parent, title="Parameter Range",
                          pos=pos, style=wx.DEFAULT_FRAME_STYLE | wx.FRAME_FLOAT_ON_PARENT)
        # Page - the currently active page of the notebook.
        self.Page = self.parent.notebook.GetCurrentPage()
        # Content
        self.panel = wx.Panel(self)
        self.topSizer = wx.BoxSizer(wx.VERTICAL)

        self.WXboxsizerlist = list()
        self.WXparmlist = list()
        self.OnPageChanged(self.Page)
        # Icon
        if self.parent.MainIcon is not None:
            wx.Frame.SetIcon(self, self.parent.MainIcon)
        self.Show(True)

    def FillPanel(self):
        """ Fill the panel with parameters from the page
        """
        corr = self.Page.corr
        self.parameter_range = np.zeros_like(corr.fit_parameters_range)
        leftbound = []
        for item in corr.fit_parameters_range[:, 0]:
            if item is None:
                leftbound.append(-np.inf)
            else:
                leftbound.append(item)
        labels, parmleft = mdls.GetHumanReadableParms(corr.fit_model.id,  # @UnusedVariable
                                                      leftbound)
        rightbound = []
        for item in corr.fit_parameters_range[:, 1]:
            if item is None:
                rightbound.append(np.inf)
            else:
                rightbound.append(item)

        labels, parmright = mdls.GetHumanReadableParms(corr.fit_model.id,
                                                       rightbound)
        self.parameter_range[:, 0] = np.array(parmleft)
        self.parameter_range[:, 1] = np.array(parmright)
        # create line

        self.WXboxsizer = wx.FlexGridSizer(
            rows=len(labels), cols=5, vgap=5, hgap=5)
        for i in range(len(labels)):
            left = wxutils.PCFFloatTextCtrl(self.panel)
            right = wxutils.PCFFloatTextCtrl(self.panel)
            left.SetValue(self.parameter_range[i][0])
            right.SetValue(self.parameter_range[i][1])
            left.Bind(wx.EVT_SPINCTRL, self.OnSetParmRange)
            right.Bind(wx.EVT_SPINCTRL, self.OnSetParmRange)
            text = wx.StaticText(self.panel, label=u'< ')
            text2 = wx.StaticText(self.panel, label=labels[i])
            text3 = wx.StaticText(self.panel, label=u' <')
            self.WXboxsizer.Add(left)
            self.WXboxsizer.Add(text)
            self.WXboxsizer.Add(text2, 0, wx.ALIGN_CENTER, 0)
            self.WXboxsizer.Add(text3)
            self.WXboxsizer.Add(right)
            self.WXparmlist.append([left, [text, text2, text3], right])
        self.WXboxsizer.Layout()

        self.topSizer.Add(self.WXboxsizer)
        self.btnapply = wx.Button(self.panel, wx.ID_ANY, 'Apply')
        self.Bind(wx.EVT_BUTTON, self.OnSetParmRange, self.btnapply)
        self.topSizer.Add(self.btnapply)

        self.topSizer.Layout()
        self.panel.SetSizer(self.topSizer)
        self.topSizer.Fit(self.panel)
        self.SetMinSize((self.topSizer.GetMinSize()[0] + 20,
                         self.topSizer.GetMinSize()[1] + 40))
        self.topSizer.Fit(self)

    def OnClose(self, event=None):
        # This is a necessary function for PyCorrFit.
        # Do not change it.
        self.parent.RangeSelector = None
        self.Destroy()

    def OnPageChanged(self, page=None, trigger=None):
        """
            This function is called, when something in the panel
            changes. The variable `trigger` is used to prevent this
            function from being executed to save stall time of the user.
            Forr a list of possible triggers, see the doc string of
            `tools`.
        """
        # When parent changes
        # This is a necessary function for PyCorrFit.
        # This is stuff that should be done when the active page
        # of the notebook changes.
        if trigger in ["parm_batch", "fit_batch", "page_add_batch"]:
            return
        self.Page = page
        if self.parent.notebook.GetPageCount() == 0:
            self.panel.Disable()
            return
        self.panel.Enable()
        try:
            self.btnapply.Destroy()
        except:
            pass
        for i in np.arange(len(self.WXparmlist)):
            self.WXparmlist[i][0].Destroy()  # start
            self.WXparmlist[i][1][0].Destroy()  # pname
            self.WXparmlist[i][1][1].Destroy()  # pname
            self.WXparmlist[i][2].Destroy()  # end
        del self.WXparmlist
        for i in np.arange(len(self.WXboxsizerlist)):
            self.WXboxsizer.Remove(0)
        self.WXboxsizerlist = list()
        self.WXparmlist = list()
        self.FillPanel()

    def OnSetParmRange(self, e):
        """ Called whenever something is edited in this frame.
            Writes back parameter ranges to the page
        """
        corr = self.Page.corr
        # Read out parameters from all controls
        for i in range(len(self.WXparmlist)):
            self.parameter_range[i][0] = self.WXparmlist[i][0].GetValue()
            self.parameter_range[i][1] = self.WXparmlist[i][2].GetValue()
            if self.parameter_range[i][0] > self.parameter_range[i][1]:
                self.parameter_range[i][1] = 1.01 * \
                    np.abs(self.parameter_range[i][0])
                self.WXparmlist[i][2].SetValue(self.parameter_range[i][1])
        # Set parameters
        parm0 = mdls.GetInternalFromHumanReadableParm(corr.fit_model.id,
                                                      self.parameter_range[:, 0])[1]
        parm1 = mdls.GetInternalFromHumanReadableParm(corr.fit_model.id,
                                                      self.parameter_range[:, 1])[1]
        corr.fit_parameters_range = np.dstack((parm0, parm1))[0]

        if self.parent.MenuAutocloseTools.IsChecked():
            # Autoclose
            self.OnClose()
