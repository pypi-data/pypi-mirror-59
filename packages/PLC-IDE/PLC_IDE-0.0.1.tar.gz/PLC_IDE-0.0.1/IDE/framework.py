# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.aui
import os
from PLC_IDE.lib.JsonClass import CJSON
from CProjectTree import Panel_Tree
from CNotebook import Panel_Notebook
from PLC_IDE.lib.CommonDialog import InputBox,MessageBox,OpenFileDialog
import CLogText
from CLogText import LogText

from PLC_IDE.IDE.Parse import Build,Clear,BuildProjectInfo
###########################################################################
## Class IDE_DEMO
###########################################################################

class IDE_DEMO(wx.Frame):

    def __init__(self, parent):
        wx.Frame.__init__(self, parent, id=wx.ID_ANY, title=u"Code IDE", pos=wx.DefaultPosition, size=wx.Size(1024, 768),
                          style=wx.DEFAULT_FRAME_STYLE | wx.TAB_TRAVERSAL)

        # self.SetSizeHintsSz(wx.DefaultSize, wx.DefaultSize)




        #


        self.curFile = None
        self.curData = None

        self.build_menubar()
        self.build_toolbar()

        bzAll = wx.BoxSizer(wx.VERTICAL)


        self.m_splitter = wx.SplitterWindow(self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize,
                                            wx.SP_3D | wx.SP_NO_XP_THEME)
        self.m_splitter.Bind(wx.EVT_IDLE, self.m_splitter1OnIdle)



        self.m_panel_left = Panel_Tree(self.m_splitter,self)
        self.m_panel_right = Panel_Notebook(self.m_splitter,self)


        self.m_splitter.SplitVertically(self.m_panel_left, self.m_panel_right, 254)
        bzAll.Add(self.m_splitter, 5, wx.EXPAND, 0)


        CLogText.create_log(self)


        bzAll.Add(CLogText.logtext,1,wx.EXPAND,0)

        self.SetSizer(bzAll)
        self.Layout()
        # self.m_statusBar1 = self.CreateStatusBar(1, wx.ST_SIZEGRIP, wx.ID_ANY)

        self.Centre(wx.BOTH)

        # parse test code
        # __path = 'D:\\Work\\Code\\Python\\PLC_IDE\\Projects\\test1.ryj'
        # self.OpenProject(__path)
        # self.RenderProject(self.curData)
        # Build(self.curData, __path)

    def __del__(self):
        pass


    def build_menubar(self):

        def additem(menu,txt):
            _menuitem = wx.MenuItem(menu, wx.ID_ANY, txt, wx.EmptyString, wx.ITEM_NORMAL)
            menu.Append(_menuitem)
            return _menuitem



        m_menubar = wx.MenuBar(0)

        _menuitems = []
        # ----------------------------------------------------------------------
        _menu_File = wx.Menu()

        _menuitems.append(additem(_menu_File,u"New Project"))
        _menuitems.append(additem(_menu_File,u"Open..."))
        _menuitems.append(additem(_menu_File,u"Save"))
        _menuitems.append(additem(_menu_File,u"Save As..."))
        _menuitems.append(additem(_menu_File,u"Close Project"))
        _menu_File.AppendSeparator()
        _menuitems.append(additem(_menu_File,u"Open Project Folder"))
        _menu_File.AppendSeparator()
        _menuitems.append(additem(_menu_File, u"Exit"))
        m_menubar.Append(_menu_File, u"File")
        # ----------------------------------------------------------------------
        _menu_Edit = wx.Menu()
        _menuitems.append(additem(_menu_Edit, u"Find"))
        _menuitems.append(additem(_menu_Edit, u"Replace"))
        _menuitems.append(additem(_menu_Edit, u"Refactor"))
        m_menubar.Append(_menu_Edit, u"Edit")
        # ----------------------------------------------------------------------
        _menu_View = wx.Menu()
        m_menubar.Append(_menu_View, u"View")
        # ----------------------------------------------------------------------
        _menu_Debug = wx.Menu()
        m_menubar.Append(_menu_Debug, u"Debug")
        # ----------------------------------------------------------------------
        _menu_Build = wx.Menu()
        _menuitems.append(additem(_menu_Build, u"Build"))
        _menuitems.append(additem(_menu_Build, u"Rebuild"))
        _menuitems.append(additem(_menu_Build, u"Clear"))
        m_menubar.Append(_menu_Build, u"Build")
        # ----------------------------------------------------------------------

        _menu_Tools = wx.Menu()
        _menuitems.append(additem(_menu_Tools, u"Build Info"))
        _menuitems.append(additem(_menu_Tools, u"Open Info"))
        m_menubar.Append(_menu_Tools, u"Tools")
        # ----------------------------------------------------------------------
        _menu_Help = wx.Menu()
        m_menubar.Append(_menu_Help, u"Help")
        # ----------------------------------------------------------------------
        self.SetMenuBar(m_menubar)

        self.Bind(wx.EVT_MENU, self.OnNewProject, id=_menuitems[0].GetId())
        self.Bind(wx.EVT_MENU, self.OnOpenProject, id=_menuitems[1].GetId())
        self.Bind(wx.EVT_MENU, self.OnSaveProject, id=_menuitems[2].GetId())
        self.Bind(wx.EVT_MENU, self.OnSaveProject, id=_menuitems[3].GetId())
        self.Bind(wx.EVT_MENU, self.OnCloseProject, id=_menuitems[4].GetId())
        self.Bind(wx.EVT_MENU, self.OnOpenFolderProject, id=_menuitems[5].GetId())
        self.Bind(wx.EVT_MENU, self.OnExit, id=_menuitems[6].GetId())

        self.Bind(wx.EVT_MENU, self.OnBuildProject, id=_menuitems[10].GetId())
        self.Bind(wx.EVT_MENU, self.OnReBuildProject, id=_menuitems[11].GetId())
        self.Bind(wx.EVT_MENU, self.OnClearProject, id=_menuitems[12].GetId())

        self.Bind(wx.EVT_MENU, self.OnBuildProjectInfo, id=_menuitems[13].GetId())
        self.Bind(wx.EVT_MENU, self.OnOpenProjectInfo, id=_menuitems[14].GetId())

        pass

    def build_toolbar(self):

        _toolbar = self.CreateToolBar(wx.TB_HORIZONTAL, wx.ID_ANY)
        _tool_new = _toolbar.AddTool(wx.ID_ANY, u"New", wx.ArtProvider.GetBitmap(wx.ART_NEW, ),
                                               wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        _tool_open = _toolbar.AddTool(wx.ID_ANY, u"Open", wx.ArtProvider.GetBitmap(wx.ART_FILE_OPEN, ),
                                     wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        _tool_save = _toolbar.AddTool(wx.ID_ANY, u"Save", wx.ArtProvider.GetBitmap(wx.ART_FILE_SAVE, ),
                                      wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        # ----------------------------------------------------------------------
        _toolbar.AddSeparator()
        # ----------------------------------------------------------------------

        _tool_undo = _toolbar.AddTool(wx.ID_ANY, u"Undo", wx.ArtProvider.GetBitmap(wx.ART_UNDO, ),
                                     wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        _tool_redo = _toolbar.AddTool(wx.ID_ANY, u"Redo", wx.ArtProvider.GetBitmap(wx.ART_REDO, ),
                                      wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        # ----------------------------------------------------------------------
        _toolbar.AddSeparator()
        # ----------------------------------------------------------------------
        _tool_start = _toolbar.AddTool(wx.ID_ANY, u"Start", wx.ArtProvider.GetBitmap(wx.ART_GO_FORWARD, ),
                                      wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        _tool_stop = _toolbar.AddTool(wx.ID_ANY, u"Stop", wx.ArtProvider.GetBitmap(wx.ART_CLOSE, ),
                                       wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)

        _tool_download = _toolbar.AddTool(wx.ID_ANY, u"Download", wx.ArtProvider.GetBitmap(wx.ART_GO_DOWN, ),
                                      wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None)



        _toolbar.Realize()
        pass


    def m_splitter1OnIdle(self, event):
        self.m_splitter.SetSashPosition(254)
        self.m_splitter.Unbind(wx.EVT_IDLE)

    def RenderProject(self,dc):
        self.m_panel_left.DeleteAll()
        self.m_panel_left.Render(dc['File'])
        pass

    def GetNewProject(self):
        def init_project_info():
            d = {
                'version':2000001
            }
            return d

        def init_file_struct():
            d = {
                "struct":{},
                "enum" :{},
                "gvl":{
                    "GVL":[]
                },
                "function" :{},
                "class":{},
                "program":{

                },
                "task":{
                },
                "motion":{
                    "axis":{}
                },
                "hardware":{
                    "0":{
                        'Slot':{},
                        'Alias':{}
                    }
                }
            }
            return d

        dc = {}

        dc['Info'] = init_project_info()
        dc['File'] = init_file_struct()
        return dc

    #event hanndle
    def OnNewProject(self,event):
        dc = self.GetNewProject()

        self.curData = dc
        self.Check_Project_Complete()
        self.RenderProject(self.curData)
        event.Skip()

    def OnOpenProject(self,event):

        _paths = OpenFileDialog(self,[['ryj文件','ryj'],['All File','*']])
        self.OpenProject(_paths)
        self.RenderProject(self.curData)
        event.Skip()


    def OnSaveProject(self,event):
        path = self.curFile
        _exists = 0

        if self.curFile == None:
            import os
            wildcard = "Project File (*.ryj)|*.ryj|" \
                       "All files (*.*)|*.*"

            dlg = wx.FileDialog(
                self, message="Save file as ...", defaultDir=os.getcwd(),
                defaultFile="", wildcard=wildcard, style=wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
            )

            dlg.SetFilterIndex(2)

            if dlg.ShowModal() == wx.ID_OK:
                path = dlg.GetPath()
                if os.path.exists(path):
                    _exists = 1



            dlg.Destroy()
            pass

        if self.curData == None:
            self.curData = self.GetNewProject()
            pass

        from lib.CommonDialog import MessageBox
        if _exists == 1:
            val = MessageBox(self,u'File Exists！',u'Error',wx.YES_NO|wx.ICON_ERROR)
            if val == wx.NO:
                return

        if path == "":
            return

        LogText('save file:' + path)

        objJSON = CJSON()
        objJSON.writefile(self.curData,path)
        event.Skip()

    def OnCloseProject(self,event):
        self.m_panel_left.DeleteAll()
        self.m_panel_right.CloseAll()
        self.curFile = ''
        self.curData.clear()

        LogText('Close Project!!')
        event.Skip()

    def OnExit(self,event):
        wx.Exit()
        event.Skip()

    def OnOpenFolderProject(self,event):
        if self.curFile != '':
            filepath = self.curFile
            _dir = os.path.dirname(filepath)
            _file = os.path.basename(filepath)
            _hz = os.path.splitext(filepath)[1]

            _name = _file.replace(_hz, '')

            _folder = os.path.join(_dir, _name)

            os.system("explorer.exe %s" % _folder)
        event.Skip()


    def OnBuildProject(self,event):
        Build(self.curData,self.curFile)
        _res = MessageBox(None, u'打开帮助?', 'Tips', wx.YES_NO)
        print _res
        if _res == 5103:
            self.OpenHelpFile()
        event.Skip()
        pass

    def OnReBuildProject(self,event):
        Clear(self.curFile)
        Build(self.curData, self.curFile)
        event.Skip()
        pass

    def OnClearProject(self,event):
        Clear(self.curFile)

        event.Skip()
        pass

    def OnBuildProjectInfo(self,event):
        if self.curFile != '':
            BuildProjectInfo(self.curFile)
        event.Skip()

    def OnOpenProjectInfo(self,event):
        if self.curFile != '':
            self.OpenHelpFile()
        event.Skip()


    def openfilepage(self,d):
        k = d[0]
        f = d[1]
        m = ''
        if len(d) > 2:
            m = d[2]
        if len(d) == 2:
            self.m_panel_right.OpenPage(d,self.curData['File'][k][f])
        else:
            self.m_panel_right.OpenPage(d, self.curData['File'][k][f][m])
        pass

    def SavePage(self,l,data):
        k = l[0]
        f = l[1]

        if len(l) > 2:
            m = l[2]
            self.curData['File'][k][f][m] = data
        else:
            self.curData['File'][k][f] = data

    def TreeOnRightDown(self,d):
        _menu = wx.Menu()

        _menuitem1 = wx.MenuItem(_menu, wx.ID_ANY, u"Add", wx.EmptyString, wx.ITEM_NORMAL)
        _menu.Append(_menuitem1)

        _menuitem2 = wx.MenuItem(_menu, wx.ID_ANY, u"Rename", wx.EmptyString, wx.ITEM_NORMAL)
        _menu.Append(_menuitem2)

        _menuitem3 = wx.MenuItem(_menu, wx.ID_ANY, u"Del", wx.EmptyString, wx.ITEM_NORMAL)
        _menu.Append(_menuitem3)

        self.Bind(wx.EVT_MENU, self.AddFile, id=_menuitem1.GetId())
        self.Bind(wx.EVT_MENU, self.RenameFile, id=_menuitem2.GetId())
        self.Bind(wx.EVT_MENU, self.DelFile, id=_menuitem3.GetId())

        self.PopupMenu(_menu)
        pass



    def TreeClassOnRrightDown(self,d):

        def AddMeth(event):
            v = InputBox(self, 'input meth name', 'Input')
            if v == '' or v == 'init':
                event.Skip()
                return

            self.curData['File'][d[0]][d[1]][v] = {}

            self.m_panel_left.DeleteAll()
            self.m_panel_left.Render(self.curData['File'])
            event.Skip()

        def RenameMeth(event):
            v = InputBox(self, 'input new name', 'Input')
            if v == '':
                event.Skip()
                return

            self.curData['File'][d[0]][d[1]][d[2]] = self.curData['File'][d[0]][d[1]].pop(d[2])

            self.m_panel_left.DeleteAll()
            self.m_panel_left.Render(self.curData['File'])

            event.Skip()

        def DelMeth(event):
            self.curData['File'][d[0]][d[1]].pop(d[2])

            self.m_panel_left.DeleteAll()
            self.m_panel_left.Render(self.curData['File'])
            event.Skip()

        def DelClass(event):
            self.curData['File'][d[0]].pop(d[1])

            self.m_panel_left.DeleteAll()
            self.m_panel_left.Render(self.curData['File'])

            event.Skip()

        def RenameClass(event):
            v = InputBox(self, 'input new name', 'Input')
            if v == '':
                event.Skip()
                return

            self.curData['File'][d[0]][d[1]] = self.curData['File'][d[0]].pop(d[1])

            self.m_panel_left.DeleteAll()
            self.m_panel_left.Render(self.curData['File'])
            event.Skip()

        print 'tree'

        _menu = wx.Menu()

        if len(d) == 2:
            _menuitem1 = wx.MenuItem(_menu, wx.ID_ANY, u"Add Meth", wx.EmptyString, wx.ITEM_NORMAL)
            _menu.Append(_menuitem1)

            _menu.AppendSeparator()

            _menuitem2 = wx.MenuItem(_menu, wx.ID_ANY, u"Rename Class", wx.EmptyString, wx.ITEM_NORMAL)
            _menu.Append(_menuitem2)

            _menuitem3 = wx.MenuItem(_menu, wx.ID_ANY, u"Del Class", wx.EmptyString, wx.ITEM_NORMAL)
            _menu.Append(_menuitem3)

            self.Bind(wx.EVT_MENU, AddMeth, id=_menuitem1.GetId())
            self.Bind(wx.EVT_MENU, RenameClass, id=_menuitem2.GetId())
            self.Bind(wx.EVT_MENU, DelClass, id=_menuitem3.GetId())

        elif len(d) == 3:

            _menuitem1 = wx.MenuItem(_menu, wx.ID_ANY, u"Add Meth", wx.EmptyString, wx.ITEM_NORMAL)
            _menu.Append(_menuitem1)

            _menuitem2 = wx.MenuItem(_menu, wx.ID_ANY, u"Rename Meth", wx.EmptyString, wx.ITEM_NORMAL)
            _menu.Append(_menuitem2)

            _menuitem3 = wx.MenuItem(_menu, wx.ID_ANY, u"Del Meth", wx.EmptyString, wx.ITEM_NORMAL)
            _menu.Append(_menuitem3)

            if d[2] == 'init':
                _menuitem2.Enable(False)
                _menuitem3.Enable(False)

            self.Bind(wx.EVT_MENU, AddMeth, id=_menuitem1.GetId())
            self.Bind(wx.EVT_MENU, RenameMeth, id=_menuitem2.GetId())
            self.Bind(wx.EVT_MENU, DelMeth, id=_menuitem3.GetId())


        self.PopupMenu(_menu)


        pass



    def AddFile(self,event):
        v = InputBox(self,'input new name','Input')
        if v == '':
            event.Skip()
            return

        d = self.m_panel_left.SelectionItem
        if d == None:
            return

        if self.curData['File'][d[0]].has_key(v):
            return

        self.curData['File'][d[0]][v] = {}


        if d[0] == 'class':
            self.curData['File'][d[0]][v]['init'] = {}
            self.curData['File'][d[0]][v]['Declare'] = {}


        self.m_panel_left.DeleteAll()
        self.m_panel_left.Render(self.curData['File'])
        pass


    def RenameFile(self,event):
        v = InputBox(self, 'input new name', 'Input')
        if v == '':
            event.Skip()
            return
        d = self.m_panel_left.SelectionItem
        if d == None:
            return
        if len(d) == 2:
            self.curData['File'][d[0]][v] = self.curData['File'][d[0]].pop(d[1])
        self.m_panel_left.DeleteAll()
        self.m_panel_left.Render(self.curData['File'])
        pass

    def DelFile(self,event):
        d = self.m_panel_left.SelectionItem
        if d == None:
            return
        if len(d) == 2:
            self.curData['File'][d[0]].pop(d[1])

        self.m_panel_left.DeleteAll()
        self.m_panel_left.Render(self.curData['File'])
        pass



    def OpenProject(self,_paths):
        if type(_paths) == type([]):
            if len(_paths) > 0:
                objJSON = CJSON()
                self.curData = objJSON.loadfile(_paths[0])
                self.Check_Project_Complete()
                self.curFile = _paths[0]
                LogText('Open File:' + _paths[0])
        else:
            if os.path.exists(_paths):
                objJSON = CJSON()
                self.curData = objJSON.loadfile(_paths)
                self.Check_Project_Complete()
                self.curFile = _paths
                LogText('Open File:' + _paths)


    def Check_Project_Complete(self):
        lt = [
            'hardware',
            'motion',
            'struct',
            'enum',
            'function',
            'class',
            'program',
            'gvl',
            'task'
        ]

        for n in lt:
            if self.curData['File'].has_key(n):
                pass
            else:
                self.curData['File'][n] = {}
                if n == 'hardware':
                    self.curData['File'][n] = {'0':{}}
                elif n == 'gvl':
                    self.curData['File'][n] = {'GVL': {}}
                elif n == 'motion':
                    self.curData['File'][n] = {'axis': {}}

        pass


    def OpenHelpFile(self):
        filepath = self.curFile
        _dir = os.path.dirname(filepath)
        _file = os.path.basename(filepath)
        _hz = os.path.splitext(filepath)[1]

        _name = _file.replace(_hz, '')

        _path = os.path.join(_dir, _name, 'Helper', 'html', 'index.html')
        print _path
        import CHelpBuilder
        CHelpBuilder.OpenHtml(_path)