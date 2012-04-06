
import  keyword

import  wx
import  wx.stc  as  stc
import  wx.lib.newevent

import re

import yaml, os.path, sys

#----------------------------------------------------------------------

demoText = """\
# just a test

"""

#----------------------------------------------------------------------


if wx.Platform == '__WXMSW__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Courier',
              'helv' : 'Arial',
              'other': 'Helvetica',
              'size' : 12,
              'size2': 10,
             }
elif wx.Platform == '__WXMAC__':
    faces = { 'times': 'Times New Roman',
              'mono' : 'Monaco',
              'helv' : 'Arial',
              'other': 'Comic Sans MS',
              'size' : 12,
              'size2': 10,
             }
else:
    faces = { 'times': 'Times',
              'mono' : 'Courier New',
              'helv' : 'Helvetica',
              'other': 'new century schoolbook',
              'size' : 12,
              'size2': 10,
             }

#   for x in dir(api):
#       print type(getattr(api, x)), x


#----------------------------------------------------------------------
(EventTabpadOutput, EVT_TABPAD_STATUS) = wx.lib.newevent.NewEvent()
class FindDialog(wx.Dialog):
    def __init__ (self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(200, 150))

        self.parent = parent
        self.tabList = []
        
        #sizer = wx.GridSizer(2, 1, 5, 5)
    
        self.inp = wx.TextCtrl(self, -1, pos=(5, 5), size=(160, -1))
        btn = wx.Button(self, -1, 'Find', pos=(10, 30))
        self.Bind(wx.EVT_BUTTON, self.onFind, btn)

        #sizer.Add(self.inp)
        #sizer.Add(btn)

        #self.SetSizer(sizer)

        self.Centre()
        self.Show()
        

    def onFind(self, event):
        self.word = self.inp.GetValue()

        self.SearchFromHead(self.word)
        

        #if self.getSelectionLines() == False:
        #    wx.MessageBox('Nothing found', 'Result', 
        #            wx.OK | wx.ICON_INFORMATION)

        self.Destroy()

    def SearchFromHead(self, word):
        self.printStatus('Search Word: '+word)
        currentTabNum = self.parent.GetSelection()
        self.parent.SetSelection(self, word, select=True)
        currentSTC = self.tabList[self.parent.currentTabNum]
        currentSTC.GotoPos(0)
        currentSTC.SearchAnchor()
        currentSTC.SearchNext( wx.stc.STC_FIND_REGEXP, word)


    def printStatus(self, msg, append = False):
        evt = EventTabpadOutput(output=msg, append=append)
        wx.PostEvent(self.parent, evt)
        


