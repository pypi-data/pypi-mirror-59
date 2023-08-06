# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.stc as stc
from CLogText import LogText
###########################################################################
## Class Panel_Code
###########################################################################

class Panel_Declare_HW(wx.Panel):

    def __init__(self, parent,hanndel):
        wx.Panel.__init__(self, parent, id=wx.ID_ANY, pos=wx.DefaultPosition, size=wx.Size(600, 800),
                          style=wx.TAB_TRAVERSAL)

        self.parent = hanndel
        bz = wx.BoxSizer(wx.VERTICAL)



        self.list = CustListCtrl(self, wx.ID_ANY,
                                 style=wx.LC_REPORT
                                       | wx.BORDER_NONE
                                       # | wx.LC_SORT_ASCENDING            # Content of list as instructions is
                                       | wx.LC_HRULES | wx.LC_VRULES  # nonsense with auto-sort enabled
                                 )

        toolbar1 = self.BuildMenu(bz,self.list)

        bz.Add(toolbar1, 0, wx.EXPAND, 5)



        bz.Add(self.list, 1, wx.ALL | wx.EXPAND, 0)
        self.list.Populate1()




        self.listAlias = CustListCtrl(self, wx.ID_ANY,
                                 style=wx.LC_REPORT
                                       | wx.BORDER_NONE
                                       # | wx.LC_SORT_ASCENDING            # Content of list as instructions is
                                       | wx.LC_HRULES | wx.LC_VRULES  # nonsense with auto-sort enabled
                                 )

        toolbar2 = self.BuildMenu(bz, self.listAlias)

        bz.Add(toolbar2, 0, wx.EXPAND, 5)

        bz.Add(self.listAlias, 1, wx.ALL | wx.EXPAND, 0)
        self.listAlias.Populate2()

        self.SetSizer(bz)
        self.Layout()


        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnItemSelected, self.list)
    def __del__(self):
        pass



    def BuildMenu(self,bz,list):

        def OnAdd(event):
            index = list.InsertItem(list.GetItemCount(), '')

            list.SetItemData(index, index)
            event.Skip()

        def OnDelete(event):
            print self.currentItem
            list.DeleteItem(self.currentItem)
            event.Skip()

        def OnUp(event):
            event.Skip()

        def OnDn(event):
            event.Skip()





        _toolBar = wx.ToolBar(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TB_HORIZONTAL)
        _tool_save = _toolBar.AddTool(wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, ),
                                                  wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString,
                                                  None)
        _tool_refresh = _toolBar.AddTool(wx.ID_ANY, u"tool",
                                                     wx.ArtProvider.GetBitmap(wx.ART_GO_TO_PARENT, ),
                                                     wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString,
                                                     None)

        _toolBar.AddSeparator()

        _tool_add = _toolBar.AddTool(wx.ID_ANY, u"tool",
                                                 wx.ArtProvider.GetBitmap(wx.ART_ADD_BOOKMARK, ), wx.NullBitmap,
                                                 wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        _tool_delete = _toolBar.AddTool(wx.ID_ANY, u"tool",
                                                    wx.ArtProvider.GetBitmap(wx.ART_DEL_BOOKMARK, ), wx.NullBitmap,
                                                    wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        _toolBar.AddSeparator()

        _tool_up = _toolBar.AddTool(wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap(wx.ART_GO_UP, ),
                                                wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString,
                                                None)

        _tool_dn = _toolBar.AddTool(wx.ID_ANY, u"tool", wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, ),
                                                wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString,
                                                None)
        _toolBar.Realize()


        # Connect Events
        self.Bind(wx.EVT_TOOL, self.OnSave, id=_tool_save.GetId())
        self.Bind(wx.EVT_TOOL, OnAdd, id=_tool_add.GetId())
        self.Bind(wx.EVT_TOOL, OnDelete, id=_tool_delete.GetId())
        self.Bind(wx.EVT_TOOL, OnUp, id=_tool_up.GetId())
        self.Bind(wx.EVT_TOOL, OnDn, id=_tool_dn.GetId())

        return _toolBar


    # Virtual event handlers, overide them in your derived class
    def OnSave(self, event):
        self.parent.SavePage(self.savedata())
        event.Skip()



    def OnItemSelected(self, event):
        ##print(event.GetItem().GetTextColour())
        self.currentItem = event.Index
        print self.currentItem
        event.Skip()


    def savedata(self):
        dc = {}

        data = []
        _lenth = self.list.GetItemCount()
        _cols = self.list.GetColumnCount()
        for i in xrange(_lenth):
            lt = []
            for j in xrange(_cols):
                v = self.list.GetItem(i,j).GetText()
                lt.append(v)
            data.append(lt)


        dc['Slot'] = data

        data = []
        _lenth = self.listAlias.GetItemCount()
        _cols = self.listAlias.GetColumnCount()
        for i in xrange(_lenth):
            lt = []
            for j in xrange(_cols):
                v = self.listAlias.GetItem(i, j).GetText()
                lt.append(v)
            data.append(lt)
        dc['Alias'] = data
        return dc
        pass

    def renderdata(self,data):



        if type(data) == type([]):
            for i in xrange(len(data)):
                index = self.list.InsertItem(self.list.GetItemCount(), data[i][0])
                for j in range(1, min(self.list.GetColumnCount(), len(data[i]))):
                    self.list.SetItem(index, j, data[i][j])

            return 0

        if data.has_key('Slot'):
            for i in xrange(len(data['Slot'])):
                index = self.list.InsertItem(self.list.GetItemCount(), data['Slot'][i][0])
                for j in range(1, min(self.list.GetColumnCount(), len(data['Slot'][i]))):
                    self.list.SetItem(index, j, data['Slot'][i][j])

        if data.has_key('Alias'):
            for i in xrange(len(data['Alias'])):
                index = self.listAlias.InsertItem(self.listAlias.GetItemCount(), data['Alias'][i][0])
                for j in range(1, min(self.listAlias.GetColumnCount(), len(data['Alias'][i]))):
                    self.listAlias.SetItem(index, j, data['Alias'][i][j])


        pass

#----------------------------------------------------------------------


import sys
import wx
import wx.lib.mixins.listctrl as listmix



class CustListCtrl(wx.ListCtrl,
                   listmix.ListCtrlAutoWidthMixin,
                   listmix.TextEditMixin):

    def __init__(self, parent, ID, pos=wx.DefaultPosition,
                 size=wx.DefaultSize, style=0):
        wx.ListCtrl.__init__(self, parent, ID, pos, size, style)

        listmix.ListCtrlAutoWidthMixin.__init__(self)

        listmix.TextEditMixin.__init__(self)





    def Populate1(self):
        # for normal, simple columns, you can add them like this:

        self.InsertColumn(0, "HW Type")
        self.InsertColumn(1, "comment")

        self.currentItem = 0


    def Populate2(self):
        # for normal, simple columns, you can add them like this:

        self.InsertColumn(0, "Channel")
        self.InsertColumn(1, "Alias")
        self.InsertColumn(2, "commnt")

        self.currentItem = 0
    # def SetStringItem(self, index, col, data):
    #     if col in range(3):
    #         wx.ListCtrl.SetItem(self, index, col, data)
    #         wx.ListCtrl.SetItem(self, index, 3+col, str(len(data)))
    #     else:
    #         try:
    #             datalen = int(data)
    #         except:
    #             return
    #
    #         wx.ListCtrl.SetItem(self, index, col, data)
    #
    #         data = self.GetItem(index, col-3).GetText()
    #         wx.ListCtrl.SetItem(self, index, col-3, data[0:datalen])
