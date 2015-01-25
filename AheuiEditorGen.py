# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Oct  8 2012)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc
import wx.grid

###########################################################################
## Class Editor
###########################################################################

class Editor ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Aheui Editor", pos = wx.DefaultPosition, size = wx.Size( 757,342 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		bSizer2 = wx.BoxSizer( wx.HORIZONTAL )
		
		self.left_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( -1,-1 ), wx.TAB_TRAVERSAL )
		fgSizer1 = wx.FlexGridSizer( 0, 1, 0, 0 )
		fgSizer1.SetFlexibleDirection( wx.BOTH )
		fgSizer1.SetNonFlexibleGrowMode( wx.FLEX_GROWMODE_SPECIFIED )
		
		CodeDirectionChoices = [ u" " ]
		self.CodeDirection = wx.Choice( self.left_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, CodeDirectionChoices, 0 )
		self.CodeDirection.SetSelection( 0 )
		self.CodeDirection.SetFont( wx.Font( 13, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer1.Add( self.CodeDirection, 0, wx.ALL|wx.EXPAND, 5 )
		
		CodeCommandChoices = [ u" " ]
		self.CodeCommand = wx.Choice( self.left_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, CodeCommandChoices, 0 )
		self.CodeCommand.SetSelection( 0 )
		self.CodeCommand.SetFont( wx.Font( 13, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer1.Add( self.CodeCommand, 0, wx.ALL|wx.EXPAND, 5 )
		
		CodeNumberChoices = [ u" " ]
		self.CodeNumber = wx.Choice( self.left_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, CodeNumberChoices, 0 )
		self.CodeNumber.SetSelection( 0 )
		self.CodeNumber.SetFont( wx.Font( 13, 70, 90, 90, False, wx.EmptyString ) )
		
		fgSizer1.Add( self.CodeNumber, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.GridWidth = wx.SpinCtrl( self.left_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 15 )
		fgSizer1.Add( self.GridWidth, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.GridHeight = wx.SpinCtrl( self.left_panel, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.SP_ARROW_KEYS, 1, 1000, 15 )
		fgSizer1.Add( self.GridHeight, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.LoadFile = wx.Button( self.left_panel, wx.ID_ANY, u"Load", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.LoadFile, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.SaveFile = wx.Button( self.left_panel, wx.ID_ANY, u"Save", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.SaveFile, 0, wx.ALL|wx.EXPAND, 5 )
		
		self.Execute = wx.Button( self.left_panel, wx.ID_ANY, u"Execute", wx.DefaultPosition, wx.DefaultSize, 0 )
		fgSizer1.Add( self.Execute, 0, wx.ALL|wx.EXPAND, 5 )
		
		
		self.left_panel.SetSizer( fgSizer1 )
		self.left_panel.Layout()
		fgSizer1.Fit( self.left_panel )
		bSizer2.Add( self.left_panel, 0, wx.EXPAND, 0 )
		
		self.right_panel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
		bSizer1 = wx.BoxSizer( wx.VERTICAL )
		
		self.CodeGrid = wx.grid.Grid( self.right_panel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, 0 )
		
		# Grid
		self.CodeGrid.CreateGrid( 15, 15 )
		self.CodeGrid.EnableEditing( False )
		self.CodeGrid.EnableGridLines( True )
		self.CodeGrid.EnableDragGridSize( False )
		self.CodeGrid.SetMargins( 0, 0 )
		
		# Columns
		self.CodeGrid.EnableDragColMove( False )
		self.CodeGrid.EnableDragColSize( True )
		self.CodeGrid.SetColLabelSize( 0 )
		self.CodeGrid.SetColLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Rows
		self.CodeGrid.EnableDragRowSize( True )
		self.CodeGrid.SetRowLabelSize( 0 )
		self.CodeGrid.SetRowLabelAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		
		# Label Appearance
		
		# Cell Defaults
		self.CodeGrid.SetDefaultCellFont( wx.Font( 13, 70, 90, 90, False, wx.EmptyString ) )
		self.CodeGrid.SetDefaultCellAlignment( wx.ALIGN_CENTRE, wx.ALIGN_CENTRE )
		bSizer1.Add( self.CodeGrid, 1, wx.EXPAND|wx.ALL, 5 )
		
		
		self.right_panel.SetSizer( bSizer1 )
		self.right_panel.Layout()
		bSizer1.Fit( self.right_panel )
		bSizer2.Add( self.right_panel, 1, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.CodeDirection.Bind( wx.EVT_CHOICE, self.CodeDirectionOnChoice )
		self.CodeCommand.Bind( wx.EVT_CHOICE, self.CodeCommandOnChoice )
		self.CodeNumber.Bind( wx.EVT_CHOICE, self.CodeNumberOnChoice )
		self.GridWidth.Bind( wx.EVT_SPINCTRL, self.GridWidthOnSpinCtrl )
		self.GridWidth.Bind( wx.EVT_TEXT, self.GridWidthOnSpinCtrlText )
		self.GridHeight.Bind( wx.EVT_SPINCTRL, self.GridHeightOnSpinCtrl )
		self.GridHeight.Bind( wx.EVT_TEXT, self.GridHeightOnSpinCtrlText )
		self.LoadFile.Bind( wx.EVT_BUTTON, self.LoadFileOnButtonClick )
		self.SaveFile.Bind( wx.EVT_BUTTON, self.SaveFileOnButtonClick )
		self.Execute.Bind( wx.EVT_BUTTON, self.ExecuteOnButtonClick )
		self.CodeGrid.Bind( wx.grid.EVT_GRID_SELECT_CELL, self.CodeGridOnGridSelectCell )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def CodeDirectionOnChoice( self, event ):
		event.Skip()
	
	def CodeCommandOnChoice( self, event ):
		event.Skip()
	
	def CodeNumberOnChoice( self, event ):
		event.Skip()
	
	def GridWidthOnSpinCtrl( self, event ):
		event.Skip()
	
	def GridWidthOnSpinCtrlText( self, event ):
		event.Skip()
	
	def GridHeightOnSpinCtrl( self, event ):
		event.Skip()
	
	def GridHeightOnSpinCtrlText( self, event ):
		event.Skip()
	
	def LoadFileOnButtonClick( self, event ):
		event.Skip()
	
	def SaveFileOnButtonClick( self, event ):
		event.Skip()
	
	def ExecuteOnButtonClick( self, event ):
		event.Skip()
	
	def CodeGridOnGridSelectCell( self, event ):
		event.Skip()
	

