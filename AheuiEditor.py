#!/usr/bin/env python2
# -*- coding: utf-8 -*-
#
# Copyright (C) 2013 Thomas Kühnel <kuehnelth@gmail.com>
#
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#                     Version 2, December 2004
#
# Everyone is permitted to copy and distribute verbatim or modified
# copies of this license document, and changing it is allowed as long
# as the name is changed.
#
#             DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE
#    TERMS AND CONDITIONS FOR COPYING, DISTRIBUTION AND MODIFICATION
#
# 0. You just DO WHAT THE FUCK YOU WANT TO.

import os
import wx
import AheuiEditorGen
import unicodedata
import codecs
#import EsotopeAheui
import ajit

wildcard = "Aheui Code (*.aheui)|*.aheui|" \
           "All files (*.*)|*.*"

# Implementing Editor
class AheuiEditor(AheuiEditorGen.Editor):
    def __init__(self, parent):
        AheuiEditorGen.Editor.__init__(self, parent)
        self.CodeDirectionChoices = [ u" ", u"ᅡ", u"ᅥ", u"ᅩ", u"ᅮ ", u"ᅣ", u"ᅧ", u"ᅭ", u"ᅲ ", u"ᅳ", u"ᅵ", u"ᅴ" ]
        self.CodeCommandChoices = [ u" ", u"ᄋ null", u"ᄒ terminate", u"ᄃ add", u"ᄄ multiply", u"ᄂ divide", u"ᄐ substract", u"ᄅ modulo", u"ᄆ pop", u"ᄇ push", u"ᄈ duplicate", u"ᄑ swap", u"ᄉ select", u"ᄊ transfer", u"ᄌ compare", u"ᄎ decide" ]
        self.CodeNumberChoices = [ u" ", u"ᆨ 2", u"ᆫ 2", u"ᆮ 3", u"ᆯ 5", u"ᆷ 4", u"ᆸ 4", u"ᆺ 2", u"ᆽ 3", u"ᆾ 4", u"ᆿ 3", u"ᇀ 4", u"ᇁ 4", u"ᆩ 4", u"ᆪ 4", u"ᆬ 5", u"ᆭ 5", u"ᆰ 7", u"ᆱ 9", u"ᆲ 9", u"ᆳ 7", u"ᆴ 9", u"ᆵ 9", u"ᆶ 8", u"ᆹ 6", u"ᆻ 4", u"ᆼ int", u"ᇂ uchar" ]

        for el in self.CodeDirectionChoices:
            self.CodeDirection.Append(el)
        for el in self.CodeCommandChoices:
            self.CodeCommand.Append(el)
        for el in self.CodeNumberChoices:
            self.CodeNumber.Append(el)


        self.CodeGrid.SetDefaultColSize(25, resizeExistingCols = True)
        self.CodeGrid.SetDefaultRowSize(25, resizeExistingRows = True)
        self.CodeGrid.Bind(wx.grid.EVT_GRID_RANGE_SELECT, self.OnCodeGridSelectRange)
        self.CodeGridSelection = None

        self.selectionX = 0
        self.selectionY = 0

        self.clipboard = [[]]

        shortcuts = [[wx.NewId(), self.onCtrlC, wx.ACCEL_CTRL,  ord('C')],
                     [wx.NewId(), self.onCtrlV, wx.ACCEL_CTRL,  ord('V')],
                     [wx.NewId(), self.onCtrlX, wx.ACCEL_CTRL,  ord('X')]]

        for s in shortcuts:
            self.Bind(wx.EVT_MENU, s[1], id=s[0])
        accel_tbl = wx.AcceleratorTable([(s[2], s[3], s[0]) for s in shortcuts])
        self.SetAcceleratorTable(accel_tbl)

        return

    def onCtrlC(self, event):
        self.onCtrlX(event, False)
        return

    def onCtrlV(self, event):
        #TODO: Check if Grid is large enough to paste data
        if not self.CodeGridSelection:
            self.SetGridSelectionCursor()
        cy = self.CodeGrid.GetGridCursorCol()
        cx = self.CodeGrid.GetGridCursorRow()
        for y in range(cy, cy + len(self.clipboard)):
            for x in range(cx, cx + len(self.clipboard[0])):
                self.CodeGrid.SetCellValue(x, y, self.clipboard[y - cy][x - cx])
        return

    def onCtrlX(self, event, cut=True):
        clipboard = []
        if not self.CodeGridSelection:
            self.SetGridSelectionCursor()
        for y in range(self.CodeGridSelection[0][1], self.CodeGridSelection[1][1] + 1):
            row = []
            for x in range(self.CodeGridSelection[0][0], self.CodeGridSelection[1][0] + 1):
                row.append(self.CodeGrid.GetCellValue(x, y))
                if cut:
                    self.CodeGrid.SetCellValue(x, y, "")
            clipboard.append(row)
        self.clipboard = clipboard
        return

    def SetGridSelectionCursor(self):
        self.CodeGridSelection = ((self.CodeGrid.GetGridCursorRow(), self.CodeGrid.GetGridCursorCol()),
                                      (self.CodeGrid.GetGridCursorRow(), self.CodeGrid.GetGridCursorCol()))
        return

    def OnCodeGridSelectRange(self, event):
        if event.Selecting():
            self.CodeGridSelection = (event.GetTopLeftCoords(), event.GetBottomRightCoords())
        else:
            self.CodeGridSelection = None

    def jamo2syl(self, s):
        return unicodedata.normalize("NFC", s)

    def syl2jamo(self, s):
        return unicodedata.normalize("NFD", s)

    def setchar(self):
        line = self.CodeCommand.GetStringSelection()[0] + self.CodeDirection.GetStringSelection()[0] + self.CodeNumber.GetStringSelection()[0]
        self.CodeGrid.SetCellValue(self.selectionX, self.selectionY, self.jamo2syl(line).strip())
        return

    def importGrid(self, s):
        s = [l.rstrip() for l in s]
        self.GridHeight.SetValue(len(s))
        self.GridHeightOnSpinCtrl(None)
        self.GridWidth.SetValue(len(max(s, key = len)))
        self.GridWidthOnSpinCtrl(None)
        for x, line in enumerate(s):
            for y, c in enumerate(line):
                self.CodeGrid.SetCellValue(x, y, c)
        return

    def exportGrid(self):
        s = ""
        for x in range(0, self.CodeGrid.GetNumberRows()):
            l = ""
            for y in range(0, self.CodeGrid.GetNumberCols()):
                l += self.CodeGrid.GetCellValue(x,y) or " "
            s += l.rstrip() + "\n"
        return s

    # Handlers for Editor events.
    def CodeDirectionOnChoice(self, event):
        self.setchar()

    def CodeCommandOnChoice(self, event):
        self.setchar()

    def CodeNumberOnChoice(self, event):
        self.setchar()

    def GridWidthOnSpinCtrl(self, event):
        # TODO: Implement code_widthOnSpinCtrl
        pass

    def GridWidthOnSpinCtrlText(self, event):
        cols = self.CodeGrid.GetNumberCols()
        newcols = self.GridWidth.GetValue()
        if newcols > cols:
            self.CodeGrid.InsertCols(cols, newcols - cols)
        elif newcols < cols:
            self.CodeGrid.DeleteCols(newcols, cols - newcols)

    def GridHeightOnSpinCtrl(self, event):
        rows = self.CodeGrid.GetNumberRows()
        newrows = self.GridHeight.GetValue()
        if newrows > rows:
            self.CodeGrid.InsertRows(rows, newrows - rows)
        elif newrows < rows:
            self.CodeGrid.DeleteRows(newrows, rows - newrows)

    def GridHeightOnSpinCtrlText(self, event):
        # TODO: Implement code_heightOnSpinCtrlText
        pass

    def LoadFileOnButtonClick(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.OPEN | wx.CHANGE_DIR | wx.FD_FILE_MUST_EXIST
            )

        if dlg.ShowModal() == wx.ID_OK:
            f = codecs.open(dlg.GetPath(), encoding="utf-8")
            s = f.readlines()
            f.close()
            self.importGrid(s)
        pass

    def SaveFileOnButtonClick(self, event):
        dlg = wx.FileDialog(
            self, message="Choose a file",
            defaultDir=os.getcwd(),
            defaultFile="",
            wildcard=wildcard,
            style=wx.SAVE | wx.CHANGE_DIR
            )

        if dlg.ShowModal() == wx.ID_OK:
            f = codecs.open(dlg.GetPath(), encoding="utf-8", mode="w")
            data = self.exportGrid()
            f.write(data)
            f.close()

        pass

    def ExecuteOnButtonClick(self, event):
        code = self.exportGrid()
        machine = ajit.Machine(ajit.parse(code))
        machine.number_input = ajit.aheui_number_input
        machine.character_input = ajit.aheui_character_input
        machine.output = ajit.aheui_output
        try:
            machine.run()
        except ajit.AheuiExit as e:
            if e.code != 0:
                print "Error %d" % e.code
        event.Skip()

    def CodeGridOnGridSelectCell(self, event):
        self.selectionX = event.GetRow()
        self.selectionY = event.GetCol()
        jamo = self.syl2jamo(self.CodeGrid.GetCellValue(self.selectionX, self.selectionY)) + "   "
        for c in self.CodeCommandChoices:
            if jamo[0] == c[0]:
                self.CodeCommand.SetStringSelection(c)
        for c in self.CodeDirectionChoices:
            if jamo[1] == c[0]:
                self.CodeDirection.SetStringSelection(c)
        for c in self.CodeNumberChoices:
            if jamo[2] == c[0]:
                self.CodeNumber.SetStringSelection(c)
        event.Skip()
        pass


if __name__ == "__main__":
    app = wx.App()
    frame = AheuiEditor(None)
    frame.Show(True)
    app.MainLoop()
