__author__ = 'masslab'

from PyQt4 import QtGui
try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def populate_table_widget(cls):
    role_options = ["Unkn", "Restraint", "Check"]

    # Set table length
    m = len(cls.main_dict['design matrix'][0])
    cls.ui.weightTable.setRowCount(m)

    # Populate Table one row at at time
    for n in range(0, m):

        # clear row
        for n2 in range(0, int(cls.ui.weightTable.columnCount())):
            item = QtGui.QTableWidgetItem()
            item.setText("")
            cls.ui.weightTable.setItem(n, n2, item)

        # Set Row name
        item = QtGui.QTableWidgetItem()
        cls.ui.weightTable.setVerticalHeaderItem(n, item)
        item = cls.ui.weightTable.verticalHeaderItem(n)
        item.setText(_translate("MainWindow", "Pos. %s" % (n+1), None))

        # Insert Combobox for roles
        roles = QtGui.QComboBox()
        roles.addItems(role_options)
        cls.ui.weightTable.setCellWidget(n, 1, roles)

        # Insert Text edit for cog
        cog = QtGui.QLineEdit()
        cog.setAcceptDrops(False)
        cls.ui.weightTable.setCellWidget(n, 2, cog)
        cls.ui.weightTable.cellWidget(n, 2).setText("0")

        # Make table un editable
        cls.ui.weightTable.setEditTriggers(QtGui.QAbstractItemView.NoEditTriggers)