class PythonSTC(stc.StyledTextCtrl):

    fold_symbols = 2
    
    indent = None
    complete = ""
    def __init__(self, parent, ID,
                 pos=wx.DefaultPosition, size=wx.DefaultSize,
                 style=0):
        stc.StyledTextCtrl.__init__(self, parent, ID, pos, size, style)

        self.CmdKeyAssign(ord('B'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMIN)
        self.CmdKeyAssign(ord('N'), stc.STC_SCMOD_CTRL, stc.STC_CMD_ZOOMOUT)

        self.SetLexer(stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))

        self.SetProperty("fold", "1")
        self.SetProperty("tab.timmy.whinge.level", "1")
        self.SetMargins(0,0)

        self.SetViewWhiteSpace(False)
        self.SetBufferedDraw(True)
        #self.SetViewEOL(True)
        #self.SetEOLMode(stc.STC_EOL_CRLF)
        self.SetUseAntiAliasing(True)
        
        self.SetEdgeMode(stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)

        # Setup a margin to hold fold markers
        self.SetFoldFlags(16)  ###  WHAT IS THIS VALUE?  WHAT ARE THE OTHER FLAGS?  DOES IT MATTER?
        self.SetMarginType(2, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)

        # Tabbing settings
        self.SetIndent(4)
        self.SetUseTabs(0)
        self.SetTabWidth(4)
        self.SetTabIndents(0)

        if self.fold_symbols == 0:
            # Arrow pointing right for contracted folders, arrow pointing down for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_ARROWDOWN, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_ARROW, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "black", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY,     "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY,     "white", "black")
            
        elif self.fold_symbols == 1:
            # Plus for contracted folders, minus for expanded
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_MINUS, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_PLUS,  "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_EMPTY, "white", "black")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_EMPTY, "white", "black")

        elif self.fold_symbols == 2:
            # Like a flattened tree control using circular headers and curved joins
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_CIRCLEMINUS,          "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_CIRCLEPLUS,           "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,                "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNERCURVE,         "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_CIRCLEPLUSCONNECTED,  "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_CIRCLEMINUSCONNECTED, "white", "#404040")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNERCURVE,         "white", "#404040")

        elif self.fold_symbols == 3:
            # Like a flattened tree control using square headers
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN,    stc.STC_MARK_BOXMINUS,          "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDER,        stc.STC_MARK_BOXPLUS,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB,     stc.STC_MARK_VLINE,             "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL,    stc.STC_MARK_LCORNER,           "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND,     stc.STC_MARK_BOXPLUSCONNECTED,  "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, "white", "#808080")
            self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER,           "white", "#808080")


        self.Bind(stc.EVT_STC_UPDATEUI, self.OnUpdateUI)
        self.Bind(stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.Bind(wx.EVT_KEY_DOWN, self.OnKeyPressed)
        self.Bind(wx.EVT_CHAR, self.OnChar)



        # Make some styles,  The lexer defines what each style is used for, we
        # just have to define what each style looks like.  This set is adapted from
        # Scintilla sample property files.

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,size:%(size)d" % faces)
        self.StyleClearAll()  # Reset all to be like the default

        # Global default styles for all languages
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT,     "face:%(helv)s,back:#ffffff,size:%(size)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER,  "back:#ffffff,fore:#111111,face:%(helv)s,size:%(size2)d" % faces)
        self.StyleSetSpec(stc.STC_STYLE_CONTROLCHAR, "fore:#000000,face:%(other)s" % faces)
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT,  "fore:#000000,back:#ffffff,bold,size:14")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD,    "fore:#000000,back:#ffffff")

        # Default 
        self.StyleSetSpec(stc.STC_P_DEFAULT, "fore:#000000,bold,face:%(helv)s,size:%(size)d,back:#ffffff" % faces)
        # Comments
        self.StyleSetSpec(stc.STC_P_COMMENTLINE, "fore:#000000,italic,face:%(other)s,size:%(size)d,back:#ffffff" % faces)
        # Number
        self.StyleSetSpec(stc.STC_P_NUMBER, "fore:#ff0000,size:%(size)d,back:#ffffff" % faces)
        # String
        self.StyleSetSpec(stc.STC_P_STRING, "fore:#800000,italic,face:%(helv)s,size:%(size)d,back:#ffffff" % faces)
        # Single quoted string
        self.StyleSetSpec(stc.STC_P_CHARACTER, "fore:#800000,italic,face:%(helv)s,size:%(size)d,back:#ffffff" % faces)
        # Keyword
        self.StyleSetSpec(stc.STC_P_WORD, "fore:#000000,bold,size:%(size)d,back:#ffffff" % faces)
        self.StyleSetSpec(stc.STC_P_WORD2, "fore:#0000ff,size:%(size)d,back:#ffffff" % faces)
        # Triple quotes
        self.StyleSetSpec(stc.STC_P_TRIPLE, "fore:#800000,size:%(size)d,back:#ffffff" % faces)
        # Triple double quotes
        self.StyleSetSpec(stc.STC_P_TRIPLEDOUBLE, "fore:#800000,size:%(size)d,back:#ffffff" % faces)
        # Class name definition
        self.StyleSetSpec(stc.STC_P_CLASSNAME, "fore:#000000,bold,underline,size:%(size)d,back:#ffffff" % faces)
        # Function or method name definition
        self.StyleSetSpec(stc.STC_P_DEFNAME, "fore:#000000,size:%(size)d,back:#ffffff" % faces)
        # Operators
        self.StyleSetSpec(stc.STC_P_OPERATOR, "fore:#000000,size:%(size)d,back:#ffffff" % faces)
        # Identifiers 
        self.StyleSetSpec(stc.STC_P_IDENTIFIER, "fore:#000000,face:%(helv)s,size:%(size)d,back:#ffffff" % faces)
        # Comment-blocks
        self.StyleSetSpec(stc.STC_P_COMMENTBLOCK, "fore:#aeaeae,size:%(size)d,back:#0D1021" % faces)
        # End of line where string is not closed
        self.StyleSetSpec(stc.STC_P_STRINGEOL, "fore:#000000,face:%(mono)s,back:#ffffff,eol,size:%(size)d" % faces)

        self.SetCaretForeground("black")
        self.SetSelForeground(True, "#000000")
        self.SetSelBackground(True, "#3399ff")
        
        self.SetMarginType(1, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(1, 25)   
        
        self.Fit()
        self.Refresh()
        
        self.SetBackSpaceUnIndents(True)
        self.AutoCompSetDropRestOfWord(True)
        self.AutoCompSetFillUps("\t")
        self.AutoCompSetCancelAtStart(True)

        root = os.path.dirname(sys.path[0] + os.sep) \
                        .replace("library.zip", "")

        self.api = yaml.load(open(root + os.sep + 'help.yml'))

        self.SetKeyWords(1, " ".join(self.api.keys()))

        self.constants = ['IN_1', 'IN_2', 'IN_3', 'IN_4', 'LCD_LINE1', 
                            'LCD_LINE2', 'LCD_LINE3', 'LCD_LINE4', 
                            'LCD_LINE5', 'LCD_LINE6', 'LCD_LINE7', 
                            'LCD_LINE8', 'OUT_A', 'OUT_AB', 'OUT_ABC', 
                            'OUT_AC', 'OUT_B', 'OUT_BC', 'OUT_C', 
                            'S1', 'S2', 'S3', 'S4', 
                            'SENSOR_LIGHT', 'SENSOR_TOUCH']



        self.last_id = None
        self.last_arg_pos = 0

    def OnChar(self, event):
        key = event.GetKeyCode()
        
        pos = self.GetCurrentPos()
        
        # Showing CallTip
        if key == ord('('):
            style = self.GetStyleAt(pos - 1)
            if style == stc.STC_P_WORD2 or style == stc.STC_P_IDENTIFIER:
                if style == stc.STC_P_WORD2:
                    id = self.getWORD2(pos - 1)
                elif style == stc.STC_P_IDENTIFIER:
                    id = self.getIdentifier(pos - 1)

                if id in self.api:
                    self.last_id = id
                    self.last_arg_pos = 1
                    self.CallTipSetForeground("#000000")
                    self.CallTipSetBackground("#FFFFFF")
                    self.CallTipShow(pos - len(id), self.api[id])
                    pos = self.getArgPos(self.last_id, self.last_arg_pos)
                    self.CallTipSetHighlight(pos[0], pos[1]-1)
                                 
        
        if key == ord(','):
            if self.last_id is not None:
                self.last_arg_pos += 1
                pos = self.getArgPos(self.last_id, self.last_arg_pos)
                self.CallTipSetHighlight(pos[0], pos[1]-1)
                
            
                                 
        # Hiding CallTip
        if key == ord(')'):
            self.CallTipCancel()
            self.last_id = None
            self.last_arg_pos = 0
        
        event.Skip()

    def OnKeyPressed(self, event):
        key = event.GetKeyCode()
        
        pos = self.GetCurrentPos()
        
        
        if key == wx.WXK_RETURN:
            
            # using enter for completion
            if self.AutoCompActive():
                self.AutoCompComplete()
                return

            c = self.GetCharAt(self.GetCurrentPos() - 1)
            self.indent = self.getIndent(self.GetCurLine()[0])
            if c == 58:
                self.AddText("\n" + self.GetIndent()*' ' + self.indent)
            else:
                self.AddText("\n" + self.indent)
            return

        if (key == 102 or key == 70) and event.ControlDown():
            FindDialog(self, id=wx.ID_ANY, title='Find...')

        if key == 32 and event.ControlDown():
            pos = self.GetCurrentPos()

            # Tips
            if event.ShiftDown():
                #self.CallTipSetBackground("#ffffff")
                self.CallTipSetForeground("#ffffff")
                self.CallTipShow(pos, 'lots of of text: blah, blah, blah\n\n'
                                 'show some suff, maybe parameters..\n\n'
                                 'fubar(param1, param2)')
            # Code completion
            else:
                #lst = []
                #for x in range(50000):
                #    lst.append('%05d' % x)
                #st = " ".join(lst)
                #print len(st)
                #self.AutoCompShow(0, st)
                
                id = self.getIdentifier()

                kw = keyword.kwlist[:] + self.api.keys()
                #kw.append("zzzzzz?2")
               #kw.append("aaaaa?2")
               #kw.append("__init__?3")
               #kw.append("zzaaaaa?2")
               #kw.append("zzbaaaa?2")
                kw.append("this_is_a_longer_value")
                kw.append("this_is_a_much_much_much_much_much_much_much_longer_value")

                kw.sort()  # Python sorts are case sensitive
                self.AutoCompSetIgnoreCase(False)  # so this needs to match

                self.AutoCompShow(len(id), " ".join(kw))
        else:
            event.Skip()


    def OnUpdateUI(self, evt):
        # check for matching braces
        braceAtCaret = -1
        braceOpposite = -1
        charBefore = None
        caretPos = self.GetCurrentPos()

        if caretPos > 0:
            charBefore = self.GetCharAt(caretPos - 1)
            styleBefore = self.GetStyleAt(caretPos - 1)
            
           #if styleBefore == stc.STC_P_IDENTIFIER:
           #    kw = keyword.kwlist[:]
           #    kw.sort()
           #    
           #    self.complete += chr(charBefore)
           #    if not self.AutoCompActive():
           #        self.AutoCompShow(0, " ".join(kw))
           #    else:
           #        self.AutoCompSelect(self.complete)
           #else:
           #    self.complete = ""

        # check before
        if charBefore and chr(charBefore) in "[]{}()" and styleBefore == stc.STC_P_OPERATOR:
            braceAtCaret = caretPos - 1

        # check after
        if braceAtCaret < 0:
            charAfter = self.GetCharAt(caretPos)
            styleAfter = self.GetStyleAt(caretPos)

            if charAfter and chr(charAfter) in "[]{}()" and styleAfter == stc.STC_P_OPERATOR:
                braceAtCaret = caretPos

        if braceAtCaret >= 0:
            braceOpposite = self.BraceMatch(braceAtCaret)

        if braceAtCaret != -1  and braceOpposite == -1:
            self.BraceBadLight(braceAtCaret)
        else:
            self.BraceHighlight(braceAtCaret, braceOpposite)
            #pt = self.PointFromPosition(braceOpposite)
            #self.Refresh(True, wxRect(pt.x, pt.y, 5,5))
            #print pt
            #self.Refresh(False)


    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True

        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break

        lineNum = 0

        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & stc.STC_FOLDLEVELHEADERFLAG and \
               (level & stc.STC_FOLDLEVELNUMBERMASK) == stc.STC_FOLDLEVELBASE:

                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)

                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)

            lineNum = lineNum + 1



    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)

            if level == -1:
                level = self.GetFoldLevel(line)

            if level & stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)

                    line = self.Expand(line, doExpand, force, visLevels-1)

                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1

        return line
    
    def getIndent(self, string):
        """Returns string used as indentation in given string"""

        return re.match('([ \t]*).*', string).groups()[0]
    
    def getIdentifier(self, pos = None):
        """Returns text marked as IDENTIFIER. Starts at current position""" 

        out = ""
        if pos is None:
            pos = self.GetCurrentPos() - 1 

        while self.GetStyleAt(pos) == stc.STC_P_IDENTIFIER:
            out = chr(self.GetCharAt(pos)) + out
            pos -= 1

        return out

    def getWORD2(self, pos = None):
        """Returns text marked as WORD2. Starts at current position""" 

        out = ""
        if pos is None:
            pos = self.GetCurrentPos() - 1 

        while self.GetStyleAt(pos) == stc.STC_P_WORD2:
            out = chr(self.GetCharAt(pos)) + out
            pos -= 1

        return out


    def getArgPos(self, id, n):
        """Returns position of the n-th argument in function description"""

        m = re.match(".*?\((.*?[,\)]){%d}" % (n) ,
                        self.api[id])

        if m is not None:
            return m.span(1)
        else:
            return (0, 0)


            

        
        

#----------------------------------------------------------------------
testCode = """

def main():
    OnFwd(OUT_AB, 100)
    Wait(2000)

    # Stop and return back

    OnRev(OUT_AB, 100)
    Wait(2000)


"""


if __name__ == '__main__':
    import sys,os
    app = wx.App()
    frame = wx.Frame(None, -1, title="test")
    ed = PythonSTC(frame, -1)
    ed.SetText(demoText + testCode)
    ed.EmptyUndoBuffer()
    ed.Colourise(0, -1)

    # line numbers in the margin
    ed.SetMarginType(1, stc.STC_MARGIN_NUMBER)
    ed.SetMarginWidth(1, 25)   
    
    frame.Show()
    app.MainLoop()


#----------------------------------------------------------------------
#----------------------------------------------------------------------

