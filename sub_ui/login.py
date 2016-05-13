__author__ = 'masslab'

from PyQt4 import QtGui


class LoginUi(QtGui.QDialog):
    """ Database login ui """
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("Database Login")
        self.labelName = QtGui.QLabel(self)
        self.labelName.setText("Username:")
        self.labelPass = QtGui.QLabel(self)
        self.labelPass.setText("Password:")
        self.textName = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.labelName)
        layout.addWidget(self.textName)
        layout.addWidget(self.labelPass)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)

    def handle_login(self):
        self.setVisible(False)
