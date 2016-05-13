__author__ = 'masslab'

from PyQt4 import QtGui, uic
from sub_ui.error_message import ErrorMessage


class AT106HSettings:
    """ Specific balance and run settings user interface """
    def __init__(self):
        self.window = QtGui.QDialog()
        self.ui = uic.loadUi('sub_ui/AT106H_Settings.ui', self.window)
        # self.ui = uic.loadUi('AT106H_Settings.ui', self.window)

        self.settings_dict = {}

        # Initial settings
        self.ui.CenteringsEdit.setText('0')
        self.ui.WaitTimeEdit.setText('0')
        self.ui.StabTimeEdit.setText('10')
        self.ui.IntegrationEdit.setText('5')
        self.ui.PreRunsEdit.setText('0')
        self.ui.RunsEdit.setText('1')

        # Activate click event detection
        self.ui.SubmitButton.clicked.connect(self.submit)

        self.window.exec_()

    def submit(self):
        try:
            self.settings_dict = {'resolution': int(self.ui.ResComboBox.currentIndex()),
                                  'centerings': int(self.ui.CenteringsEdit.text()),
                                  'wait time': float(self.ui.WaitTimeEdit.text()),
                                  'stab time': int(self.ui.StabTimeEdit.text()),
                                  'int time': int(self.ui.IntegrationEdit.text()),
                                  'pre runs': int(self.ui.PreRunsEdit.text()),
                                  'runs': int(self.ui.RunsEdit.text()),
                                  'tare at start': int(self.ui.TareCheckBox.isChecked()),
                                  'tare between runs': int(self.ui.AdjustCheckBox.isChecked())}
            self.window.close()
        except TypeError as e:
            message = 'All entries must be integers!\n %s' % e
            ErrorMessage(message)

    @staticmethod
    def is_number(s):
        try:
            float(s)
            if float(s) >= 0:
                return True
            else:
                return False
        except ValueError:
            return False