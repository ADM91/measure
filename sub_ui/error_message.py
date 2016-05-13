__author__ = 'masslab'

from PyQt4 import QtGui


class ErrorMessage(QtGui.QDialog):
    """
    This is a dialog that pops up when the user has to be notified of an error in the
    usage of the interface.
    This dialog is modal, the user must close it before interacting with with main interface again.
    """
    def __init__(self, message):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("Error")
        self.setFixedWidth(200)
        self.labelMess = QtGui.QLabel(self)
        self.labelMess.setText(message)
        self.buttonAgain = QtGui.QPushButton('Ok', self)
        self.buttonAgain.clicked.connect(self.handleAgain)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.labelMess)
        layout.addWidget(self.buttonAgain)
        self.exec_()

    def handleAgain(self):
        self.close()
