# -*- coding: utf-8 -*-
#@+leo-ver=5-thin
#@+node:ekr.20150514040146.1: * @file ../commands/rectangleCommands.py
#@@first
'''Leo's rectangle commands.'''
#@+<< imports >>
#@+node:ekr.20150514050446.1: ** << imports >> (rectangleCommands.py)
import leo.core.leoGlobals as g
from leo.commands.baseCommands import BaseEditCommandsClass as BaseEditCommandsClass
#@-<< imports >>

def cmd(name):
    '''Command decorator for the RectangleCommandsClass class.'''
    return g.new_cmd_decorator(name, ['c', 'rectangleCommands',])

class RectangleCommandsClass(BaseEditCommandsClass):
    #@+others
    #@+node:ekr.20150514063305.448: ** rectangle.ctor
    def __init__(self, c):
        '''Ctor for RectangleCommandsClass.'''
        self.c = c
        self.theKillRectangle = []
            # Do not re-init this!
        self.stringRect = None
        self.commandsDict = {
        'c': ('clear-rectangle', self.clearRectangle),
        'd': ('delete-rectangle', self.deleteRectangle),
        'k': ('kill-rectangle', self.killRectangle),
        'o': ('open-rectangle', self.openRectangle),
        'r': ('copy-rectangle-to-register', self.copyRectangleToRegister),
        't': ('string-rectangle', self.stringRectangle),
        'y': ('yank-rectangle', self.yankRectangle),
        }
    #@+node:ekr.20150514063305.451: ** check
    def check(self, event, warning='No rectangle selected'):
        '''
        Return True if there is a selection.
        Otherwise, return False and issue a warning.
        '''
        return self._chckSel(event, warning)
    #@+node:ekr.20150514063305.453: ** rectangle.Entries
    #@+node:ekr.20150514063305.454: *3* clearRectangle
    @cmd('rectangle-clear')
    def clearRectangle(self, event):
        '''Clear the rectangle defined by the start and end of selected text.'''
        w = self.editWidget(event)
        if not w or not self.check(event):
            return
        self.beginCommand(w, 'clear-rectangle')
        r1, r2, r3, r4 = self.getRectanglePoints(w)
        # Change the text.
        fill = ' ' * (r4 - r2)
        for r in range(r1, r3 + 1):
            w.delete('%s.%s' % (r, r2), '%s.%s' % (r, r4))
            w.insert('%s.%s' % (r, r2), fill)
        w.setSelectionRange('%s.%s' % (r1, r2), '%s.%s' % (r3, r2 + len(fill)))
        self.endCommand()
    #@+node:ekr.20150514063305.455: *3* closeRectangle
    @cmd('rectangle-close')
    def closeRectangle(self, event):
        '''Delete the rectangle if it contains nothing but whitespace..'''
        w = self.editWidget(event)
        if not w or not self.check(event):
            return
        self.beginCommand(w, 'close-rectangle')
        r1, r2, r3, r4 = self.getRectanglePoints(w)
        # Return if any part of the selection contains something other than whitespace.
        for r in range(r1, r3 + 1):
            s = w.get('%s.%s' % (r, r2), '%s.%s' % (r, r4))
            if s.strip(): return
        # Change the text.
        for r in range(r1, r3 + 1):
            w.delete('%s.%s' % (r, r2), '%s.%s' % (r, r4))
        i = '%s.%s' % (r1, r2)
        j = '%s.%s' % (r3, r2)
        w.setSelectionRange(i, j, insert=j)
        self.endCommand()
    #@+node:ekr.20150515060613.1: *3* copyRectangleToRegister
    @cmd('rectangle-copy-to-register')
    def copyRectangleToRegister(self, event):
        self.c.registerCommands.copyRectangleToRegister(event)
    #@+node:ekr.20150514063305.456: *3* deleteRectangle
    @cmd('rectangle-delete')
    def deleteRectangle(self, event):
        '''Delete the rectangle defined by the start and end of selected text.'''
        w = self.editWidget(event)
        if not w or not self.check(event):
            return
        self.beginCommand(w, 'delete-rectangle')
        r1, r2, r3, r4 = self.getRectanglePoints(w)
        for r in range(r1, r3 + 1):
            w.delete('%s.%s' % (r, r2), '%s.%s' % (r, r4))
        i = '%s.%s' % (r1, r2)
        j = '%s.%s' % (r3, r2)
        w.setSelectionRange(i, j, insert=j)
        self.endCommand()
    #@+node:ekr.20150514063305.457: *3* killRectangle
    @cmd('rectangle-kill')
    def killRectangle(self, event):
        '''Kill the rectangle defined by the start and end of selected text.'''
        w = self.editWidget(event)
        if not w or not self.check(event):
            return
        self.beginCommand(w, 'kill-rectangle')
        r1, r2, r3, r4 = self.getRectanglePoints(w)
        self.theKillRectangle = []
        for r in range(r1, r3 + 1):
            s = w.get('%s.%s' % (r, r2), '%s.%s' % (r, r4))
            self.theKillRectangle.append(s)
            w.delete('%s.%s' % (r, r2), '%s.%s' % (r, r4))
        if self.theKillRectangle:
            ins = '%s.%s' % (r, r2)
            w.setSelectionRange(ins, ins, insert=ins)
        self.endCommand()
    #@+node:ekr.20150514063305.458: *3* openRectangle
    @cmd('rectangle-open')
    def openRectangle(self, event):
        '''
        Insert blanks in the rectangle defined by the start and end of selected
        text. This pushes the previous contents of the rectangle rightward.
        '''
        w = self.editWidget(event)
        if not w or not self.check(event):
            return
        self.beginCommand(w, 'open-rectangle')
        r1, r2, r3, r4 = self.getRectanglePoints(w)
        fill = ' ' * (r4 - r2)
        for r in range(r1, r3 + 1):
            w.insert('%s.%s' % (r, r2), fill)
        i = '%s.%s' % (r1, r2)
        j = '%s.%s' % (r3, r2 + len(fill))
        w.setSelectionRange(i, j, insert=j)
        self.endCommand()
    #@+node:ekr.20150514063305.459: *3* stringRectangle
    @cmd('rectangle-string')
    def stringRectangle(self, event):
        '''
        Prompt for a string, then replace the contents of a rectangle
        with a string on each line.
        '''
        c, k = self.c, self.c.k
        state = k.getState('string-rect')
        if g.app.unitTesting:
            state = 1
            k.arg = 's...s' # This string is known to the unit test.
            w = self.editWidget(event)
            self.stringRect = self.getRectanglePoints(w)
        if state == 0:
            self.w = self.editWidget(event)
            if self.w and self.check(event):
                self.stringRect = self.getRectanglePoints(self.w)
                k.setLabelBlue('String rectangle: ')
                k.getArg(event, 'string-rect', 1, self.stringRectangle)
        else:
            k.clearState()
            k.resetLabel()
            c.bodyWantsFocus()
            w = self.w
            self.beginCommand(w, 'string-rectangle')
            # pylint: disable=unpacking-non-sequence
            r1, r2, r3, r4 = self.stringRect
            s = w.getAllText()
            for r in range(r1, r3 + 1):
                i = g.convertRowColToPythonIndex(s, r - 1, r2)
                j = g.convertRowColToPythonIndex(s, r - 1, r4)
                s = s[: i] + k.arg + s[j:]
            w.setAllText(s)
            i = g.convertRowColToPythonIndex(s, r1 - 1, r2)
            j = g.convertRowColToPythonIndex(s, r3 - 1, r2 + len(k.arg))
            w.setSelectionRange(i, j)
            self.endCommand()
            # 2010/1/1: Fix bug 480422:
            # string-rectangle kills syntax highlighting.
            c.frame.body.recolor(c.p, incremental=False)
    #@+node:ekr.20150514063305.460: *3* yankRectangle
    @cmd('rectangle-yank')
    def yankRectangle(self, event, killRect=None):
        '''Yank into the rectangle defined by the start and end of selected text.'''
        # c = self.c
        k = self.c.k
        w = self.editWidget(event)
        if not w:
            return
        killRect = killRect or self.theKillRectangle
        if g.app.unitTesting:
            # This value is used by the unit test.
            killRect = ['Y1Y', 'Y2Y', 'Y3Y', 'Y4Y']
        elif not killRect:
            k.setLabelGrey('No kill rect')
            return
        self.beginCommand(w, 'yank-rectangle')
        r1, r2, r3, r4 = self.getRectanglePoints(w)
        n = 0
        for r in range(r1, r3 + 1):
            # g.trace(n,r,killRect[n])
            if n >= len(killRect): break
            w.delete('%s.%s' % (r, r2), '%s.%s' % (r, r4))
            w.insert('%s.%s' % (r, r2), killRect[n])
            n += 1
        i = '%s.%s' % (r1, r2)
        j = '%s.%s' % (r3, r2 + len(killRect[n - 1]))
        w.setSelectionRange(i, j, insert=j)
        self.endCommand()
    #@-others
#@-leo
