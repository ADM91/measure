__author__ = 'masslab'

from PyQt4 import QtGui, QtCore
from utility.database_orm import DatabaseORM
from login_failed import LoginFailed
from error_message import ErrorMessage
# from main_ui import app


class LoginUi(QtGui.QDialog):
    """ Database login ui """
    def __init__(self, quit_signal):
        QtGui.QDialog.__init__(self)
        self.setWindowTitle("Database Login")
        self.labelUsr = QtGui.QLabel(self)
        self.labelUsr.setText("Username:")
        self.labelPass = QtGui.QLabel(self)
        self.labelPass.setText("Password:")
        self.textUsr = QtGui.QLineEdit(self)
        self.textPass = QtGui.QLineEdit(self)
        self.textPass.setEchoMode(QtGui.QLineEdit.Password)
        self.buttonLogin = QtGui.QPushButton('Login', self)
        self.buttonLogin.clicked.connect(self.handle_login)
        layout = QtGui.QVBoxLayout(self)
        layout.addWidget(self.labelUsr)
        layout.addWidget(self.textUsr)
        layout.addWidget(self.labelPass)
        layout.addWidget(self.textPass)
        layout.addWidget(self.buttonLogin)
        self.ident = None
        self.db = None
        self.quit_signal = quit_signal
        self.exec_()

    def handle_login(self):

        # Instantiate database
        self.db = DatabaseORM()
        identifier = self.db.check_user_password(self.textUsr.text(), self.textPass.text())
        if identifier:
            self.ident = identifier
            self.close()
        else:
            ErrorMessage('Login failed')


