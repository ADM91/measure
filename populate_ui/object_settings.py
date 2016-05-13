__author__ = 'masslab'

from PyQt4 import QtGui, QtCore


try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8

    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


def object_settings(cls):
    """ Populates menus, sets headers, and sets button access in main ui"""
    cls = cls.ui
    # Set up sizing convention for mass table
    cls.weightTable.autoFillBackground()

    # Set up mass setup table with selected number of columns
    column_count = 13
    cls.weightTable.setColumnCount(column_count)
    cls.weightTable.setRowCount(0)
    for i in range(column_count):
        item = QtGui.QTableWidgetItem()
        cls.weightTable.setHorizontalHeaderItem(i, item)

    # Set Headers for the mass table
    item = cls.weightTable.horizontalHeaderItem(0)
    item.setText(_translate("MainWindow", "Weight", None))
    item = cls.weightTable.horizontalHeaderItem(1)
    item.setText(_translate("MainWindow", "Role", None))
    item = cls.weightTable.horizontalHeaderItem(2)
    item.setText(_translate("MainWindow", "CoG Diff [cm]", None))
    item = cls.weightTable.horizontalHeaderItem(3)
    item.setText(_translate("MainWindow", "Addon 1", None))
    item = cls.weightTable.horizontalHeaderItem(4)
    item.setText(_translate("MainWindow", "Addon 2", None))
    item = cls.weightTable.horizontalHeaderItem(5)
    item.setText(_translate("MainWindow", "Addon 3", None))
    item = cls.weightTable.horizontalHeaderItem(6)
    item.setText(_translate("MainWindow", "Addon 4", None))
    item = cls.weightTable.horizontalHeaderItem(7)
    item.setText(_translate("MainWindow", "Addon 5", None))
    item = cls.weightTable.horizontalHeaderItem(8)
    item.setText(_translate("MainWindow", "Addon 6", None))
    item = cls.weightTable.horizontalHeaderItem(9)
    item.setText(_translate("MainWindow", "Addon 7", None))
    item = cls.weightTable.horizontalHeaderItem(10)
    item.setText(_translate("MainWindow", "Addon 8", None))
    item = cls.weightTable.horizontalHeaderItem(11)
    item.setText(_translate("MainWindow", "Addon 9", None))
    item = cls.weightTable.horizontalHeaderItem(12)
    item.setText(_translate("MainWindow", "Addon 10", None))

    # Set Header for the tree widget
    cls.weightTree.headerItem().setText(0, _fromUtf8("Database Weights"))

    # Set drag and drop settings
    cls.weightTree.setDragEnabled(True)
    cls.weightTable.setAcceptDrops(True)
