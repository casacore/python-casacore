from wxPython.grid import *
from wxPython.wx import *

import six


class wxCasaTable(wxPyGridTableBase):
    """
    This is all it takes to make a custom data table to plug into a
    wxGrid.  There are many more methods that can be overridden, but
    the ones shown below are the required ones.  This table simply
    provides strings containing the row and column values.
    """

    def __init__(self, log, ctable):
        wxPyGridTableBase.__init__(self)
        self.log = log
        self.casatab = ctable
        self.odd = wxGridCellAttr()
        self.odd.SetBackgroundColour("gray90")
        self.even = wxGridCellAttr()
        self.even.SetBackgroundColour("white")

    def GetAttr(self, row, col, kind):
        attr = [self.even, self.odd][row % 2]
        attr.IncRef()
        return attr

    def GetColLabelValue(self, col):
        colnames = self.casatab.colnames()
        return colnames[col]

    def GetNumberRows(self):
        return self.casatab.nrows()

    def GetNumberCols(self):
        return self.casatab.ncols()

    def IsEmptyCell(self, row, col):
        return False

    def GetValue(self, row, col):
        coln = self.casatab.colnames()
        cell = 'array'
        ##         if self.casatab.isscalarcol(coln[col]):
        ##             cellval = self.casatab.getcell(coln[col],row)
        ##             if isinstance(cellval,float):
        ##                 if coln[col] == "TIME":
        ##                     cell = str(cellval)
        ##                 else:
        ##                     cell = "%3.5f" % cellval
        ##             else:
        ##                 cell = str(cellval)
        ##         else:
        ##             cell += self.casatab.getcolshapestring(coln[col],row,1)[0]
        ##         return cell
        return str(self.casatab.getcell(coln[col], row))

    def SetValue(self, row, col, value):
        self.log.write('SetValue(%d, %d, "%s") ignored.\n' % (row, col, value))


# ---------------------------------------------------------------------------

class wxCasaTableGrid(wxGrid):
    def __init__(self, parent, log, ctable):
        wxGrid.__init__(self, parent, -1)
        table = wxCasaTable(log, ctable)
        # The second parameter means that the grid is to take ownership of the
        # table and will destroy it when done.  Otherwise you would need to keep
        # a reference to it and call it's Destroy method later.
        self.SetTable(table, True)
        EVT_GRID_CELL_RIGHT_CLICK(self, self.OnRightDown)  # added

    def OnRightDown(self, event):  # added
        six.print_(self.GetSelectedRows())  # added


# ---------------------------------------------------------------------------

class CasaTestFrame(wxFrame):
    def __init__(self, parent, log, ctable):
        wxFrame.__init__(self, parent, -1, "Casa Table Browser",
                         size=(640, 480))
        grid = wxCasaTableGrid(self, log, ctable)
        grid.EnableEditing(False)
        # grid.AutoSizeColumns()


# ---------------------------------------------------------------------------

if __name__ == '__main__':
    import sys

    app = wxPySimpleApp()
    from casacore.tables import table as casatable

    casatab = casatable('/nfs/aips++/data/atnf/scripts/C972.ms')
    frame = CasaTestFrame(None, sys.stdout, casatab)
    frame.Show(True)
    app.MainLoop()


# ---------------------------------------------------------------------------
